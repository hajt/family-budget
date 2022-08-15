import factory
import factory.fuzzy

from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.fuzzy.FuzzyText(length=12)
    last_name = factory.fuzzy.FuzzyText(length=12)
    username = factory.fuzzy.FuzzyText(length=12)
    password = factory.fuzzy.FuzzyText(length=12)
    email = factory.LazyAttribute(lambda user: f"{user.username}@example.com")

    class Meta:
        model = User
