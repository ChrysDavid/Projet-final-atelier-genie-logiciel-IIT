# urls.py
from django.urls import path
from .views import (
    login_view,
    logout_view,
    # register_view,
    profile_view,
    forgot_password
)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('forgot_password', forgot_password, name="forgot_password"),

]