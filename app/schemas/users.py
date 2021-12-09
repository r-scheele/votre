from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserSchema(UserBase):
    id: int
    created_at: datetime
    role: Optional[str] = "user"
    is_active: bool
#    posts: Optional[List[Post]] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
