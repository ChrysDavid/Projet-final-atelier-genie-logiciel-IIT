from django.contrib import admin
from .models import Rapport

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation', 'type', 'periode', 'archive', 'utilisateur')
    list_filter = ('archive', 'date_creation', 'periode')
    search_fields = ('type', 'periode', 'contenu')
    ordering = ('-date_creation',)
