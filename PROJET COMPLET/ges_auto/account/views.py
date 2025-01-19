# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm
from .models import CustomUser

# views.py
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            try:
                # Essayer de trouver l'utilisateur par email d'abord
                if '@' in username_or_email:
                    user_obj = CustomUser.objects.get(email=username_or_email)
                    username = user_obj.username
                else:
                    username = username_or_email
                
                # Authentifier l'utilisateur
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    user.dernier_connexion = timezone.now()
                    user.save()
                    messages.success(request, 'Connexion réussie!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Mot de passe incorrect.')
            
            except CustomUser.DoesNotExist:
                messages.error(request, 'Aucun compte trouvé avec ces identifiants.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs du formulaire.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})




# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Compte créé avec succès!')
#             return redirect('utilisateur:dashboard')
#         else:
#             messages.error(request, 'Erreur lors de la création du compte.')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('utilisateur:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('utilisateur:profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


def forgot_password(request):
    return render(request, 'forgot-password.html')