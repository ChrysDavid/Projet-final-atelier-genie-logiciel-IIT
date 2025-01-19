from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from .models import Rapport
from .forms import RapportForm
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas


@login_required
def rapport_list(request):
    rapports = Rapport.objects.all()
    form = RapportForm()
    if request.method == 'POST':
        form = RapportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rapport_list')
    return render(request, 'rapport.html', {'rapports': rapports, 'form': form})


@login_required 
def rapport_edit(request, pk): 
    rapport = get_object_or_404(Rapport, pk=pk) 
    rapports = Rapport.objects.all()  # Ajout de la liste des rapports
    
    if request.method == 'POST': 
        form = RapportForm(request.POST, instance=rapport) 
        if form.is_valid(): 
            form.save() 
            return redirect('rapport_list') 
    else: 
        form = RapportForm(instance=rapport) 
    
    context = {
        'form': form,
        'rapports': rapports,
        'editing': True,
        'edit_pk': pk,
        'show_modal': True  # Pour ouvrir automatiquement le modal
    }
    return render(request, 'rapport.html', context)

@login_required
def rapport_delete(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)
    rapport.delete()
    return redirect('rapport_list')






# Export en CSV
def rapport_export_csv(request):
    rapports = Rapport.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rapports.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Date de création', 'Type', 'Contenu', 'Période', 'Statut'])

    for rapport in rapports:
        writer.writerow([
            rapport.id,
            rapport.date_creation,
            rapport.type,
            rapport.contenu,
            rapport.periode,
            'Archivé' if rapport.archive else 'Actif'
        ])
    
    return response

# Export en PDF
def rapport_export_pdf(request):
    rapports = Rapport.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapports.pdf"'

    pdf_canvas = canvas.Canvas(response)
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(100, 800, "Liste des Rapports")

    y = 750
    for rapport in rapports:
        pdf_canvas.drawString(50, y, f"ID: {rapport.id} | Type: {rapport.type} | Période: {rapport.periode} | Statut: {'Archivé' if rapport.archive else 'Actif'}")
        y -= 20

        if y < 50:  # Nouvelle page si l'espace est insuffisant
            pdf_canvas.showPage()
            pdf_canvas.setFont("Helvetica", 12)
            y = 750

    pdf_canvas.save()
    return response
