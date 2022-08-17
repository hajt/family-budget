import pytest

from django.urls import reverse

from api.transactions.models import Category, Transaction
from api.wallets.models import Currency
from .factories import TransactionFactory, WalletFactory


@pytest.mark.django_db
def test_transaction_view_get_transaction_owner(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner)
    transaction = TransactionFactory(wallet=wallet)
    expected_response = {
        "id": str(transaction.id),
        "title": transaction.title,
        "category": transaction.category,
        "currency": transaction.currency,
        "date": str(transaction.date),
        "amount": transaction.amount,
        "is_expense": transaction.is_expense,
        "wallet": transaction.wallet.id,
    }

    response = authenticated_api_client.get(
        reverse("transactions:transactions-detail", args=[transaction.id])
    )

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_transaction_view_get_transaction_participant(authenticated_api_client):
    participant = authenticated_api_client.user
    wallet = WalletFactory(participants=[participant])
    transaction = TransactionFactory(wallet=wallet)
    expected_response = {
        "id": str(transaction.id),
        "title": transaction.title,
        "category": transaction.category,
        "currency": transaction.currency,
        "date": str(transaction.date),
        "amount": transaction.amount,
        "is_expense": transaction.is_expense,
        "wallet": transaction.wallet.id,
    }

    response = authenticated_api_client.get(
        reverse("transactions:transactions-detail", args=[transaction.id])
    )

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_transaction_view_get_transaction_no_owner_no_participant(
    authenticated_api_client,
):
    transaction = TransactionFactory()

    response = authenticated_api_client.get(
        reverse("transactions:transactions-detail", args=[transaction.id])
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_transaction_view_patch_transaction_owner(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner)
    transaction = TransactionFactory(wallet=wallet)

    data = {
        "title": "new title",
        "category": Category.OTHER,
        "currency": Currency.PLN,
        "amount": 1000,
    }

    response = authenticated_api_client.patch(
        reverse("transactions:transactions-detail", args=[transaction.id]), data=data
    )

    assert response.status_code == 200
    assert response.data["title"] == "new title"
    assert response.data["category"] == Category.OTHER
    assert response.data["currency"] == Currency.PLN
    assert response.data["amount"] == 1000


@pytest.mark.django_db
def test_transaction_view_patch_transaction_participant(authenticated_api_client):
    participant = authenticated_api_client.user
    wallet = WalletFactory(participants=[participant])
    transaction = TransactionFactory(wallet=wallet)

    data = {
        "title": "new title",
        "category": Category.OTHER,
        "currency": Currency.PLN,
        "amount": 1000,
    }

    response = authenticated_api_client.patch(
        reverse("transactions:transactions-detail", args=[transaction.id]), data=data
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_transaction_view_patch_transaction_no_owner_no_participant(
    authenticated_api_client,
):
    transaction = TransactionFactory()

    data = {
        "title": "new title",
        "category": Category.OTHER,
        "currency": Currency.PLN,
        "amount": 1000,
    }

    response = authenticated_api_client.patch(
        reverse("transactions:transactions-detail", args=[transaction.id]), data=data
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_transaction_view_delete_transaction_owner(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner)
    transaction = TransactionFactory(wallet=wallet)

    response = authenticated_api_client.delete(
        reverse("transactions:transactions-detail", args=[transaction.id])
    )

    assert response.status_code == 204
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_transaction_view_delete_transaction_participant(authenticated_api_client):
    participant = authenticated_api_client.user
    wallet = WalletFactory(participants=[participant])
    transaction = TransactionFactory(wallet=wallet)

    response = authenticated_api_client.delete(
        reverse("transactions:transactions-detail", args=[transaction.id])
    )

    assert response.status_code == 404
    assert Transaction.objects.count() == 1


@pytest.mark.django_db
def test_transaction_view_delete_transaction_no_owner_no_participant(
    authenticated_api_client,
):
    transaction = TransactionFactory()

    response = authenticated_api_client.delete(
        reverse("transactions:transactions-detail", args=[transaction.id])
    )

    assert response.status_code == 404
    assert Transaction.objects.count() == 1
