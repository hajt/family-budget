from rest_framework import serializers

from .models import Category, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "title",
            "category",
            "currency",
            "date",
            "amount",
            "is_expense",
            "wallet",
        )
        read_only_fields = ("id", "date", "is_expense", "wallet")


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "title", "currency", "date", "amount")
        read_only_fields = ("id", "title", "currency", "date", "amount")


class TransactionGroupedSerializer(serializers.Serializer):
    def to_representation(self, data):
        return {
            category[0]: TransactionListSerializer(
                instance=data.filter(category=category[0]), many=True
            ).data
            for category in Category.choices
        }
