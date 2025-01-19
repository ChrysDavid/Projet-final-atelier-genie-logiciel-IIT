from django.shortcuts import render

# Create your views here.

def user_page(request):
    return render(request, 'user.html')

def logistics_fleet(request):
    return render(request, 'trajet.html')







def map_page(request):
    return render(request, 'map.html')

