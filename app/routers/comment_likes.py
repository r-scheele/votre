from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.config.database import get_db
from app.models.comment_likes import CommentLike
from app.models.post_likes import Like
from app.schemas.comment_like import CommentLikeSchema
from app.schemas.like import LikeSchema
from app.utils.oauth2 import get_current_user

router = APIRouter(
    tags=["Comment likes"],
    prefix="/clikes"
)


@router.post(path="/", status_code=status.HTTP_201_CREATED)
def like_a_comment(like: CommentLikeSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    like_query = db.query(CommentLike).filter(CommentLike.post_id == like.post_id, CommentLike.owner_id == current_user.id)
    found_like = like_query.first()

    if like.dir == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id}"
                                                                             f" has already like {like.post_id}")
        new_vote = Like(post_id=like.post_id, owner_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {
            "message": "Post successfully liked!"
        }
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Like does not exist!")
        db.delete(like_query)
        db.commit()
        return {
            "message": "Like successfully deleted!"
        }