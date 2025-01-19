from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé basé sur AbstractUser avec des champs supplémentaires.
    """
    matricule = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Matricule",
        help_text="Identifiant unique de l'employé"
    )
    nom = models.CharField(
        max_length=255, 
        verbose_name="Nom",
        help_text="Nom de famille de l'utilisateur"
    )
    prenom = models.CharField(
        max_length=255, 
        verbose_name="Prénom",
        help_text="Prénom de l'utilisateur"
    )
    fonction = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Fonction",
        help_text="Poste occupé dans l'entreprise"
    )
    adresse = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Adresse",
        help_text="Adresse postale de l'utilisateur"
    )
    date_embauche = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Date d'embauche",
        help_text="Date d'entrée dans l'entreprise"
    )
    dernier_connexion = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Dernière connexion",
        help_text="Date et heure de la dernière connexion"
    )
    date_modification = models.DateTimeField(
        auto_now=True, 
        verbose_name="Date de modification",
        help_text="Date de dernière modification du profil"
    )
    date_enregistrement = models.DateTimeField(
        default=now, 
        verbose_name="Date d'enregistrement",
        help_text="Date de création du compte"
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name=_('groups'),
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.')
    )

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ['-date_enregistrement']

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"

    def clean(self):
        """
        Validation personnalisée pour le modèle
        """
        if self.date_embauche and self.date_embauche > now().date():
            raise ValidationError({
                'date_embauche': _("La date d'embauche ne peut pas être dans le futur.")
            })

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour effectuer des validations supplémentaires
        """
        self.clean()
        self.username = self.username.lower()  # Normalisation du nom d'utilisateur
        self.email = self.email.lower()  # Normalisation de l'email
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        """
        Retourne le nom complet de l'utilisateur
        """
        return f"{self.prenom} {self.nom}".strip()

    def get_active_duration(self):
        """
        Calcule la durée depuis l'embauche
        """
        if self.date_embauche:
            return now().date() - self.date_embauche
        return None