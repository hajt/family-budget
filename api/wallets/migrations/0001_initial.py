# Generated by Django 3.2.15 on 2022-08-15 15:39

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=30, unique=True)),
                (
                    "currency",
                    models.CharField(
                        choices=[("pln", "Polish złoty")], default="pln", max_length=15
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="own_wallets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        blank=True,
                        related_name="shared_wallets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
