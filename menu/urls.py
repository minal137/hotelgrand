from django.urls import path
from . import views

urlpatterns = [
    path("private-menu/", views.private_menu, name="private_menu"),
    path("place-order/", views.place_order, name="place_order"),
]