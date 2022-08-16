from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("name", "wallet", "category", "date", "is_expense", "currency")
    list_filter = ("category", "wallet", "is_expense", "date", "currency")
    search_fields = ("id", "wallet__owner__username")
    ordering = ("date",)
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("wallet", "wallet__owner")
