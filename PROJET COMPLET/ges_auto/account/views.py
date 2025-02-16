from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm
from .models import CustomUser, ROLES

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
                    if user.is_active:
                        login(request, user)
                        user.dernier_connexion = timezone.now()
                        user.save()
                        messages.success(request, f'Bienvenue {user.full_name} !')
                        
                        # Redirection basée sur le rôle
                        if user.role == ROLES.SUPERUSER:
                            return redirect('admin:index')
                        return redirect('dashboard')
                    else:
                        messages.error(request, 'Votre compte est désactivé.')
                else:
                    messages.error(request, 'Mot de passe incorrect.')
            
            except CustomUser.DoesNotExist:
                messages.error(request, 'Aucun compte trouvé avec ces identifiants.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs du formulaire.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    user_name = request.user.full_name
    logout(request)
    messages.info(request, f'Au revoir {user_name} !')
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            user = form.save(commit=False)
            
            # Vérification des permissions selon le rôle
            if user.role == ROLES.SUPERUSER:
                user.is_staff = True
                user.is_superuser = True
                user.acces_gestion_vehicules = True
                user.acces_maintenance = True
                user.acces_rapports = True
            elif user.role == ROLES.SECRETAIRE:
                user.is_staff = True
                user.is_superuser = False
                user.acces_gestion_vehicules = True
                user.acces_rapports = True
                user.acces_maintenance = False
            else:
                user.is_staff = False
                user.is_superuser = False
                user.acces_gestion_vehicules = False
                user.acces_maintenance = False
                user.acces_rapports = False
            
            user.save()
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
        'duree_service': request.user.get_active_duration()
    }
    return render(request, 'profile.html', context)

def forgot_password(request):
    return render(request, 'forgot-password.html')

# Vues pour les administrateurs
@user_passes_test(lambda u: u.role == ROLES.SUPERUSER)
def user_list_view(request):
    users = CustomUser.objects.all().order_by('-date_enregistrement')
    context = {
        'users': users,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'inactive_users': users.filter(is_active=False).count()
    }
    return render(request, 'user_list.html', context)

@user_passes_test(lambda u: u.role == ROLES.SUPERUSER)
def user_detail_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profil de {user.full_name} mis à jour avec succès!')
            return redirect('user_list')
    else:
        form = CustomUserUpdateForm(instance=user)
    
    context = {
        'user_profile': user,
        'form': form,
        'duree_service': user.get_active_duration()
    }
    return render(request, 'user_detail.html', context)