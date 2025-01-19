from django import forms
from .models import Rapport

class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ['date_creation', 'type', 'contenu', 'periode', 'archive', 'utilisateur']
        widgets = {
            'date_creation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control'}),
            'periode': forms.TextInput(attrs={'class': 'form-control'}),
            'archive': forms.Select(choices=[(False, 'Actif'), (True, 'Archivé')], attrs={'class': 'form-control'}),
            'utilisateur': forms.Select(attrs={'class': 'form-control'}),
        }
