from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.config.database import get_db
from app.models.likes import Like
from app.models.posts import Post
from app.schemas.like import LikeSchema
from app.utils.oauth2 import get_current_user

router = APIRouter(
    tags=["likes"],
    prefix="/likes"
)


@router.post(path="/", status_code=status.HTTP_201_CREATED)
def like_post(like: LikeSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Action not authorized, please login and try again")
    
    # now like would have a parent id field, search the post model if the row exists if it doesnt search the comment
    # if any of them is found, attach the like as appropriate
    # or use a path like likes/comment/id for comment like and likes/post/id for post likes but i don't know how to
    # persist to database yet. so lets wait and see -
    
    post = db.query(Post).filter(Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {like.post_id} does not exist")

    like_query = db.query(Like).filter(Like.post_id == like.post_id, Like.owner_id == current_user.id)
    found_like = like_query.first()

    if like.dir == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id}"
                                                                             f" has already like {like.post_id}")
        new_like = Like(post_id=like.post_id, owner_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {
            "message": "Post successfully liked!"
        }
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Like does not exist!")
        db.delete(found_like)
        db.commit()
        return {
            "message": "Like successfully deleted!"
        }
