from django.shortcuts import render

# Create your views here.
def index_page(request):
    return render(request, 'index.html')

def user_page(request):
    return render(request, 'tables-datatables-basic.html')

def email_page(request):
    return render(request, 'app-email.html')

def logistics_fleet(request):
    return render(request, 'app-logistics-fleet.html')