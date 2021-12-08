from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app.config.database import get_db
from app.schemas.posts import PostSchema, PostCreate

router = APIRouter(
    tags=["posts"],
    prefix="/posts"
)


@router.get(path="/{id}", response_model=PostSchema)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostSchema).filter(PostSchema.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")
    return post


@router.get("/", response_model=List[PostSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostSchema).all()
    return posts


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post = PostSchema(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put(path="/{id}", response_model=PostSchema)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    previous_post = db.query(PostSchema).filter(PostSchema.id == id).first()
    if not previous_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")

    post = PostSchema(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostSchema).filter(PostSchema.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")

    post.delete()
    db.commit()
