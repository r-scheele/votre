from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.models.users import User
from app.config.database import get_db
from app.schemas.users import UserCreate
from app.utils.oauth2 import create_access_token
from app.utils.utils import verify_password

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)


@router.post(path="/login")
def login(response: Response, user_body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    if not verify_password(user_body.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    token_in_session = create_access_token(
        data={
            "user_id": user.id,
            "role": user.role,
            "is_active": user.is_active
        })
    response.set_cookie("session", token_in_session)
    return {
        "access_token": token_in_session,
        "token_type": "bearer"
    }
