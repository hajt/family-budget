import factory
import factory.fuzzy

from api.users.tests.factories import UserFactory
from ..models import Currency, Wallet


class WalletFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText(length=12)
    currency = factory.fuzzy.FuzzyChoice(choices=Currency.values)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Wallet

    @factory.post_generation
    def participants(self, create, participants, **kwargs):
        if not create:
            return

        if participants:
            self.participants.set(participants)
