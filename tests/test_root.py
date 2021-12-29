from tests.config.fixtures import client, session


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert type(response.json()) is str
