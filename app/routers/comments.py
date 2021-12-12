from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.config.database import get_db
from app.models.comments import Comment
from app.schemas.comment import CommentSchema
from app.utils.oauth2 import get_current_user

router = APIRouter(
    tags=["comments"],
    prefix="/comments"
)


@router.post(path="/", status_code=status.HTTP_201_CREATED)
def comment_on_post(comment: CommentSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    comment_query = db.query(Comment).filter(Comment.post_id == comment.post_id, Comment.owner_id == current_user.id)
