from django.db import models
from django.utils.timezone import now

class Vehicule(models.Model):
    STATUS_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Indisponible', 'Indisponible'),
    ]

    CATEGORIE_CHOICES = [
        ('Transporteur de marchandise', 'Transporteur de marchandise'),
        ('Ramasseur de déchet', 'Ramasseur de déchet'),
        ('Transporteur de passagers', 'Transporteur de passagers'),
        ('Autre', 'Autre'),
    ]

    immatriculation = models.CharField(max_length=50, unique=True, verbose_name="Immatriculation")
    marque = models.CharField(max_length=255, verbose_name="Marque")
    modele = models.CharField(max_length=255, verbose_name="Modèle")
    annee = models.PositiveIntegerField(verbose_name="Année")
    categorie = models.CharField(max_length=255, choices=CATEGORIE_CHOICES, verbose_name="Catégorie")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Disponible', verbose_name="Statut")
    date_acquisition = models.DateField(null=True, blank=True, verbose_name="Date d'acquisition")
    date_derniere_maintenance = models.DateField(null=True, blank=True, verbose_name="Date de dernière maintenance")
    kilometrage = models.PositiveIntegerField(null=True, blank=True, verbose_name="Kilométrage")
    image_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="URL de l'image")
    date_enregistrement = models.DateTimeField(default=now, verbose_name="Date d'enregistrement")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"

    class Meta:
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"
        ordering = ['-date_enregistrement']




class Maintenance(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
    ]

    date_maintenance = models.DateField(verbose_name="Maintenance Date")
    type = models.CharField(max_length=50, verbose_name="Type of Maintenance")
    description = models.TextField(verbose_name="Description", blank=True)
    cout = models.FloatField(verbose_name="Cost")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Status")
    pieces_changees = models.TextField(verbose_name="Replaced Parts", blank=True)
    date_prochaine_maintenance = models.DateField(null=True, blank=True, verbose_name="Next Maintenance Date")
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, verbose_name="Vehicle")
    date_enregistrement = models.DateTimeField(default=now, verbose_name="Date Recorded")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date Modified")

    def __str__(self):
        return f"Maintenance {self.type} for {self.vehicule.immatriculation} on {self.date_maintenance}"

    class Meta:
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenances"
        ordering = ['-date_maintenance']



class Carburant(models.Model):
    date_prise = models.DateField(verbose_name="Date Prise")
    quantite = models.FloatField(verbose_name="Quantité (L)")
    cout_unitaire = models.FloatField(null=True, blank=True, verbose_name="Coût Unitaire")
    cout_total = models.FloatField(null=True, blank=True, verbose_name="Coût Total")
    type_carburant = models.CharField(max_length=50, verbose_name="Type Carburant")
    station = models.CharField(max_length=255, verbose_name="Station")
    kilometrage_actuel = models.PositiveIntegerField(verbose_name="Kilométrage Actuel")
    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Véhicule"
    )
    date_enregistrement = models.DateTimeField(default=now, verbose_name="Date d'Enregistrement")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de Modification")

    def __str__(self):
        if self.vehicule:
            return f"{self.type_carburant} - {self.quantite}L (Véhicule {self.vehicule.immatriculation})"
        return f"{self.type_carburant} - {self.quantite}L (Aucun véhicule associé)"


    class Meta:
        verbose_name = "Carburant"
        verbose_name_plural = "Carburants"
        ordering = ['-date_prise']
