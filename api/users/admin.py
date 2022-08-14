from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "created_at",
        "updated_at",
    )
    search_fields = ("id", "email", "username", "first_name", "last_name")
    ordering = ("username", "email")
    readonly_fields = ("created_at", "updated_at")
