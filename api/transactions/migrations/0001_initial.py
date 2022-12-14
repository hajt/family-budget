# Generated by Django 3.2.15 on 2022-08-16 15:35

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wallets", "0002_auto_20220815_1906"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=50)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("bills", "Bills"),
                            ("clothes", "Clothes"),
                            ("entertainment", "Entertainment"),
                            ("food", "Food"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=30,
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[("pln", "Polish złoty")], default="pln", max_length=15
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "amount",
                    models.PositiveSmallIntegerField(
                        help_text="Amount in the smallest, integer currency parts (eg. cents)",
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                ("is_expense", models.BooleanField(default=True)),
                (
                    "wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="wallets.wallet",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
