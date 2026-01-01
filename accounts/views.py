# accounts/views.py
import os
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already taken'})
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already registered'})


        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.create(user=user, role='customer')  

        return JsonResponse({'success': True})
    


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password'})





@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts_customer_dashboard')  # or wherever you want
    else:
        form = ProfileEditForm(initial={
            'username': request.user.username,
            'profile_image': profile.profile_image
        }, instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@csrf_exempt
@login_required
def update_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            return JsonResponse({'success': False, 'error': 'Username already taken'})
        request.user.username = new_username
        request.user.save()
        return JsonResponse({'success': True})


@csrf_exempt
@login_required
def update_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            return JsonResponse({'success': False, 'error': 'Email already registered'})
        request.user.email = new_email
        request.user.save()
        return JsonResponse({'success': True})

@csrf_exempt
@login_required
def update_photo(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile = request.user.userprofile

        # Delete old image if it exists and isn't the default
        if profile.profile_image and profile.profile_image.name != 'images/default-avatar.png':
            old_path = os.path.join(settings.MEDIA_ROOT, profile.profile_image.name)
            if os.path.isfile(old_path):
                os.remove(old_path)

        # Save new image
        profile.profile_image = request.FILES['profile_image']
        profile.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'No image uploaded'})





from django.contrib.auth import update_session_auth_hash

@csrf_exempt
@login_required
def update_password(request):
    if request.method == 'POST':
        old = request.POST.get('old_password')
        new1 = request.POST.get('new_password1')
        new2 = request.POST.get('new_password2')

        if not request.user.check_password(old):
            return JsonResponse({'success': False, 'error': 'Incorrect current password'})

        if new1 != new2:
            return JsonResponse({'success': False, 'error': 'New passwords do not match'})

        request.user.set_password(new1)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return JsonResponse({'success': True})
    


@csrf_exempt
@login_required
def update_details(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if dob:
            profile.dob = dob
        profile.phone = phone
        profile.address = address
        profile.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
