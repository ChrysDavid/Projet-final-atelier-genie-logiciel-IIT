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
