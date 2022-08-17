import pytest

from ..serializers import (
    TransactionGroupedSerializer,
    TransactionListSerializer,
    TransactionSerializer,
)
from .factories import Transaction, TransactionFactory


@pytest.mark.django_db
def test_transaction_deserialization():
    transaction = TransactionFactory()
    serializer = TransactionSerializer(transaction)
    assert serializer.data["id"] == str(transaction.id)
    assert serializer.data["title"] == transaction.title
    assert serializer.data["category"] == transaction.category
    assert serializer.data["currency"] == transaction.currency
    assert serializer.data["date"] == str(transaction.date)
    assert serializer.data["amount"] == transaction.amount
    assert serializer.data["is_expense"] == transaction.is_expense
    assert serializer.data["wallet"] == transaction.wallet.id


@pytest.mark.django_db
def test_transaction_list_deserialization():
    transaction = TransactionFactory()
    serializer = TransactionListSerializer(transaction)
    assert serializer.data["id"] == str(transaction.id)
    assert serializer.data["title"] == transaction.title
    assert serializer.data["currency"] == transaction.currency
    assert serializer.data["date"] == str(transaction.date)
    assert serializer.data["amount"] == transaction.amount


@pytest.mark.django_db
def test_transaction_grouped_deserialization_queryset():
    transaction = TransactionFactory()
    category = transaction.category
    serializer = TransactionGroupedSerializer(Transaction.objects.all())

    assert (
        serializer.data[category]
        == TransactionListSerializer([transaction], many=True).data
    )


@pytest.mark.django_db
def test_transaction_grouped_deserialization_single_instance():
    transaction = TransactionFactory()
    category = transaction.category
    serializer = TransactionGroupedSerializer(transaction)

    assert (
        serializer.data[category]
        == TransactionListSerializer([transaction], many=True).data
    )
