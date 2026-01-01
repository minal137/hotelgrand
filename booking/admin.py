from django.contrib import admin
from .models import Room, Booking, RoomImage

# Inline image uploader for Room
class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    fields = ["image", "image_url", "caption", "link_url"]  # ✅ Use image_url

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]
    list_display = ["name", "price", "capacity","bedrooms", "bathrooms", "size", "security_level"]
    search_fields = ["name", "amenities"]
    list_filter = ["capacity", "bedrooms", "bathrooms", "security_level"]
    fields = [
        "name", "price", "capacity", "bedrooms", "bathrooms",
        "size", "security_level", "amenities", "image", "image_url", "description"
    ]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["guest_name", "room", "check_in", "check_out", "status", "total_price"]
    list_filter = ["status", "check_in", "room"]
    search_fields = ["guest_name", "room__name"]
    readonly_fields = ["total_price"]
    actions = ["mark_as_checked_in"]

    def mark_as_checked_in(self, request, queryset):
        updated = queryset.update(status="checked_in")
        self.message_user(request, f"{updated} booking(s) marked as checked in.")
    mark_as_checked_in.short_description = "✅ Mark selected bookings as checked in"
