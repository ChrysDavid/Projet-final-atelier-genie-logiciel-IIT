from django import forms
from .models import Vehicule, Maintenance, Carburant



class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = [
            'immatriculation', 'marque', 'modele', 'annee', 'categorie',
            'status', 'date_acquisition', 'date_derniere_maintenance',
            'kilometrage', 'image_url'
        ]
        widgets = {
            'date_acquisition': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_derniere_maintenance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'immatriculation': forms.TextInput(attrs={'class': 'form-control'}),
            'marque': forms.TextInput(attrs={'class': 'form-control'}),
            'modele': forms.TextInput(attrs={'class': 'form-control'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'kilometrage': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }



class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'date_maintenance', 'type', 'description', 'cout',
            'status', 'pieces_changees', 'date_prochaine_maintenance', 'vehicule'
        ]
        widgets = {
            'date_maintenance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_prochaine_maintenance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cout': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'pieces_changees': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'vehicule': forms.Select(attrs={'class': 'form-select'}),
        }



class CarburantForm(forms.ModelForm):
    class Meta:
        model = Carburant
        fields = [
            'date_prise', 'quantite', 'cout_unitaire', 'cout_total',
            'type_carburant', 'station', 'kilometrage_actuel', 'vehicule'
        ]
        widgets = {
            'date_prise': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'cout_unitaire': forms.NumberInput(attrs={'class': 'form-control'}),
            'cout_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_carburant': forms.TextInput(attrs={'class': 'form-control'}),
            'station': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometrage_actuel': forms.NumberInput(attrs={'class': 'form-control'}),
            'vehicule': forms.Select(attrs={'class': 'form-control'}),
        }