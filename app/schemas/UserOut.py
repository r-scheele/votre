from typing import Optional, List

from app.schemas.post import PostSchema
from app.schemas.user import UserSchema


class UserOut(UserSchema):
    pass
    # posts: Optional[List[PostSchema]] = []
