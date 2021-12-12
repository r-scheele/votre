from sqlalchemy import Column, Integer, String, text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.config.database import Base


# implement search functionality when username is added to the model

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String(120), index=True, nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    is_active = Column(Boolean, server_default=expression.true(), nullable=False)
    role = Column(String(128), nullable=False, server_default="user")

    posts = relationship('Post', backref='post_author', lazy='dynamic',
                         primaryjoin="User.id == Post.owner_id")
    post_likes = relationship('Like', backref='post_likes_author', lazy='dynamic',
                              primaryjoin="User.id == Like.owner_id")
    comments = relationship('Comment', backref='comment_author', lazy='dynamic',
                            primaryjoin="User.id == Comment.owner_id")
    comment_likes = relationship('CommentLike', backref='comment_likes_author', lazy='dynamic',
                                 primaryjoin="User.id == CommentLike.owner_id")
