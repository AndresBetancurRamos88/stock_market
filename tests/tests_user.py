import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_signup(client, user_signup):
    json_data = json.dumps(user_signup)
    response = client.post(
        reverse("signup"),
        data=json_data,
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json()


@pytest.mark.django_db
def test_fail_signup_not_name(client, user_signup):
    del user_signup["name"]
    json_data = json.dumps(user_signup)
    response = client.post(
        reverse("signup"),
        data=json_data,
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.json() == {"name": ["This field is required."]}


@pytest.mark.django_db
def test_fail_signup_not_last_name(client, user_signup):
    del user_signup["last_name"]
    json_data = json.dumps(user_signup)
    response = client.post(
        reverse("signup"),
        data=json_data,
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.json() == {"last_name": ["This field is required."]}


@pytest.mark.django_db
def test_fail_signup_not_email(client, user_signup):
    del user_signup["email"]
    json_data = json.dumps(user_signup)
    response = client.post(
        reverse("signup"),
        data=json_data,
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.json() == {"email": ["This field is required."]}


@pytest.mark.django_db
def test_fail_signup_not_credentials(client):
    response = client.post(
        reverse("signup"),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.json() == {
        "name": ["This field is required."],
        "last_name": ["This field is required."],
        "email": ["This field is required."],
    }
