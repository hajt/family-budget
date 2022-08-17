import json

import pytest

from django.urls import reverse
from django.utils.timezone import now

from api.transactions.models import Category, Transaction
from api.transactions.serializers import TransactionListSerializer
from api.transactions.tests.factories import TransactionFactory
from api.users.tests.factories import UserFactory
from api.wallets.exceptions import NotOwnerError
from ..models import Currency, Wallet
from .factories import WalletFactory


@pytest.mark.django_db
def test_wallet_view_get_list_wallets(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner)

    expected_response = json.dumps(
        [
            {
                "id": str(wallet.id),
                "name": wallet.name,
                "currency": wallet.currency,
                "owner": str(wallet.owner),
                "balance": wallet.balance,
            }
        ]
    )

    response = authenticated_api_client.get(reverse("wallets:wallets-list"))
    response_data = json.dumps(response.data["results"])

    assert response.status_code == 200
    assert response_data == expected_response


@pytest.mark.django_db
def test_wallet_view_get_list_no_wallets(authenticated_api_client):
    response = authenticated_api_client.get(reverse("wallets:wallets-list"))

    assert response.status_code == 200
    assert response.data["results"] == []


@pytest.mark.django_db
def test_wallet_view_get_list_no_owner_wallet(authenticated_api_client):
    WalletFactory()

    response = authenticated_api_client.get(reverse("wallets:wallets-list"))

    assert response.status_code == 200
    assert response.data["results"] == []


@pytest.mark.django_db
def test_wallet_view_get_shared_wallets(authenticated_api_client):
    participant = authenticated_api_client.user
    wallet = WalletFactory(participants=[participant])

    expected_response = json.dumps(
        [
            {
                "id": str(wallet.id),
                "name": wallet.name,
                "currency": wallet.currency,
                "owner": str(wallet.owner),
                "balance": wallet.balance,
            }
        ]
    )

    response = authenticated_api_client.get(reverse("wallets:wallets-shared"))
    response_data = json.dumps(response.data["results"])

    assert response.status_code == 200
    assert response_data == expected_response


@pytest.mark.django_db
def test_wallet_view_get_shared_wallets_no_participant(authenticated_api_client):
    WalletFactory(participants=[UserFactory()])

    response = authenticated_api_client.get(reverse("wallets:wallets-shared"))

    assert response.status_code == 200
    assert response.data["results"] == []


