from django.shortcuts import render

# Create your views here.

def user_page(request):
    return render(request, 'user.html')

def logistics_fleet(request):
    return render(request, 'trajet.html')

# def vehicule_page(request):
#     return render(request, 'vehicule.html')

def maintenance_page(request):
    return render(request, 'maintenance.html')

def carburant_page(request):
    return render(request, 'carburant.html')

def raport_page(request):
    return render(request, 'raport.html')

def account_page(request):
    return render(request, 'account.html')

def map_page(request):
    return render(request, 'map.html')

def forgot_password(request):
    return render(request, 'forgot-password.html')