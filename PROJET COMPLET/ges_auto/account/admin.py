from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'photo_preview',
        'username',
        'matricule',
        'full_name_display',
        'email',
        'role',
        'fonction',
        'service',
        'telephone_pro',
        'telephone_perso',
        'adresse_complete',
        'date_embauche',
        'duree_service',
        'derniere_activite',
        'is_active',
        'permissions_display',
    )
    
    list_filter = (
        'role',
        'is_active',
        'service',
        'date_embauche',
        'acces_gestion_vehicules',
        'acces_maintenance',
        'acces_rapports'
    )
    
    search_fields = (
        'username',
        'matricule',
        'nom',
        'prenom',
        'email',
        'telephone_pro',
        'telephone_perso',
        'adresse',
        'ville'
    )
    
    ordering = ('-date_enregistrement',)
    list_per_page = 50
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'matricule')
        }),
        (_('Informations personnelles'), {
            'fields': (
                'nom',
                'prenom',
                'email',
                'photo_profile',
                'adresse',
                'code_postal',
                'ville',
                'telephone_perso'
            )
        }),
        (_('Informations professionnelles'), {
            'fields': (
                'role',
                'fonction',
                'service',
                'telephone_pro',
                'date_embauche'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'acces_gestion_vehicules',
                'acces_maintenance',
                'acces_rapports',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Dates importantes'), {
            'fields': (
                'last_login',
                'dernier_connexion',
                'date_modification',
                'date_enregistrement'
            )
        }),
    )
    
    readonly_fields = (
        'date_modification',
        'date_enregistrement',
        'dernier_connexion'
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'role',
                'matricule',
                'nom',
                'prenom',
                'email'
            ),
        }),
    )

    def full_name_display(self, obj):
        return format_html(
            '<strong>{}</strong> {}',
            obj.nom,
            obj.prenom
        )
    full_name_display.short_description = _('Nom complet')

    def photo_preview(self, obj):
        if obj.photo_profile:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.photo_profile.url
            )
        return format_html(
            '<div style="width: 40px; height: 40px; border-radius: 50%; background-color: #ccc; display: flex; align-items: center; justify-content: center;">'
            '<span style="color: #666;">?</span>'
            '</div>'
        )
    photo_preview.short_description = _('Photo')

    def adresse_complete(self, obj):
        if obj.adresse:
            return format_html(
                '{}<br>{} {}',
                obj.adresse,
                obj.code_postal or '',
                obj.ville or ''
            )
        return '-'
    adresse_complete.short_description = _('Adresse')

    def duree_service(self, obj):
        if obj.date_embauche:
            duree = now().date() - obj.date_embauche
            annees = duree.days // 365
            mois = (duree.days % 365) // 30
            return format_html(
                '{} an(s) {} mois',
                annees,
                mois
            )
        return '-'
    duree_service.short_description = _('Ancienneté')

    def derniere_activite(self, obj):
        if obj.dernier_connexion:
            return obj.dernier_connexion.strftime('%d/%m/%Y %H:%M')
        return '-'
    derniere_activite.short_description = _('Dernière activité')

    def permissions_display(self, obj):
        permissions = []
        if obj.acces_gestion_vehicules:
            permissions.append('Véhicules')
        if obj.acces_maintenance:
            permissions.append('Maintenance')
        if obj.acces_rapports:
            permissions.append('Rapports')
        
        if not permissions:
            return format_html(
                '<span style="color: #999;">Aucune permission</span>'
            )
        
        return format_html(
            '<span style="color: #28a745;">{}</span>',
            ', '.join(permissions)
        )
    permissions_display.short_description = _('Permissions')

    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            if not obj.password:  # Si aucun mot de passe n'est défini
                obj.set_password(obj.username)  # Utilise le nom d'utilisateur comme mot de passe par défaut
        super().save_model(request, obj, form, change)