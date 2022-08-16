import json

import pytest

from django.urls import reverse

from api.users.tests.factories import UserFactory
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
            }
        ]
    )

    response = authenticated_api_client.get(reverse("wallets:wallets-list"))
    response_data = json.dumps(response.data)

    assert response.status_code == 200
    assert response_data == expected_response


@pytest.mark.django_db
def test_wallet_view_get_list_no_wallets(authenticated_api_client):
    response = authenticated_api_client.get(reverse("wallets:wallets-list"))

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_wallet_view_get_list_no_owner_wallet(authenticated_api_client):
    WalletFactory()

    response = authenticated_api_client.get(reverse("wallets:wallets-list"))

    assert response.status_code == 200
    assert response.data == []


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
            }
        ]
    )

    response = authenticated_api_client.get(reverse("wallets:wallets-shared"))
    response_data = json.dumps(response.data)

    assert response.status_code == 200
    assert response_data == expected_response


@pytest.mark.django_db
def test_wallet_view_get_shared_wallets_no_participant(authenticated_api_client):
    WalletFactory(participants=[UserFactory()])

    response = authenticated_api_client.get(reverse("wallets:wallets-shared"))

    assert response.status_code == 200
    assert response.data == []


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
