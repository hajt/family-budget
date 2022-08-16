import pytest

from django.core.exceptions import ValidationError

from api.users.tests.factories import UserFactory
from ..models import Wallet
from .factories import WalletFactory


@pytest.mark.django_db
def test_wallet_repr():
    wallet = WalletFactory()
    assert wallet.__repr__() == f"<{Wallet.__name__}({wallet.name})>"


@pytest.mark.django_db
def test_wallet_str():
    wallet = WalletFactory()
    assert wallet.__str__() == f"{wallet.name} | {wallet.owner}"


@pytest.mark.django_db
def test_wallet_get_participants_display():
    participant = UserFactory()
    participant2 = UserFactory()
    wallet = WalletFactory(participants=[participant, participant2])
    assert wallet.get_participants_display() == f"{participant}, {participant2}"


@pytest.mark.django_db
def test_wallet_unique_constrain():
    owner = UserFactory()
    WalletFactory(name="test_wallet", owner=owner)

    with pytest.raises(ValidationError) as error:
        WalletFactory(name="test_wallet", owner=owner)

    assert (
        str(error.value)
        == "{'__all__': ['Wallet with this Name and Owner already exists.']}"
    )
