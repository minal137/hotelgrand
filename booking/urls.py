from booking import views as booking_views
from django.urls import path
from booking.views import booking_success, room_detail
from . import views

urlpatterns = [
    path("book/private/", booking_views.private_booking, name="private_booking"),
    path("check/", booking_views.check_availability, name="check_availability"),
    path("booking/success/", booking_success, name="booking_success"),
    path("room/<int:room_id>/", room_detail, name="room_detail"),
    path("extend-booking/", views.extend_booking, name="extend_booking"),
    path("submit-review/", views.submit_review, name="submit_review"),
    ]