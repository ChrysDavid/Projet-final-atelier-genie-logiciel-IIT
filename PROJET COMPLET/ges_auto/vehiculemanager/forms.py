from django import forms
from .models import Vehicule

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
