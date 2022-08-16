from django.db import models
from django.db.models import F, OuterRef, Subquery
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce

from api.core.models import CommonModel
from api.users.models import User


class Currency(models.TextChoices):
    PLN = "pln", "Polish złoty"


class WalletManager(models.Manager):
    def get_queryset(self):
        from api.transactions.models import Transaction

        expenses_subquery = (
            Transaction.objects.filter(wallet_id=OuterRef("id"), is_expense=True)
            .values("wallet_id")
            .annotate(total_expenses=Sum("amount"))
            .values("total_expenses")
        )
        income_subquery = (
            Transaction.objects.filter(wallet_id=OuterRef("id"), is_expense=False)
            .values("wallet_id")
            .annotate(total_income=Sum("amount"))
            .values("total_income")
        )

        return (
            super()
            .get_queryset()
            .annotate(
                expenses=Coalesce(Subquery(expenses_subquery), 0),
                income=Coalesce(Subquery(income_subquery), 0),
                balance=F("income") - F("expenses"),
            )
        )


class Wallet(CommonModel):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="own_wallets"
    )
    participants = models.ManyToManyField(
        User, blank=True, related_name="shared_wallets"
    )
    currency = models.CharField(
        max_length=15, choices=Currency.choices, default=Currency.PLN
    )

    objects = WalletManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "owner"], name="unique_name_owner")
        ]

    def get_participants_display(self):
        return ", ".join([str(participant) for participant in self.participants.all()])

    get_participants_display.short_description = "Shared with"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.name})>"

    def __str__(self) -> str:
        return f"{self.name} | {self.owner}"
