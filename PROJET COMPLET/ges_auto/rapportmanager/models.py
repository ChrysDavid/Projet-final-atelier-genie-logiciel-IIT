from django.db import models
from django.utils.timezone import now
from account.models import CustomUser

class Rapport(models.Model):
    """
    Modèle pour la gestion des rapports.
    """
    date_creation = models.DateField(verbose_name="Date de création", default=now)
    type = models.CharField(max_length=50, verbose_name="Type")
    contenu = models.TextField(verbose_name="Contenu")
    periode = models.CharField(max_length=50, verbose_name="Période")
    archive = models.BooleanField(default=False, verbose_name="Archivé")
    utilisateur = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur",
        help_text="Utilisateur responsable du rapport"
    )
    date_enregistrement = models.DateTimeField(default=now, verbose_name="Date d'enregistrement")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.type} - {self.periode} ({self.utilisateur.full_name})"
