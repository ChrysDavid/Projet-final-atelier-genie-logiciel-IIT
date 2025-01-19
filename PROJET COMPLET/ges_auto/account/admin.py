# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Administration personnalisée pour CustomUser.
    """
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('matricule', 'nom', 'prenom', 'fonction', 'adresse', 'date_embauche')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('matricule', 'nom', 'prenom', 'fonction', 'adresse', 'date_embauche')}),
    )
    list_display = ['username', 'email', 'matricule', 'nom', 'prenom', 'is_active']
    search_fields = ['username', 'email', 'matricule', 'nom', 'prenom']
