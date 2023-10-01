from django.contrib import admin
from .models import Plan, Group


# Register your models here.
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['id',"owner", "title", "time", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["title"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["plan", "user", "created_at"]
