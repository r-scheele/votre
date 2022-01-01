import pytest
from starlette.testclient import TestClient

from app.config.database import Base, get_db
from app.main import app
from app.models.posts import Post
from app.utils.oauth2 import create_access_token
from tests.config.database import engine, TestingSessionLocal


@pytest.fixture
def session():
    """
    :return: database object - can be queried in the tests functions
    """

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session) -> TestClient:
    """
    :param session: database object
    :return: test client - from starlette
    """

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app=app)


@pytest.fixture
def test_create_user_before_login(client) -> dict:
    body = {
        "email": "user@example.com",
        "password": "string"
    }
    response = client.post(url="/users/", json=body)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = body["password"]
    return new_user


@pytest.fixture
def test_create_second_user_before_login(client) -> dict:
    body = {
        "email": "user2@example.com",
        "password": "string"
    }
    response = client.post(url="/users/", json=body)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = body["password"]
    return new_user


@pytest.fixture
def token(test_create_user_before_login) -> str:
    token = create_access_token(
        data={
            "user_id": test_create_user_before_login["id"],
            "role": test_create_user_before_login["role"],
            "is_active": test_create_user_before_login["is_active"]
        })
    return token


@pytest.fixture
def authorized_client(client, token) -> TestClient:
    """
    :param client:
    :param token:
    :return: the first test user:
    """

    # set headers in client
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    # set cookies in client
    client.cookies["session"] = token
    return client


@pytest.fixture
def test_posts(test_create_user_before_login, session, test_create_second_user_before_login):
    posts = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_create_user_before_login["id"]
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_create_user_before_login["id"]
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_create_user_before_login["id"]
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_create_second_user_before_login["id"]
        }
    ]
    post_models = list(map(lambda post: Post(**post), posts))
    session.add_all(post_models)
    session.commit()
    new_posts = session.query(Post).all()
    return new_posts
