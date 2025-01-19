from django.contrib import admin
from .models import Trajet

@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ('lieu_depart', 'destination', 'date_depart', 'status', 'vehicule', 'personnel')
    list_filter = ('status', 'date_depart', 'vehicule', 'personnel')
    search_fields = ('lieu_depart', 'destination', 'motif')
    readonly_fields = ('date_creation', 'date_modification')
    fieldsets = (
        (None, {
            'fields': ('lieu_depart', 'destination', 'date_depart', 'date_arrivee')
        }),
        ('Coordonnées', {
            'fields': (('depart_lat', 'depart_lon'), ('destination_lat', 'destination_lon'))
        }),
        ('Détails', {
            'fields': ('motif', 'distance', 'cout_estime', 'status')
        }),
        ('Assignation', {
            'fields': ('vehicule', 'personnel')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )