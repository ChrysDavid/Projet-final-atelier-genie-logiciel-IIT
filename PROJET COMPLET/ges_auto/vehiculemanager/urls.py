from django.urls import path
from . import views

urlpatterns = [
    path('vehicule/', views.vehicule_page, name='vehicule'),
    path('vehicule/<int:pk>/edit/', views.vehicule_edit, name='vehicule_edit'),
    path('vehicule/<int:pk>/delete/', views.vehicule_delete, name='vehicule_delete'),
]
