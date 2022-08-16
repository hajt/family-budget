from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    balance = serializers.SerializerMethodField("get_balance")

    class Meta:
        model = Wallet
        fields = ("id", "name", "currency", "owner", "balance")
        read_only_fields = ("id", "name", "currency", "owner", "balance")

    def get_balance(self, obj):
        return f"{obj.balance/100:.2f}"


class WalletDetailSerializer(WalletSerializer):
    expenses = serializers.SerializerMethodField("get_expenses")
    income = serializers.SerializerMethodField("get_income")

    class Meta:
        model = Wallet
        fields = WalletSerializer.Meta.fields + ("income", "expenses", "participants")
        read_only_fields = (
            "id",
            "name",
            "currency",
            "owner",
            "balance",
            "income",
            "expenses",
            "participants",
        )

    def get_expenses(self, obj):
        return f"-{obj.expenses/100:.2f}"

    def get_income(self, obj):
        return f"{obj.income/100:.2f}"


class WalletUpdateSerializer(WalletDetailSerializer):
    class Meta:
        model = Wallet
        fields = WalletDetailSerializer.Meta.fields
        read_only_fields = ("id", "owner", "balance", "income", "expenses")
