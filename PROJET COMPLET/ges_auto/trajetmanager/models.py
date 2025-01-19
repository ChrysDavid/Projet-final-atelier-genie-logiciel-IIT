from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from vehiculemanager.models import Vehicule
from account.models import CustomUser

class Trajet(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    date_depart = models.DateTimeField(verbose_name="Date de départ")
    date_arrivee = models.DateTimeField(null=True, blank=True, verbose_name="Date d'arrivée")
    lieu_depart = models.CharField(max_length=255, verbose_name="Lieu de départ")
    destination = models.CharField(max_length=255, verbose_name="Destination")
    depart_lat = models.FloatField(null=True, blank=True)
    depart_lon = models.FloatField(null=True, blank=True)
    destination_lat = models.FloatField(null=True, blank=True)
    destination_lon = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True, verbose_name="Distance (km)")
    motif = models.TextField(verbose_name="Motif du trajet")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    cout_estime = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    personnel = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(default=now)
    date_modification = models.DateTimeField(auto_now=True)

    def get_progress(self):
        if self.status == 'termine':
            return 100
        elif self.status == 'en_cours':
            if self.date_arrivee:
                total_duration = (self.date_arrivee - self.date_depart).total_seconds()
                elapsed = (timezone.now() - self.date_depart).total_seconds()
                return min(int((elapsed / total_duration) * 100), 99)
            return 50
        elif self.status == 'en_attente':
            return 0
        return 0

    def get_status_color(self):
        return {
            'en_attente': 'warning',
            'en_cours': 'info',
            'termine': 'success',
            'annule': 'danger',
        }.get(self.status, 'secondary')

    def __str__(self):
        return f"{self.lieu_depart} → {self.destination} ({self.date_depart})"

    class Meta:
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        ordering = ['-date_depart']
