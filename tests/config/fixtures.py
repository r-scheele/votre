import pytest
from starlette.testclient import TestClient

from app.config.database import Base, get_db
from app.main import app
from tests.config.database import engine, TestingSessionLocal


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
def client(session):
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
