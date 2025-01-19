# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from account.models import CustomUser
from django.core.paginator import Paginator
import csv
import xlsxwriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.core.exceptions import ValidationError
import json

@login_required
def list_users_view(request):
    search_query = request.GET.get('search', '')
    utilisateurs = CustomUser.objects.filter(
        nom__icontains=search_query
    ).order_by('-date_enregistrement')
    
    paginator = Paginator(utilisateurs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'user.html', {
        'utilisateurs': page_obj,
        'page_obj': page_obj,
        'search_query': search_query
    })


@login_required
@require_http_methods(["POST"])
def create_user(request):
    try:
        data = json.loads(request.body) if request.body else request.POST
        
        user = CustomUser.objects.create(
            matricule=data.get('matricule'),
            username=data.get('email'),  # Utiliser l'email comme nom d'utilisateur
            email=data.get('email'),
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            fonction=data.get('fonction'),
            adresse=data.get('adresse'),
            date_embauche=data.get('date_embauche')
        )
        
        # Définir un mot de passe temporaire
        temp_password = CustomUser.objects.make_random_password()
        user.set_password(temp_password)
        user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Utilisateur créé avec succès',
            'temp_password': temp_password
        })
    except ValidationError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
@require_http_methods(["POST"])
def update_user(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        data = json.loads(request.body) if request.body else request.POST
        
        user.matricule = data.get('matricule', user.matricule)
        user.nom = data.get('nom', user.nom)
        user.prenom = data.get('prenom', user.prenom)
        user.email = data.get('email', user.email)
        user.fonction = data.get('fonction', user.fonction)
        user.adresse = data.get('adresse', user.adresse)
        user.date_embauche = data.get('date_embauche', user.date_embauche)
        
        user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Utilisateur mis à jour avec succès'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["POST"])
def delete_user(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Utilisateur supprimé avec succès'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def export_users(request, format):
    utilisateurs = CustomUser.objects.all()
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="utilisateurs.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Matricule', 'Nom', 'Prénom', 'Email', 'Fonction', 'Date d\'embauche'])
        
        for user in utilisateurs:
            writer.writerow([
                user.matricule,
                user.nom,
                user.prenom,
                user.email,
                user.fonction,
                user.date_embauche
            ])
        
        return response
        
    elif format == 'excel':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # En-têtes
        headers = ['Matricule', 'Nom', 'Prénom', 'Email', 'Fonction', 'Date d\'embauche']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        
        # Données
        for row, user in enumerate(utilisateurs, 1):
            worksheet.write(row, 0, user.matricule)
            worksheet.write(row, 1, user.nom)
            worksheet.write(row, 2, user.prenom)
            worksheet.write(row, 3, user.email)
            worksheet.write(row, 4, user.fonction)
            worksheet.write(row, 5, str(user.date_embauche))
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="utilisateurs.xlsx"'
        return response
        
    elif format == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="utilisateurs.pdf"'
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # En-tête
        p.drawString(100, 750, "Liste des Utilisateurs")
        y = 700
        
        for user in utilisateurs:
            if y < 50:  # Nouvelle page si plus d'espace
                p.showPage()
                y = 750
            
            p.drawString(100, y, f"{user.matricule} - {user.nom} {user.prenom}")
            y -= 20
            p.drawString(120, y, f"Email: {user.email}")
            y -= 20
            p.drawString(120, y, f"Fonction: {user.fonction or 'N/A'}")
            y -= 40
        
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    
    return JsonResponse({'error': 'Format non supporté'}, status=400)