from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire pour la création d'un nouvel utilisateur avec des champs personnalisés.
    """
    email = forms.EmailField(
        required=True, 
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2',
            'matricule', 
            'nom', 
            'prenom', 
            'fonction', 
            'adresse', 
            'date_embauche'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'fonction': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulaire d'authentification personnalisé permettant la connexion 
    par nom d'utilisateur ou email
    """
    username = forms.CharField(
        label="Nom d'utilisateur ou Email",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre nom d\'utilisateur ou email',
                'autofocus': True
            }
        )
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '••••••••'
            }
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                if '@' in username:
                    user = CustomUser.objects.get(email=username)
                    username = user.username
            except CustomUser.DoesNotExist:
                pass

        self.cleaned_data['username'] = username
        return super().clean()

class CustomPasswordResetForm(forms.Form):
    """
    Formulaire de réinitialisation de mot de passe
    """
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre adresse email'
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Aucun compte n'est associé à cette adresse email.")
        return email