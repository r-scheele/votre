from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str = Field(
        title="The description of the post", max_length=300
    )
    published: bool = True


class PostCreate(PostBase):
    pass


class PostSchema(PostBase):
    id: int
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        orm_mode = True



