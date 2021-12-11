from typing import List, Optional

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette import status

from app.models.posts import Post
from app.models.users import User
from app.config.database import get_db
from app.schemas.UserOut import UserOut
from app.schemas.user import UserSchema, UserCreate
from app.utils.oauth2 import get_current_user
from app.utils.utils import hash_password

router = APIRouter(
    tags=["users"],
    prefix="/users"
)


@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db), current_user=Depends(get_current_user),
                  limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    users = db.query(User).order_by(desc(User.created_at)).filter(Post.title.contains(search)).\
        limit(limit=limit).offset(offset=skip).all()
    return users


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=UserOut,
             response_model_exclude_unset=True)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
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


@router.get(path="/{user_id}", response_model=UserOut)
def get_a_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} is not found")
    return user


@router.delete(path="/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the id {user_id} is not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Action not authorized")

    db.delete(user)
    db.commit()


@router.put(path="/{user_id}", response_model=UserOut)
def update_a_user(user_id: int, user: UserCreate, db: Session = Depends(get_db),
                  current_user=Depends(get_current_user)):
    previous_user_query = db.query(User).filter(User.id == user_id)
    previous_user = previous_user_query.first()

    if not previous_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {user_id} is not found")
    if previous_user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Action not authorized, please login and try again")

    previous_user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return previous_user_query.first()
