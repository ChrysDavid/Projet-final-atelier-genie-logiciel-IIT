from django.urls import path
from .views import (
    vehicule_page,
    vehicule_edit,
    vehicule_delete,
    maintenance_list,
    maintenance_edit,
    maintenance_delete,
    carburant_list,
    carburant_edit,
    carburant_delete
)

urlpatterns = [
    path('vehicule/', vehicule_page, name='vehicule'),
    path('vehicule/<int:pk>/edit/', vehicule_edit, name='vehicule_edit'),
    path('vehicule/<int:pk>/delete/', vehicule_delete, name='vehicule_delete'),

    path('maintenance/', maintenance_list, name='maintenance_list'),
    path('maintenance/<int:pk>/edit/', maintenance_edit, name='maintenance_edit'),
    path('maintenance/<int:pk>/delete/', maintenance_delete, name='maintenance_delete'),

    path('carburant/', carburant_list, name='carburant_list'),
    path('carburant/<int:pk>/edit/', carburant_edit, name='carburant_edit'),
    path('carburant/<int:pk>/delete/', carburant_delete, name='carburant_delete'),

]
