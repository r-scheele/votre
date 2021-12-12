from pydantic import BaseModel


class CommentSchema(BaseModel):
    post_id: int
    owner_id: int
    disabled: bool

