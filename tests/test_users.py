import pytest
from app.schemas.UserOut import UserOut
from tests.config.fixtures import client, session


@pytest.fixture
def test_create_user_before_login(client):
    body = {
        "email": "user@example.com",
        "password": "string"
    }
    response = client.post(url="/users/", json=body)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = body["password"]
    return new_user


def test_create_new_user(client):
    body = {
        "email": "user@example.com",
        "password": "string"
    }
    response = client.post("/users/", json=body)
    assert response.status_code == 201
    assert body["email"] == UserOut(**response.json()).email


def test_login_a_user(client, test_create_user_before_login):
    body = {
        "username": test_create_user_before_login["email"],
        "password": test_create_user_before_login["password"]
    }
    # data in the request - route accepts form data
    response = client.post("auth/login", data=body)
    assert response.status_code == 200


def test_get_all_users(client):
    pass


def test_delete_a_user(client):
    pass