@pytest.mark.django_db
def test_wallet_view_get_wallet_owner(authenticated_api_client):
    owner = authenticated_api_client.user
    participant = UserFactory()
    wallet = WalletFactory(owner=owner, participants=[participant])
    expected_response = {
        "id": str(wallet.id),
        "name": wallet.name,
        "currency": wallet.currency,
        "owner": str(wallet.owner),
        "balance": wallet.balance,
        "income": wallet.income,
        "expenses": wallet.expenses,
        "participants": [participant.id],
    }

    response = authenticated_api_client.get(
        reverse("wallets:wallets-detail", args=[wallet.id])
    )

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_wallet_view_get_wallet_participant(authenticated_api_client):
    owner = UserFactory()
    participant = authenticated_api_client.user
    wallet = WalletFactory(owner=owner, participants=[participant])
    expected_response = {
        "id": str(wallet.id),
        "name": wallet.name,
        "currency": wallet.currency,
        "owner": str(wallet.owner),
        "balance": wallet.balance,
        "income": wallet.income,
        "expenses": wallet.expenses,
        "participants": [participant.id],
    }

    response = authenticated_api_client.get(
        reverse("wallets:wallets-detail", args=[wallet.id])
    )

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_wallet_view_get_wallet_no_owner_no_participant(authenticated_api_client):
    wallet = WalletFactory(participants=[UserFactory()])

    response = authenticated_api_client.get(
        reverse("wallets:wallets-detail", args=[wallet.id])
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_wallet_view_post_wallet(authenticated_api_client):
    owner = authenticated_api_client.user
    participant = UserFactory()

    data = {
        "name": "test wallet",
        "currency": Currency.PLN,
        "participants": [str(participant.id)],
    }

    response = authenticated_api_client.post(reverse("wallets:wallets-list"), data=data)

    assert response.status_code == 201
    assert response.data["name"] == "test wallet"
    assert response.data["currency"] == Currency.PLN
    assert response.data["owner"] == str(owner)
    assert response.data["participants"] == [participant.id]


@pytest.mark.django_db
def test_wallet_view_patch_wallet(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner, participants=[UserFactory()])

    participant = UserFactory()
    data = {"name": "new name", "participants": [str(participant.id)]}

    response = authenticated_api_client.patch(
        reverse("wallets:wallets-detail", args=[wallet.id]), data=data
    )

    assert response.status_code == 200
    assert response.data["name"] == "new name"
    assert response.data["currency"] == Currency.PLN
    assert response.data["owner"] == str(owner)
    assert response.data["participants"] == [participant.id]


@pytest.mark.django_db
def test_wallet_view_patch_wallet_no_owner(authenticated_api_client):
    wallet = WalletFactory(participants=[UserFactory()])

    participant = UserFactory()
    data = {"name": "new name", "participants": [str(participant.id)]}

    response = authenticated_api_client.patch(
        reverse("wallets:wallets-detail", args=[wallet.id]), data=data
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_wallet_view_delete_wallet(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner)

    response = authenticated_api_client.delete(
        reverse("wallets:wallets-detail", args=[wallet.id])
    )

    assert response.status_code == 204
    assert Wallet.objects.count() == 0


@pytest.mark.django_db
def test_wallet_view_delete_wallet_no_owner(authenticated_api_client):
    wallet = WalletFactory()

    response = authenticated_api_client.delete(
        reverse("wallets:wallets-detail", args=[wallet.id])
    )

    assert response.status_code == 404
    assert Wallet.objects.count() == 1


@pytest.mark.django_db
def test_wallet_view_delete_wallet_participant(authenticated_api_client):
    participant = authenticated_api_client.user
    wallet = WalletFactory(participants=[participant])

    response = authenticated_api_client.delete(
        reverse("wallets:wallets-detail", args=[wallet.id])
    )

    assert response.status_code == 404
    assert Wallet.objects.count() == 1


@pytest.mark.django_db
def test_wallet_view_get_expenses_owner(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner)
    transaction = TransactionFactory(wallet=wallet)
    category = transaction.category

    response = authenticated_api_client.get(
        reverse("wallets:wallets-expenses", args=[wallet.id])
    )

    assert response.status_code == 200
    assert (
        response.data[category]
        == TransactionListSerializer([transaction], many=True).data
    )


@pytest.mark.django_db
def test_wallet_view_get_expenses_participant(authenticated_api_client):
    participant = authenticated_api_client.user
    wallet = WalletFactory(participants=[participant])
    transaction = TransactionFactory(wallet=wallet)
    category = transaction.category

    response = authenticated_api_client.get(
        reverse("wallets:wallets-expenses", args=[wallet.id])
    )

    assert response.status_code == 200
    assert (
        response.data[category]
        == TransactionListSerializer([transaction], many=True).data
    )


@pytest.mark.django_db
def test_wallet_view_get_expenses_no_owner_no_participant(authenticated_api_client):
    transaction = TransactionFactory()

    response = authenticated_api_client.get(
        reverse("wallets:wallets-expenses", args=[transaction.wallet.id])
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_wallet_view_post_expenses_owner(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner)

    data = {
        "title": "test expense",
        "category": Category.OTHER,
        "currency": Currency.PLN,
        "amount": 1000,
    }

    response = authenticated_api_client.post(
        reverse("wallets:wallets-expenses", args=[wallet.id]), data=data
    )

    assert response.status_code == 201
    assert response.data["title"] == "test expense"
    assert response.data["category"] == Category.OTHER
    assert response.data["currency"] == Currency.PLN
    assert response.data["amount"] == 1000
    assert response.data["date"] == str(now().date())
    assert response.data["is_expense"] is True
    assert response.data["wallet"] == wallet.id


@pytest.mark.django_db
def test_wallet_view_post_expenses_participant(authenticated_api_client):
    participant = authenticated_api_client.user
    wallet = WalletFactory(participants=[participant])

    data = {
        "title": "test expense",
        "category": Category.OTHER,
        "currency": Currency.PLN,
        "amount": 1000,
    }

    response = authenticated_api_client.post(
        reverse("wallets:wallets-expenses", args=[wallet.id]), data=data
    )

    assert response.status_code == 406
    assert response.data["detail"] == NotOwnerError.DETAIL
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_wallet_view_post_expenses_no_owner_no_participant(authenticated_api_client):
    wallet = WalletFactory()

    data = {
        "title": "test expense",
        "category": Category.OTHER,
        "currency": Currency.PLN,
        "amount": 1000,
    }

    response = authenticated_api_client.post(
        reverse("wallets:wallets-expenses", args=[wallet.id]), data=data
    )

    assert response.status_code == 404
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_wallet_view_get_income_owner(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner)
    transaction = TransactionFactory(wallet=wallet, is_expense=False)
    category = transaction.category

    response = authenticated_api_client.get(
        reverse("wallets:wallets-income", args=[wallet.id])
    )

    assert response.status_code == 200
    assert (
        response.data[category]
        == TransactionListSerializer([transaction], many=True).data
    )


@pytest.mark.django_db
def test_wallet_view_get_income_participant(authenticated_api_client):
    participant = authenticated_api_client.user
    wallet = WalletFactory(participants=[participant])
    transaction = TransactionFactory(wallet=wallet, is_expense=False)
    category = transaction.category

    response = authenticated_api_client.get(
        reverse("wallets:wallets-income", args=[wallet.id])
    )

    assert response.status_code == 200
    assert (
        response.data[category]
        == TransactionListSerializer([transaction], many=True).data
    )


@pytest.mark.django_db
def test_wallet_view_get_income_no_owner_no_participant(authenticated_api_client):
    transaction = TransactionFactory()

    response = authenticated_api_client.get(
        reverse("wallets:wallets-income", args=[transaction.wallet.id])
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_wallet_view_post_income_owner(authenticated_api_client):
    owner = authenticated_api_client.user
    wallet = WalletFactory(owner=owner)

    data = {
        "title": "test expense",
        "category": Category.OTHER,
        "currency": Currency.PLN,
        "amount": 1000,
    }

    response = authenticated_api_client.post(
        reverse("wallets:wallets-income", args=[wallet.id]), data=data
    )

    assert response.status_code == 201
    assert response.data["title"] == "test expense"
    assert response.data["category"] == Category.OTHER
    assert response.data["currency"] == Currency.PLN
    assert response.data["amount"] == 1000
    assert response.data["date"] == str(now().date())
    assert response.data["is_expense"] is False
    assert response.data["wallet"] == wallet.id


@pytest.mark.django_db
def test_wallet_view_post_income_participant(authenticated_api_client):
    participant = authenticated_api_client.user
    wallet = WalletFactory(participants=[participant])

    data = {
        "title": "test expense",
        "category": Category.OTHER,
        "currency": Currency.PLN,
        "amount": 1000,
    }

    response = authenticated_api_client.post(
        reverse("wallets:wallets-income", args=[wallet.id]), data=data
    )

    assert response.status_code == 406
    assert response.data["detail"] == NotOwnerError.DETAIL
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_wallet_view_post_income_no_owner_no_participant(authenticated_api_client):
    wallet = WalletFactory()

    data = {
        "title": "test expense",
        "category": Category.OTHER,
        "currency": Currency.PLN,
        "amount": 1000,
    }

    response = authenticated_api_client.post(
        reverse("wallets:wallets-income", args=[wallet.id]), data=data
    )

    assert response.status_code == 404
    assert Transaction.objects.count() == 0
