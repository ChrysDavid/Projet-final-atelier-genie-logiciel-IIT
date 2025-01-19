from django.urls import path
from . import views

urlpatterns = [
    path('rapport/', views.rapport_list, name='rapport_list'), 
    path('rapport/<int:pk>/edit/', views.rapport_edit, name='rapport_edit'),
    path('rapport/<int:pk>/delete/', views.rapport_delete, name='rapport_delete'),
    path('rapport/export/csv/', views.rapport_export_csv, name='rapport_export_csv'), 
    path('rapport/export/pdf/', views.rapport_export_pdf, name='rapport_export_pdf'),
]
