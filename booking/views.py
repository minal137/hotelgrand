from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime

from booking.models import Room, Booking, Review
from .forms import PrivateBookingForm, AvailabilityForm

import logging
logger = logging.getLogger(__name__)

# -------------------------------
# ⏳ Expire Old Bookings
# -------------------------------
def expire_old_bookings():
    expired = Booking.objects.filter(
        check_out__lt=timezone.now(),
        status="confirmed"
    )
    for booking in expired:
        booking.status = "completed"
        booking.save()

# -------------------------------
# 📄 Public Booking Form
# -------------------------------
def booking_form(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'public/booking_form.html', {'room': room})

# -------------------------------
# 🔒 Private Booking View
# -------------------------------
@login_required
def private_booking(request):
    expire_old_bookings()

    if request.method == "POST":
        room_id = request.POST.get("room_id")
        room = get_object_or_404(Room, id=room_id)
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        guest_count = int(request.POST.get("guest_count", 1))
        special_requests = request.POST.get("special_requests", "")

        check_in_date = datetime.strptime(check_in, "%Y-%m-%dT%H:%M")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%dT%H:%M")

        if check_out_date <= check_in_date:
            messages.error(request, "❌ Check-out must be after check-in.")
            return redirect(request.META.get("HTTP_REFERER", "private_booking"))

        conflict = Booking.objects.filter(
            room=room,
            check_in__lt=check_out_date,
            check_out__gt=check_in_date,
            status="confirmed"
        )
        if conflict.exists():
            messages.error(request, "❌ This room is already booked for the selected dates.")
            return redirect(request.META.get("HTTP_REFERER", "private_booking"))

        booking = Booking.objects.create(
            room=room,
            guest_name=request.user.username,
            check_in=check_in_date,
            check_out=check_out_date,
            special_requests=special_requests,
            status="confirmed"
        )
        booking.total_price = room.price * guest_count
        booking.save()

        return redirect("booking_success")

    form = AvailabilityForm(request.POST or None)
    available_rooms = Room.objects.all()

    if request.method == "POST":
        if "clear" in request.POST:
            form = AvailabilityForm()
            available_rooms = Room.objects.all()
        elif form.is_valid():
            check_in = form.cleaned_data["check_in"]
            check_out = form.cleaned_data["check_out"]

            filtered_rooms = []
            for room in Room.objects.all():
                overlapping = Booking.objects.filter(
                    room=room,
                    check_in__lt=check_out,
                    check_out__gt=check_in,
                    status="confirmed"
                )
                if not overlapping.exists():
                    filtered_rooms.append(room)

            available_rooms = filtered_rooms

    paginator = Paginator(available_rooms, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "customer/private_booking.html", {
        "form": form,
        "page_obj": page_obj,
        "available_rooms": available_rooms
    })

# -------------------------------
# 📅 Availability Check
# -------------------------------
def check_availability(request):
    expire_old_bookings()

    form = AvailabilityForm(request.POST or None)
    available_rooms = Room.objects.all()

    if request.method == "POST":
        if "clear" in request.POST:
            form = AvailabilityForm()
            available_rooms = Room.objects.all()
        elif form.is_valid():
            check_in = form.cleaned_data["check_in"]
            check_out = form.cleaned_data["check_out"]

            filtered_rooms = []
            for room in Room.objects.all():
                overlapping = Booking.objects.filter(
                    room=room,
                    check_in__lt=check_out,
                    check_out__gt=check_in,
                    status="confirmed"
                )
                if not overlapping.exists():
                    filtered_rooms.append(room)

            available_rooms = filtered_rooms

    return render(request, "customer/check_availability.html", {
        "form": form,
        "available_rooms": available_rooms
    })

# -------------------------------
# ✅ Booking Success Redirect
# -------------------------------
def booking_success(request):
    messages.success(request, "✅ Booking confirmed!")
    return redirect("home")

# -------------------------------
# 🏨 Room Detail View
# -------------------------------
def room_detail(request, room_id):
    expire_old_bookings()

    room = get_object_or_404(Room, id=room_id)
    reviews = Review.objects.filter(room=room).order_by("-created_at")[:5]

    existing_booking = Booking.objects.filter(
        room=room,
        guest_name=request.user.username,
        status__in=["confirmed", "checked_in"]
    ).order_by("-check_out").first()

    return render(request, "customer/room_detail.html", {
        "room": room,
        "reviews": reviews,
        "existing_booking": existing_booking,
    })

# -------------------------------
# ⏱️ Extend Booking View
# -------------------------------
def extend_booking(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        new_check_out = request.POST.get("new_check_out")

        print("🔍 booking_id:", booking_id)
        print("🔍 new_check_out:", new_check_out)

        if not booking_id or not new_check_out:
            messages.error(request, "❌ Missing booking ID or new checkout time.")
            return redirect("room_detail", room_id=booking_id)

        try:
            booking = get_object_or_404(Booking, id=booking_id, guest_name=request.user.username)
            room = booking.room

            new_checkout_dt = parse_datetime(new_check_out)
            if not new_checkout_dt:
                new_checkout_dt = datetime.strptime(new_check_out, "%Y-%m-%dT%H:%M")

            new_checkout_dt = timezone.make_aware(new_checkout_dt)

            print("✅ Parsed new_checkout_dt:", new_checkout_dt)

            if new_checkout_dt <= booking.check_out:
                messages.error(request, "❌ Extension must be after current checkout.")
                return redirect("room_detail", room_id=room.id)

            conflict = Booking.objects.filter(
                room=room,
                check_in__lt=new_checkout_dt,
                check_out__gt=booking.check_out,
                status="confirmed"
            ).exclude(id=booking.id)

            if conflict.exists():
                messages.error(request, "❌ Room is not available for that extension.")
            else:
                booking.check_out = new_checkout_dt
                booking.save()
                messages.success(request, "✅ Booking extended successfully.")

        except Exception as e:
            print("🔴 Extension error:", e)
            messages.error(request, "❌ Could not process extension.")

        return redirect("room_detail", room_id=room.id)

# -------------------------------
# ✍️ Review Booking View
# -------------------------------
@login_required
def submit_review(request):
    if request.method == "POST":
        room_id = request.POST.get("room_id")
        text = request.POST.get("text")
        room = get_object_or_404(Room, id=room_id)

        booking = Booking.objects.filter(
            room=room,
            guest_name=request.user.username,
            status="checked_in"
        ).first()

        if not booking:
            messages.error(request, "❌ You must check in before reviewing.")
            return redirect("room_detail", room_id=room.id)

        Review.objects.create(
            room=room,
            user=request.user,
            text=text
        )
        messages.success(request, "✅ Review submitted!")
        return redirect("room_detail", room_id=room.id)