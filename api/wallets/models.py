from django.db import models

from api.core.models import CommonModel
from api.users.models import User


class Currency(models.TextChoices):
    PLN = "pln", "Polish złoty"


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
