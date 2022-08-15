import json

import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_user_detail_view_authenticated(authenticated_api_client):
    user = authenticated_api_client.user
    expected_response = {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    response = authenticated_api_client.get(reverse("users:me"))

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_user_detail_view_unauthenticated(api_client):
    response = api_client.get(reverse("users:me"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_user_list_view(authenticated_api_client):
    user = authenticated_api_client.user
    expected_response = json.dumps(
        [
            {
                "id": str(user.id),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        ]
    )

    response = authenticated_api_client.get(reverse("users:users"))
    response_data = json.dumps(response.data)

    assert response.status_code == 200
    assert response_data == expected_response


@pytest.mark.django_db
def test_user_list_view_not_return_superuser(authenticated_api_client):
    user = authenticated_api_client.user
    user.is_staff = True
    user.is_superuser = True
    user.save()

    response = authenticated_api_client.get(reverse("users:users"))

    assert response.status_code == 200
    assert response.data == []
