from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.users import User
from app.config.database import get_db
from app.schemas.users import UserCreate
from app.utils.utils import verify_password

router = APIRouter(
    tags=["Authentication"],
)


@router.post(path="/auth")
def login(user_body: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_body.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    if not verify_password(user_body.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    return {"token": "login successful"}
