from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app.config.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(String(140), index=True, nullable=False)
    published = Column(Boolean, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey('users.id'))
