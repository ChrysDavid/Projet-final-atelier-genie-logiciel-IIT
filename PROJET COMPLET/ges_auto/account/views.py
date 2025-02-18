from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm, CustomAuthenticationForm
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
    user = request.user
    
    if request.method == 'POST':
        # Validation de la photo
        photo = request.FILES.get('photo_profile')
        if photo:
            if photo.size > 819200:  # 800KB
                messages.error(request, "L'image ne doit pas dépasser 800KB")
                return redirect('profile')
            if not photo.content_type in ['image/jpeg', 'image/png', 'image/gif']:
                messages.error(request, "Seuls les formats JPEG, PNG et GIF sont acceptés")
                return redirect('profile')
            user.photo_profile = photo

        # Mise à jour des champs
        user.nom = request.POST.get('nom', user.nom)
        user.prenom = request.POST.get('prenom', user.prenom)
        user.email = request.POST.get('email', user.email)
        user.fonction = request.POST.get('fonction', user.fonction)
        user.service = request.POST.get('service', user.service)
        user.telephone_pro = request.POST.get('telephone_pro', user.telephone_pro)
        user.telephone_perso = request.POST.get('telephone_perso', user.telephone_perso)
        user.adresse = request.POST.get('adresse', user.adresse)
        user.code_postal = request.POST.get('code_postal', user.code_postal)
        user.ville = request.POST.get('ville', user.ville)

        try:
            user.save()
            messages.success(request, 'Profil mis à jour avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de la mise à jour: {str(e)}')
        
        return redirect('profile')
    
    return render(request, 'profile.html', {'user': user})




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
        # Validation de la photo
        photo = request.FILES.get('photo_profile')
        if photo:
            if photo.size > 819200:  # 800KB
                messages.error(request, "L'image ne doit pas dépasser 800KB")
                return redirect('user_detail', user_id=user_id)
            if not photo.content_type in ['image/jpeg', 'image/png', 'image/gif']:
                messages.error(request, "Seuls les formats JPEG, PNG et GIF sont acceptés")
                return redirect('user_detail', user_id=user_id)
            user.photo_profile = photo

        # Mise à jour des champs
        user.nom = request.POST.get('nom', user.nom)
        user.prenom = request.POST.get('prenom', user.prenom)
        user.email = request.POST.get('email', user.email)
        user.fonction = request.POST.get('fonction', user.fonction)
        user.service = request.POST.get('service', user.service)
        user.telephone_pro = request.POST.get('telephone_pro', user.telephone_pro)
        user.telephone_perso = request.POST.get('telephone_perso', user.telephone_perso)
        user.adresse = request.POST.get('adresse', user.adresse)
        user.code_postal = request.POST.get('code_postal', user.code_postal)
        user.ville = request.POST.get('ville', user.ville)

        try:
            user.save()
            messages.success(request, f'Profil de {user.full_name} mis à jour avec succès!')
            return redirect('user_list')
        except Exception as e:
            messages.error(request, f'Erreur lors de la mise à jour: {str(e)}')
            return redirect('user_detail', user_id=user_id)

    context = {
        'user_profile': user,
        'duree_service': user.get_active_duration()
    }
    return render(request, 'user_detail.html', context)