from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Wallet
        fields = ("id", "name", "currency", "owner")
        read_only_fields = ("id", "name", "currency", "owner")


class WalletDetailSerializer(WalletSerializer):
    class Meta:
        model = Wallet
        fields = WalletSerializer.Meta.fields + ("participants",)
        read_only_fields = ("id", "name", "currency", "owner", "participants")


class WalletUpdateSerializer(WalletDetailSerializer):
    class Meta:
        model = Wallet
        fields = WalletDetailSerializer.Meta.fields
        read_only_fields = ("id", "owner")
