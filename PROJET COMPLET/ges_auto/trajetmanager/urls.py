# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('trajet/', views.trajet_list, name='trajet_list'),
    path('trajet/create/', views.trajet_create, name='trajet_create'),
    path('trajet/update/<int:pk>/', views.trajet_update, name='trajet_update'),
    path('trajet/delete/<int:pk>/', views.trajet_delete, name='trajet_delete'),
]