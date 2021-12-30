from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.config.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(String(140), index=True, nullable=False)
    published = Column(Boolean, server_default=expression.true(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', backref='posts_owner', cascade="all,delete",
                         foreign_keys=[owner_id])
    comments = relationship('Comment', backref='author', lazy='dynamic',
                            primaryjoin="Post.id == Comment.post_id")
    likes = relationship('Like', backref='author', lazy='dynamic',
                         primaryjoin="Post.id == Like.post_id")
