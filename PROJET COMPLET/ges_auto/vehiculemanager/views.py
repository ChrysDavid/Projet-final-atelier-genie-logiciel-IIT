from django.shortcuts import render, get_object_or_404, redirect
from .models import Maintenance, Vehicule, Carburant
from .forms import MaintenanceForm, VehiculeForm, CarburantForm



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






def maintenance_list(request):
    """Afficher la liste des maintenances et gérer l'ajout/modification."""
    maintenances = Maintenance.objects.all()
    if request.method == "POST":
        form = MaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()
    return render(request, 'maintenance.html', {'maintenances': maintenances, 'form': form})

def maintenance_edit(request, pk):
    """Modifier une maintenance existante."""
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == "POST":
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm(instance=maintenance)
    maintenances = Maintenance.objects.all()
    context = {
        'form': form,
        'maintenances': maintenances,
        'editing': True,
        'edit_pk': pk,
        'show_modal': True  # Pour ouvrir automatiquement le modal
    }
    return render(request, 'maintenance.html', context)

def maintenance_delete(request, pk):
    """Supprimer une maintenance existante."""
    maintenance = get_object_or_404(Maintenance, pk=pk)
    maintenance.delete()
    return redirect('maintenance_list')





def carburant_list(request):
    """Affiche la liste des entrées de carburant et gère l'ajout."""
    carburants = Carburant.objects.select_related('vehicule').all()
    if request.method == "POST":
        form = CarburantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('carburant_list')
    else:
        form = CarburantForm()
    return render(request, 'carburant.html', {'carburants': carburants, 'form': form})


def carburant_edit(request, pk):
    """Modifie une entrée de carburant."""
    carburant = get_object_or_404(Carburant, pk=pk)
    if request.method == "POST":
        form = CarburantForm(request.POST, instance=carburant)
        if form.is_valid():
            form.save()
            return redirect('carburant_list')
    else:
        form = CarburantForm(instance=carburant)
    carburants = Carburant.objects.select_related('vehicule').all()
    context = {
        'form': form,
        'carburants': carburants,
        'editing': True,
        'edit_pk': pk,
        'show_modal': True  # Pour ouvrir automatiquement le modal
    }
    return render(request, 'carburant.html', context)




def carburant_delete(request, pk):
    """Supprime une entrée de carburant."""
    carburant = get_object_or_404(Carburant, pk=pk)
    carburant.delete()
    return redirect('carburant_list')
