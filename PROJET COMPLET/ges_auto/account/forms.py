# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire pour la création d'un nouvel utilisateur avec des champs personnalisés.
    """
    email = forms.EmailField(required=True, label="Adresse e-mail")

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'matricule', 'nom', 'prenom', 'fonction', 
            'adresse', 'date_embauche'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username or email',
                'autofocus': True
            }
        )
    )
    password = forms.CharField(
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
            # Try to get user by email first
            try:
                user = CustomUser.objects.get(email=username)
                username = user.username
            except CustomUser.DoesNotExist:
                pass

        self.cleaned_data['username'] = username
        return super().clean()


class CustomUserUpdateForm(forms.ModelForm):
    """
    Formulaire pour la mise à jour des informations utilisateur.
    """
    email = forms.EmailField(required=True, label="Adresse e-mail")

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'matricule', 'nom', 'prenom',
            'fonction', 'adresse', 'date_embauche'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
