from django.contrib.auth.models import User
from django.db import models
from datetime import date

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('worker', 'Worker'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)


    def __str__(self):
        return f"{self.user.username} ({self.role})"
    

    @property
    def age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None

    def completion_percent(self):
        fields = [self.profile_image, self.dob, self.phone, self.address]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)
