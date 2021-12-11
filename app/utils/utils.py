from functools import lru_cache

from passlib.context import CryptContext

from app.config.config import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@lru_cache
def get_settings():
    return Settings()
