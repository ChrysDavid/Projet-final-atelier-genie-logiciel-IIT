# forms.py
from django import forms
from .models import Trajet

class TrajetForm(forms.ModelForm):
    class Meta:
        model = Trajet
        fields = [
            'date_depart', 'date_arrivee', 'lieu_depart', 'destination',
            'distance', 'motif', 'status', 'cout_estime', 'vehicule', 'personnel'
        ]
        widgets = {
            'date_depart': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'date_arrivee': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'lieu_depart': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Adresse de départ'}
            ),
            'destination': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Adresse de destination'}
            ),
            'distance': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.1'}
            ),
            'motif': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'cout_estime': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
            'vehicule': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'personnel': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }