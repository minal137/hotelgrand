from django.shortcuts import render
from menu.models import MenuItem, Category
from booking.models import Room

def home(request):
    return render(request, 'public/home.html')

def about(request):
    return render(request, 'public/about.html')

def public_booking(request):
    return render(request, 'public/public_booking.html')

from django.core.paginator import Paginator

def public_menu(request):
    items = MenuItem.objects.all()
    paginator = Paginator(items, 3)  # Show 9 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.prefetch_related('items').all()

    context = {
        'page_obj': page_obj,
        'categories': categories
    }
    return render(request, 'public/public_menu.html', context)


def public_booking(request):
    rooms = Room.objects.all()
    print("Rooms in DB:", rooms.count())
    paginator = Paginator(rooms, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'public/public_booking.html', context)


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect



