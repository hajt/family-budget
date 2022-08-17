from django.core.validators import MinValueValidator
from django.db import models

from api.core.models import CommonModel
from api.wallets.models import Currency, Wallet


class Category(models.TextChoices):
    BILLS = "bills", "Bills"
    CLOTHES = "clothes", "Clothes"
    ENTERTAINMENT = "entertainment", "Entertainment"
    FOOD = "food", "Food"
    OTHER = "other", "Other"


class Transaction(CommonModel):
    title = models.CharField(max_length=50)
    category = models.CharField(
        max_length=30, choices=Category.choices, default=Category.OTHER
    )
    currency = models.CharField(
        max_length=15, choices=Currency.choices, default=Currency.PLN
    )
    date = models.DateField(auto_now_add=True)
    amount = models.PositiveIntegerField(
        help_text="Amount in the smallest, integer currency parts (eg. cents)",
        validators=[MinValueValidator(1)],
    )
    is_expense = models.BooleanField(default=True)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )

    @property
    def amount_decimal(self):
        amount = f"{self.amount/100:.2f}"
        return f"-{amount}" if self.is_expense else amount

    @property
    def name(self):
        return f"{self.title} = {self.amount_decimal}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.name})>"

    def __str__(self) -> str:
        return f"{self.name} | {self.wallet}"
