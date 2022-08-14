from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api.core.models import CommonModel


class User(AbstractUser, CommonModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=30,
        unique=True,
        error_messages={"unique": "A user with that username already exists."},
        validators=[UnicodeUsernameValidator()],
    )

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.username})>"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
