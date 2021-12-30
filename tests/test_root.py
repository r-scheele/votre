
def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert type(response.json()) is str
