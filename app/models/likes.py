from sqlalchemy import Column, Integer, ForeignKey, Boolean, text, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from app.config.database import Base


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    disabled = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
