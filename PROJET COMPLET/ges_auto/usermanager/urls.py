# urls.py
from django.urls import path
from .views import (
    list_users_view,
    create_user,
    update_user,
    delete_user,
    export_users
)

urlpatterns = [
    path('utilisateurs/', list_users_view, name='user_page'),
    path('utilisateurs/create/', create_user, name='create_user'),
    path('utilisateurs/update/<int:user_id>/', update_user, name='update_user'),
    path('utilisateurs/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('utilisateurs/export/<str:format>/', export_users, name='export_users'),
]