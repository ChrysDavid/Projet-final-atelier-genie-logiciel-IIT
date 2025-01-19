from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
import json
from .models import Trajet
from .forms import TrajetForm

class TrajetJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Trajet):
            return {
                'id': obj.id,
                'date_depart': obj.date_depart,
                'date_arrivee': obj.date_arrivee,
                'lieu_depart': obj.lieu_depart,
                'destination': obj.destination,
                'distance': obj.distance,
                'motif': obj.motif,
                'status': obj.status,
                'cout_estime': obj.cout_estime,
                'vehicule': str(obj.vehicule),
                'personnel': str(obj.personnel),
                'progress': obj.get_progress(),
                'depart_lat': obj.depart_lat or 48.8566,  # Paris par défaut
                'depart_lon': obj.depart_lon or 2.3522,
                'destination_lat': obj.destination_lat or 48.8566,
                'destination_lon': obj.destination_lon or 2.3522,
            }
        return super().default(obj)

@login_required
def trajet_list(request):
    trajets = Trajet.objects.all()
    form = TrajetForm()
    
    # Sérialiser les trajets pour JavaScript
    trajets_json = json.dumps(list(trajets), cls=TrajetJSONEncoder)
    
    context = {
        'trajets': trajets,
        'form': form,
        'trajets_json': trajets_json
    }
    return render(request, 'trajet.html', context)

@login_required
def trajet_create(request):
    if request.method == 'POST':
        form = TrajetForm(request.POST)
        if form.is_valid():
            trajet = form.save()
            # Mise à jour des coordonnées via l'API Mapbox (à implémenter)
            return JsonResponse({
                'success': True,
                'message': "Trajet créé avec succès",
                'trajet': TrajetJSONEncoder().default(trajet)
            })
        return JsonResponse({
            'success': False,
            'message': "Erreur dans le formulaire",
            'errors': form.errors
        })
    return JsonResponse({'success': False, 'message': "Méthode non autorisée"})

@login_required
def trajet_update(request, pk):
    trajet = get_object_or_404(Trajet, pk=pk)
    if request.method == 'POST':
        form = TrajetForm(request.POST, instance=trajet)
        if form.is_valid():
            trajet = form.save()
            return JsonResponse({
                'success': True,
                'message': "Trajet mis à jour avec succès",
                'trajet': TrajetJSONEncoder().default(trajet)
            })
        return JsonResponse({
            'success': False,
            'message': "Erreur dans le formulaire",
            'errors': form.errors
        })
    return JsonResponse({'success': False, 'message': "Méthode non autorisée"})

@login_required
def trajet_delete(request, pk):
    if request.method == 'POST':
        trajet = get_object_or_404(Trajet, pk=pk)
        trajet.delete()
        return JsonResponse({'success': True, 'message': "Trajet supprimé avec succès"})
    return JsonResponse({'success': False, 'message': "Méthode non autorisée"})