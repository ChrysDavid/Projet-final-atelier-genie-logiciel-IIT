from django.urls import path
from .views import (
    login_view,
    logout_view,
    profile_view,
    forgot_password,
    user_list_view,
    user_detail_view
)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('users/', user_list_view, name='user_list'),
    path('users/<int:user_id>/', user_detail_view, name='user_detail'),
]