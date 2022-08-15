import pytest

from ..models import User
from .factories import UserFactory


@pytest.mark.django_db
def test_user_name():
    user = UserFactory(first_name="Jan", last_name="Kowalski")
    assert user.name == "Jan Kowalski"


@pytest.mark.django_db
def test_user_repr():
    user = UserFactory(first_name="Jan", last_name="Kowalski")
    assert user.__repr__() == f"<User({user.username})>"


@pytest.mark.django_db
def test_create_super_user():
    user = User.objects.create_superuser(
        first_name="Jan",
        last_name="Kowalski",
        username="jankowalski",
        email="jankowalski@user.com",
        password="password1234",
    )
    assert user.first_name == "Jan"
    assert user.last_name == "Kowalski"
    assert user.username == "jankowalski"
    assert user.email == "jankowalski@user.com"
    assert user.is_staff is True
    assert user.is_superuser is True


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        first_name="Jan",
        last_name="Kowalski",
        username="jankowalski",
        email="jankowalski@user.com",
        password="password1234",
    )
    assert user.first_name == "Jan"
    assert user.last_name == "Kowalski"
    assert user.username == "jankowalski"
    assert user.email == "jankowalski@user.com"
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_no_email():
    with pytest.raises(ValueError) as error:
        User.objects.create_user("", "password1234")
        assert error.value == "Email must be provided"
