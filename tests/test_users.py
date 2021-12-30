import pytest
from jose import jwt

from app.schemas.UserOut import UserOut
from app.schemas.token import Token
from tests.config.database import settings


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
    login_res = Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id: str = payload.get("user_id")

    assert user_id == test_create_user_before_login["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("users@gmail.com", "string", 403),
    ("users@example.com", "string", 403),
    ("user@example.com", "strings", 403),
    (None, "strings", 422),
    ("user@example.com", None, 422)
])
def test_unsuccessful_login(client, email, password, status_code):
    body = {
        "username": email,
        "password": password
    }
    response = client.post("auth/login", data=body)
    assert response.status_code == status_code


def test_delete_a_user(client):
    pass
