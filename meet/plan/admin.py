from django.contrib import admin
from .models import Plan, Group, Comment, Category


# Register your models here.
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "title", "time", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["title"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["plan", "user", "created_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["message", "user", "plan", "created_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}
