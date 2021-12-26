from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app=app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert type(response.json()) is str
