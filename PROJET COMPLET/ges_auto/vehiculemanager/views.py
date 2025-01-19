from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicule
from .forms import VehiculeForm

def vehicule_page(request):
    """Gère l'affichage de la liste des véhicules et l'ajout."""
    vehicules = Vehicule.objects.all()
    if request.method == "POST":
        form = VehiculeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vehicule')
    else:
        form = VehiculeForm()
    return render(request, 'vehicule.html', {'vehicules': vehicules, 'form': form})



def vehicule_edit(request, pk):
    """Gère la modification d'un véhicule."""
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == "POST":
        form = VehiculeForm(request.POST, request.FILES, instance=vehicule)
        if form.is_valid():
            form.save()
            return redirect('vehicule')
    else:
        form = VehiculeForm(instance=vehicule)
    vehicules = Vehicule.objects.all()
    context = {
        'form': form, 
        'vehicules': vehicules, 
        'editing': True, 
        'edit_pk': pk,
        'show_modal': True  # Ajoutez cette variable
    }
    return render(request, 'vehicule.html', context)


def vehicule_delete(request, pk):
    """Gère la suppression d’un véhicule."""
    vehicule = get_object_or_404(Vehicule, pk=pk)
    vehicule.delete()
    return redirect('vehicule')
