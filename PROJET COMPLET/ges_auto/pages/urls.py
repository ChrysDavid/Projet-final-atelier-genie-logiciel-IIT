from django.urls import path
from .views import (
    user_page,
    logistics_fleet,
    map_page,
)

urlpatterns = [
    path('user_page', user_page, name="user_page"),
    path('logistics_fleet', logistics_fleet, name="logistics"),
    path('map', map_page, name="map"),
]