from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserSchema(UserBase):
    id: int
    created_at: datetime
    role: Optional[str] = "user"
    is_active: bool


class UserCreate(UserBase):
    password: str


from app.schemas.post import PostSchema

UserSchema.update_forward_refs()
