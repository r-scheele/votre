from sqlalchemy import Column, Integer, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from app.config.database import Base


class CommentLike(Base):
    __tablename__ = "comment_likes"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    comment_id = Column(Integer, ForeignKey('comments.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', backref='author', cascade="all,delete", foreign_keys=[owner_id],
                         overlaps="comment_likes,comment_likes_author")
    disabled = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
