from django.contrib import admin

from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "get_participants_display",
    )
    search_fields = ("name", "owner__first_name", "owner__last_name", "owner__username")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
