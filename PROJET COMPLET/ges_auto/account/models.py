from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ROLES(models.TextChoices):
    SUPERUSER = 'SUPERUSER', _('Super Administrateur')
    SECRETAIRE = 'SECRETAIRE', _('Secrétaire')
    EMPLOYE = 'EMPLOYE', _('Employé')

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé pour la gestion de flotte automobile
    """
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='customuser_set',
        related_query_name='customuser'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_set',
        related_query_name='customuser'
    )
    
    matricule = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Matricule",
        null=True,
        blank=True
    )
    nom = models.CharField(
        max_length=255, 
        verbose_name="Nom",
        null=True,
        blank=True
    )
    prenom = models.CharField(
        max_length=255, 
        verbose_name="Prénom",
        null=True,
        blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES.choices,
        default=ROLES.SUPERUSER,
        verbose_name="Rôle"
    )
    
    # Informations professionnelles
    fonction = models.CharField(max_length=255, blank=True, null=True)
    telephone_pro = models.CharField(max_length=20, blank=True, null=True)
    service = models.CharField(max_length=100, blank=True, null=True)
    
    # Informations personnelles
    photo_profile = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )
    adresse = models.CharField(max_length=255, blank=True, null=True)
    code_postal = models.CharField(max_length=10, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    telephone_perso = models.CharField(max_length=20, blank=True, null=True)
    
    # Dates importantes
    date_embauche = models.DateField(blank=True, null=True)
    dernier_connexion = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_enregistrement = models.DateTimeField(default=now)

    # Permissions spécifiques pour la gestion de flotte
    acces_gestion_vehicules = models.BooleanField(
        default=False,
        verbose_name="Accès à la gestion des véhicules"
    )
    acces_maintenance = models.BooleanField(
        default=False,
        verbose_name="Accès à la maintenance"
    )
    acces_rapports = models.BooleanField(
        default=False,
        verbose_name="Accès aux rapports"
    )

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ['-date_enregistrement']

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"

    def clean(self):
        super().clean()
        if self.date_embauche and self.date_embauche > now().date():
            raise ValidationError({
                'date_embauche': _("La date d'embauche ne peut pas être dans le futur.")
            })
        
        # Attribution des permissions selon le rôle
        if self.role == ROLES.SUPERUSER:
            self.acces_gestion_vehicules = True
            self.acces_maintenance = True
            self.acces_rapports = True
        elif self.role == ROLES.SECRETAIRE:
            self.acces_gestion_vehicules = True
            self.acces_rapports = True
            self.acces_maintenance = False
        elif self.role == ROLES.EMPLOYE:
            self.acces_gestion_vehicules = False
            self.acces_maintenance = False
            self.acces_rapports = False

    def save(self, *args, **kwargs):
        # Générer un matricule par défaut si non fourni
        if not self.matricule:
            self.matricule = f"USER{now().strftime('%Y%m%d%H%M%S')}"
        
        # Générer nom/prénom par défaut si non fournis
        if not self.nom:
            self.nom = self.username.upper()
        if not self.prenom:
            self.prenom = "Admin" if self.role == ROLES.SUPERUSER else self.username.capitalize()

        self.clean()
        self.username = self.username.lower()
        self.email = self.email.lower()
        
        # Gestion des droits administratifs
        if self.role == ROLES.SUPERUSER:
            self.is_staff = True
            self.is_superuser = True
        elif self.role == ROLES.SECRETAIRE:
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
            
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.prenom} {self.nom}".strip()

    def get_active_duration(self):
        if self.date_embauche:
            return now().date() - self.date_embauche
        return None