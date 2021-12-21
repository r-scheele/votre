from typing import Optional

from pydantic import BaseModel

from app.schemas.post import PostBase, PostSchema
from app.schemas.user import UserSchema


# Any response addition should be added here
class Posts(PostSchema):
    owner: UserSchema


class PostOut(BaseModel):
    Post: Posts
    likes: Optional[int] = 0

    class Config:
        orm_mode = True
