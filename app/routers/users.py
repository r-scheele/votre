from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app.models.users import User
from app.config.database import get_db
from app.schemas.users import UserSchema, UserCreate
from app.utils.utils import hash_password

router = APIRouter(
    tags=["users"],
    prefix="/users"
)


@router.get(path="/{id}", response_model=UserSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found")
    return user


@router.get("/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=UserSchema, response_model_exclude_unset=True)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with the email {user.email}"
                                                                         f" already exists")

    user.password = hash_password(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the id {id} is not found")

    user.delete()
    db.commit()


@router.put(path="/{id}", response_model=UserSchema)
def update_user(id: int, user: UserCreate, db: Session = Depends(get_db)):
    pass
