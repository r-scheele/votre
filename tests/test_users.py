from fastapi.testclient import TestClient
from app.main import app
from app.schemas.UserOut import UserOut

client = TestClient(app=app)


def test_create_new_user():
    body = {
        "email": "user100@example.com",
        "password": "string"
    }
    response = client.post("/users/", json=body)
    assert response.status_code == 201
    assert body["email"] == UserOut(**response.json()).email
