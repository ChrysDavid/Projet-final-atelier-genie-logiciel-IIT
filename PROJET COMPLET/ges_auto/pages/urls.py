from django.urls import path
from .views import (
    user_page,
    logistics_fleet,
    # vehicule_page,
    maintenance_page,
    carburant_page,
    raport_page,
    account_page,
    map_page,
    forgot_password
)

urlpatterns = [
    path('user_page', user_page, name="user_page"),
    path('logistics_fleet', logistics_fleet, name="logistics"),
    # path('vehicule', vehicule_page, name="vehicule"),
    path('maintenance', maintenance_page, name="maintenance"),
    path('carburant', carburant_page, name="carburant"),
    path('raport', raport_page, name="raport"),
    path('account', account_page, name="account"),
    path('forgot_password', forgot_password, name="forgot_password"),
    path('map', map_page, name="map"),
]