from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.config.database import get_db
from app.models.post_likes import Like
from app.schemas.like import LikeSchema
from app.utils.oauth2 import get_current_user

router = APIRouter(
    tags=["likes"],
    prefix="/likes"
)


@router.post(path="/", status_code=status.HTTP_201_CREATED)
def like_post(like: LikeSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    like_query = db.query(Like).filter(Like.post_id == like.post_id, Like.owner_id == current_user.id)
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