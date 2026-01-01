from django.db import models



class Room(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.IntegerField()
    amenities = models.CharField(max_length=255)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    size = models.IntegerField(help_text="Size in square feet", default=500)
    security_level = models.CharField(max_length=50, default="Standard")

    def __str__(self):
        return self.name



from django.core.exceptions import ValidationError

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="room_images/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    caption = models.CharField(max_length=100, blank=True)
    link_url = models.URLField(blank=True, null=True)

    def get_image_source(self):
        return self.image_url or (self.image.url if self.image else None)

    def clean(self):
        if not self.image and not self.image_url:
            raise ValidationError("Please provide either an image file or an image URL.")
        if self.image and self.image_url:
            raise ValidationError("Please provide only one: image file or image URL.")

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    status = models.CharField(max_length=20, default='pending')
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)  # 1–5 stars
    review = models.TextField(blank=True)


    def save(self, *args, **kwargs):
        if self.check_in and self.check_out and self.room:
            duration = (self.check_out - self.check_in).days
            self.total_price = self.room.price * max(duration, 1)
        super().save(*args, **kwargs)


from django import forms
from .models import Booking

class PrivateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["room", "check_in", "check_out"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }

# booking/models.py

from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.room.name}"
    
from decimal import Decimal

def save(self, *args, **kwargs):
    if self.check_in and self.check_out and self.room:
        duration_seconds = (self.check_out - self.check_in).total_seconds()
        duration_days = Decimal(duration_seconds) / Decimal(86400)  # 86400 seconds in a day
        self.total_price = self.room.price * max(duration_days, Decimal("1.0"))
    super().save(*args, **kwargs)