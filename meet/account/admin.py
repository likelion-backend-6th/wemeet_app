from django.contrib import admin
from .models import UserLocation


# Register your models here.
@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ['id',"user", "longitude", "latitude", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user"]