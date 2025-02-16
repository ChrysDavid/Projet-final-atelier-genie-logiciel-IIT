from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from account.models import CustomUser, ROLES
from django.contrib import messages
import csv
import xlsxwriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import secrets
import string
from datetime import datetime



@login_required
def list_users_view(request):
    utilisateurs = CustomUser.objects.filter(role=ROLES.EMPLOYE).order_by('-date_enregistrement')
    
    search_query = request.GET.get('search', '')
    if search_query:
        utilisateurs = utilisateurs.filter(nom__icontains=search_query)
    
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
    if not (request.user.role == ROLES.SUPERUSER or request.user.role == ROLES.SECRETAIRE):
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('user_page')

    try:
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        date_embauche_str = request.POST.get('date_embauche')
        date_embauche = datetime.strptime(date_embauche_str, '%Y-%m-%d').date() if date_embauche_str else None
        
        user = CustomUser(
            username=request.POST.get('email'),
            email=request.POST.get('email'),
            nom=request.POST.get('nom'),
            prenom=request.POST.get('prenom'),
            fonction=request.POST.get('fonction'),
            service=request.POST.get('service'),
            telephone_pro=request.POST.get('telephone_pro'),
            telephone_perso=request.POST.get('telephone_perso'),
            adresse=request.POST.get('adresse'),
            code_postal=request.POST.get('code_postal'),
            ville=request.POST.get('ville'),
            date_embauche=date_embauche,
            role=ROLES.EMPLOYE,
            is_active=True
        )
        
        user.set_password(temp_password)
        user.save()
        
        messages.success(request, f'Employé créé avec succès! Mot de passe temporaire: {temp_password}')
        return redirect('user_page')
        
    except Exception as e:
        messages.error(request, f'Erreur lors de la création: {str(e)}')
        return redirect('user_page')
    




@login_required
@require_http_methods(["POST"])
def update_user(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id, role=ROLES.EMPLOYE)
        
        # Conversion de la date d'embauche
        date_embauche_str = request.POST.get('date_embauche')
        if date_embauche_str:
            date_embauche = datetime.strptime(date_embauche_str, '%Y-%m-%d').date()
        else:
            date_embauche = None
            
        user.nom = request.POST.get('nom', user.nom)
        user.prenom = request.POST.get('prenom', user.prenom)
        user.email = request.POST.get('email', user.email)
        user.username = request.POST.get('email', user.email)
        user.fonction = request.POST.get('fonction', user.fonction)
        user.service = request.POST.get('service', user.service)
        user.telephone_pro = request.POST.get('telephone_pro', user.telephone_pro)
        user.telephone_perso = request.POST.get('telephone_perso', user.telephone_perso)
        user.adresse = request.POST.get('adresse', user.adresse)
        user.code_postal = request.POST.get('code_postal', user.code_postal)
        user.ville = request.POST.get('ville', user.ville)
        user.date_embauche = date_embauche
        
        user.save()
        messages.success(request, 'Employé mis à jour avec succès')
        
    except Exception as e:
        messages.error(request, f'Erreur lors de la mise à jour: {str(e)}')
    
    return redirect('user_page')

@login_required
@require_http_methods(["POST"])
def delete_user(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id, role=ROLES.EMPLOYE)
        user.delete()
        messages.success(request, 'Employé supprimé avec succès')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression: {str(e)}')
    
    return redirect('user_page')





@login_required
def export_users(request, format):
    utilisateurs = CustomUser.objects.filter(role=ROLES.EMPLOYE)
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employes.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Nom', 'Prénom', 'Email', 'Fonction', 'Service',
            'Téléphone Pro', 'Téléphone Perso', 'Adresse',
            'Code Postal', 'Ville', 'Date d\'embauche'
        ])
        
        for user in utilisateurs:
            writer.writerow([
                user.nom,
                user.prenom,
                user.email,
                user.fonction,
                user.service,
                user.telephone_pro,
                user.telephone_perso,
                user.adresse,
                user.code_postal,
                user.ville,
                user.date_embauche
            ])
        
        return response
        
    elif format == 'excel':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        headers = [
            'Nom', 'Prénom', 'Email', 'Fonction', 'Service',
            'Téléphone Pro', 'Téléphone Perso', 'Adresse',
            'Code Postal', 'Ville', 'Date d\'embauche'
        ]
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        
        for row, user in enumerate(utilisateurs, 1):
            worksheet.write(row, 0, user.nom)
            worksheet.write(row, 1, user.prenom)
            worksheet.write(row, 2, user.email)
            worksheet.write(row, 3, user.fonction)
            worksheet.write(row, 4, user.service)
            worksheet.write(row, 5, user.telephone_pro)
            worksheet.write(row, 6, user.telephone_perso)
            worksheet.write(row, 7, user.adresse)
            worksheet.write(row, 8, user.code_postal)
            worksheet.write(row, 9, user.ville)
            worksheet.write(row, 10, str(user.date_embauche) if user.date_embauche else '')
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="employes.xlsx"'
        return response
        
    elif format == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="employes.pdf"'
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        p.drawString(100, 750, "Liste des Employés")
        y = 700
        
        for user in utilisateurs:
            if y < 50:
                p.showPage()
                y = 750
            
            p.drawString(100, y, f"{user.nom} {user.prenom}")
            y -= 20
            p.drawString(120, y, f"Email: {user.email}")
            y -= 20
            p.drawString(120, y, f"Fonction: {user.fonction or 'N/A'}")
            y -= 20
            p.drawString(120, y, f"Service: {user.service or 'N/A'}")
            y -= 40
        
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    
    return HttpResponse('Format non supporté', status=400)