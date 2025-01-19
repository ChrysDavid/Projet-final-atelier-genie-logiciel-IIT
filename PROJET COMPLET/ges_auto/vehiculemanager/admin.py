from django.contrib import admin
from .models import Vehicule, Carburant, Maintenance


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'marque', 'modele', 'categorie', 'status', 'annee', 'kilometrage', 'date_acquisition')
    list_filter = ('status', 'categorie', 'annee')
    search_fields = ('immatriculation', 'marque', 'modele')
    ordering = ('-date_enregistrement',)



@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicule', 'date_maintenance', 'type', 'status', 'cout')
    list_filter = ('status', 'vehicule')
    search_fields = ('vehicule__immatriculation', 'type', 'description')
    ordering = ('-date_maintenance',)



@admin.register(Carburant)
class CarburantAdmin(admin.ModelAdmin):
    list_display = ('date_prise', 'quantite', 'cout_unitaire', 'cout_total', 'type_carburant', 'station', 'kilometrage_actuel', 'vehicule_id')
    list_filter = ('type_carburant', 'station')
    search_fields = ('type_carburant', 'station', 'vehicule_id')
    ordering = ('-date_prise',)
