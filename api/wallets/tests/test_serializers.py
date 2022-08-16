import pytest

from api.users.tests.factories import UserFactory
from ..serializers import (
    WalletDetailSerializer,
    WalletSerializer,
    WalletUpdateSerializer,
)
from .factories import WalletFactory


@pytest.mark.django_db
def test_wallet_deserialization():
    wallet = WalletFactory()
    serializer = WalletSerializer(wallet)
    assert serializer.data["id"] == str(wallet.id)
    assert serializer.data["name"] == wallet.name
    assert serializer.data["currency"] == wallet.currency
    assert serializer.data["owner"] == str(wallet.owner)


@pytest.mark.django_db
def test_wallet_detail_deserialization():
    participant = UserFactory()
    wallet = WalletFactory(participants=[participant])
    serializer = WalletDetailSerializer(wallet)
    assert serializer.data["id"] == str(wallet.id)
    assert serializer.data["name"] == wallet.name
    assert serializer.data["currency"] == wallet.currency
    assert serializer.data["owner"] == str(wallet.owner)
    assert serializer.data["participants"] == [wallet.participants.first().id]


@pytest.mark.django_db
def test_wallet_update_deserialization():
    participant = UserFactory()
    wallet = WalletFactory(participants=[participant])
    serializer = WalletUpdateSerializer(wallet)
    assert serializer.data["id"] == str(wallet.id)
    assert serializer.data["name"] == wallet.name
    assert serializer.data["currency"] == wallet.currency
    assert serializer.data["owner"] == str(wallet.owner)
    assert serializer.data["participants"] == [wallet.participants.first().id]
