from django.contrib import admin
from .models import MenuItem, Rating

class MenuItemAdmin(admin.ModelAdmin):
    readonly_fields = ['average_rating']  
    
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Rating)