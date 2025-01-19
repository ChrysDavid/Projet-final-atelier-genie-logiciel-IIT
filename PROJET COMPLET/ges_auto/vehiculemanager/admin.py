from django.contrib import admin
from .models import Vehicule

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'marque', 'modele', 'categorie', 'status', 'annee', 'kilometrage', 'date_acquisition')
    list_filter = ('status', 'categorie', 'annee')
    search_fields = ('immatriculation', 'marque', 'modele')
    ordering = ('-date_enregistrement',)
