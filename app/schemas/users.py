from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserSchema(UserBase):
    id: int
    created_at: datetime
#    posts: Optional[List[Post]] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
