from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.utils import get_settings

settings = get_settings()
SQLALCHEMY_TEST_DATABASE_URL = f"postgresql://{settings.database_username}:" \
                               f"{settings.database_password}@{settings.database_hostname}:" \
                               f"{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

