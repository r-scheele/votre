from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from app.config.database import get_db
from app.models.users import User
from app.schemas.token import TokenData
from app.utils.utils import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
cookie_handler = APIKeyCookie(name="session")
settings = get_settings()


async def get_current_user(token: str = Depends(cookie_handler or oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(credentials_exception, token=token)
    user = db.query(User).filter(User.id == token.user_id).first()
    return user


def verify_access_token(credentials_exception: HTTPException, token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("user_id")
        role: str = payload.get("user_id")
        is_active: str = payload.get("is_active")

        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, role=role, is_active=is_active)
    except JWTError:
        raise credentials_exception

    return token_data


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expires_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
