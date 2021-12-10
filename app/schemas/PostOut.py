from app.schemas.post import PostSchema
from app.schemas.user import UserSchema


class PostOut(PostSchema):
    owner: UserSchema
