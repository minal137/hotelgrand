from django.shortcuts import render, get_object_or_404, redirect
from booking.models import Booking
from menu.models import MenuItem, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def private_menu(request):
    booking = Booking.objects.filter(
        guest_name=request.user.username,
        status="checked_in"
    ).order_by("-check_in").first()

    if not booking:
        messages.error(request, "❌ You must be checked in to access the private menu.")
        return redirect("home")

    items = MenuItem.objects.all()
    return render(request, "customer/private_menu.html", {
        "items": items,
        "booking": booking
    })

@login_required
def place_order(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = int(request.POST.get("quantity", 1))
        booking = Booking.objects.filter(
            guest_name=request.user.username,
            status="checked_in"
        ).order_by("-check_in").first()

        if not booking:
            messages.error(request, "❌ You must be checked in to place an order.")
            return redirect("private_menu")

        item = get_object_or_404(MenuItem, id=item_id)
        Order.objects.create(user=request.user, booking=booking, item=item, quantity=quantity)
        messages.success(request, f"✅ Ordered {item.name} successfully!")
        return redirect("private_menu")