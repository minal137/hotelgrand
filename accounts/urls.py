# accounts/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('update/username/', views.update_username, name='update_username'),
    path('update/email/', views.update_email, name='update_email'),
    path('update/photo/', views.update_photo, name='update_photo'),
    path('update/password/', views.update_password, name='update_password'),
    path('update/details/', views.update_details, name='update_details'),

]