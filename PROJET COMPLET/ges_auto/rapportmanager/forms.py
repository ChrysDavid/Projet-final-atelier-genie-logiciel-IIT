from django import forms
from .models import Rapport
from account.models import CustomUser, ROLES

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les utilisateurs pour n'inclure que les employés et les secrétaires
        self.fields['utilisateur'].queryset = CustomUser.objects.filter(
            role__in=[ROLES.EMPLOYE, ROLES.SECRETAIRE]
        ).order_by('nom', 'prenom')
