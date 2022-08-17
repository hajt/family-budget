import pytest

from ..models import Transaction
from .factories import TransactionFactory


@pytest.mark.django_db
def test_transaction_amount_decimal_expense():
    transaction = TransactionFactory(amount=100)
    assert transaction.amount_decimal == "-1.00"


@pytest.mark.django_db
def test_transaction_amount_decimal_income():
    transaction = TransactionFactory(is_expense=False, amount=100)
    assert transaction.amount_decimal == "1.00"


@pytest.mark.django_db
def test_transaction_name():
    transaction = TransactionFactory()
    assert transaction.name == f"{transaction.title} = {transaction.amount_decimal}"


@pytest.mark.django_db
def test_transaction_repr():
    transaction = TransactionFactory()
    assert transaction.__repr__() == f"<{Transaction.__name__}({transaction.name})>"


@pytest.mark.django_db
def test_wallet_str():
    transaction = TransactionFactory()
    assert transaction.__str__() == f"{transaction.name} | {transaction.wallet}"
