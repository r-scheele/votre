from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from starlette import status

from app.config.database import get_db
from app.models.posts import Post
from app.schemas.posts import PostSchema, PostCreate
from app.utils.oauth2 import get_current_user

router = APIRouter(
    tags=["posts"],
    prefix="/posts"
)


@router.get(path="/{id}", response_model=PostSchema)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostSchema).filter(PostSchema.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} is not found")
    return post


@router.get("/", response_model=List[PostSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
def create_post(
        post: PostCreate,
        request: Request,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    print(request.headers)
    post = Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put(path="/{id}", response_model=PostSchema)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    previous_post = db.query(Post).filter(Post.id == post_id).first()
    if not previous_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} is not found")

    post = Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostSchema).filter(PostSchema.id == post_id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} is not found")

    post.delete()
    db.commit()
