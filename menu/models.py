from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items', null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_time = models.PositiveIntegerField()
    loyalty_points = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.value for r in ratings) / ratings.count(), 1)
        return 0

    def __str__(self):
        return self.name

class Rating(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()  # e.g., 1 to 5

    def __str__(self):
        return f"{self.user.username} rated {self.menu_item.name} → {self.value}"
    


    
from django.db import models
from django.contrib.auth.models import User
from booking.models import Room, Booking
from menu.models import MenuItem  # assuming this exists

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")  # pending, preparing, delivered

    def __str__(self):
        return f"{self.user.username} ordered {self.item.name}"
