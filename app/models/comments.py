from sqlalchemy import Column, Integer, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from app.config.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', backref='post_comments', cascade="all,delete", foreign_keys=[post_id])
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', backref='owner', cascade="all,delete", foreign_keys=[owner_id],
                         overlaps="comment_author,comments")
    disabled = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    likes = relationship('CommentLike', backref='author', lazy='dynamic',
                         primaryjoin="Comment.id == CommentLike.comment_id")
