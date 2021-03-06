from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from starlette import status

from app.config.database import get_db
from app.models.likes import Like
from app.models.posts import Post
from app.models.users import User
from app.schemas.PostOut import PostOut, Posts
from app.schemas.post import PostSchema, PostCreate
from app.utils.oauth2 import get_current_user

router = APIRouter(
    tags=["posts"],
    prefix="/posts"
)


@router.get(path="/{post_id}", response_model=PostOut)
def get_a_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(Post, func.count(Like.post_id).label("likes")) \
        .join(Like, Like.post_id == Post.id, isouter=True).group_by(Post.id).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} is not found")
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Action not authorized, please login and try again")

    return post


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=Posts)
def create_a_post(post: PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Action not authorized, please login and try again")
    user = db.query(User).filter(User.id == current_user.id).first()
    post = Post(owner_id=current_user.id, owner=user, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put(path="/{post_id}", response_model=Posts)
def update_a_post(post_id: int, post: PostCreate, db: Session = Depends(get_db),
                  current_user=Depends(get_current_user)):
    previous_post_query = db.query(Post).filter(Post.id == post_id)
    previous_post = previous_post_query.first()

    if not previous_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} is not found")
    if previous_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Action not authorized, please login and try again")

    previous_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return previous_post_query.first()


@router.delete(path="/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} is not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Action not authorized")

    db.delete(post)
    db.commit()


@router.get(path="/", response_model=List[PostOut])
# @router.get(path="/")
def get_all_posts(db: Session = Depends(get_db),
                  current_user=Depends(get_current_user),
                  limit: int = 10, skip: int = 0,
                  search: Optional[str] = ""):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Action not authorized, please login and try again")
    else:
        posts = db.query(Post, func.count(Like.post_id).label("likes")) \
            .join(Like, Like.post_id == Post.id, isouter=True).group_by(Post.id).filter(Post.title.contains(search)). \
            order_by(desc(Post.created_at)).limit(limit=limit).offset(offset=skip).all()

    return posts


@router.get(path="/all/{user_id}", response_model=List[PostOut])
def get_all_posts_from_a_user(user_id: int,
                              db: Session = Depends(get_db),
                              current_user=Depends(get_current_user),
                              limit: int = 10, skip: int = 0,
                              search: Optional[str] = ""):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Action not authorized, please login and try again")
    else:
        posts = db.query(Post, func.count(Like.post_id).label("likes")) \
            .join(Like, Like.post_id == Post.id, isouter=True).group_by(Post.id).filter(
            Post.owner_id == user_id).filter(Post.title.contains(search)). \
            order_by(desc(Post.created_at)).limit(limit=limit).offset(offset=skip).all()

    return posts
