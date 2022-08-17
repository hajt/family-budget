import factory
import factory.fuzzy

from api.wallets.models import Currency
from api.wallets.tests.factories import WalletFactory
from ..models import Category, Transaction


class TransactionFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(length=12)
    category = factory.fuzzy.FuzzyChoice(choices=Category.values)
    currency = factory.fuzzy.FuzzyChoice(choices=Currency.values)
    amount = factory.fuzzy.FuzzyInteger(low=1, high=10000)
    wallet = factory.SubFactory(WalletFactory)

    class Meta:
        model = Transaction
