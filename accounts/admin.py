from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'age', 'phone', 'address', 'loyalty_points', 'completion_percent')
    readonly_fields = ('age', 'completion_percent')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)