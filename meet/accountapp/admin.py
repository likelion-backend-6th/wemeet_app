from django.contrib import admin
from .models import UserLocation, Profile


# Register your models here.
@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "longitude", "latitude", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "message", "photo"]
