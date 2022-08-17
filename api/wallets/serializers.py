from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Wallet
        fields = ("id", "name", "currency", "owner", "balance")
        read_only_fields = ("id", "name", "currency", "owner", "balance")


class WalletDetailSerializer(WalletSerializer):
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


class WalletUpdateSerializer(WalletDetailSerializer):
    class Meta:
        model = Wallet
        fields = WalletDetailSerializer.Meta.fields
        read_only_fields = ("id", "owner", "balance", "income", "expenses")
