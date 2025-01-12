from django.urls import path
from .views import (
    index_page,
    user_page,
    email_page,
    logistics_fleet
)

urlpatterns = [
    path('', index_page, name="index"),
    path('user_page', user_page, name="user_page"),
    path('email', email_page, name="email"),
    path('logistics_fleet', logistics_fleet, name="logistics"),
]