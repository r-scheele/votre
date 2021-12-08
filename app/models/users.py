from sqlalchemy import Column, Integer, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from app.config.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String(120), index=True, nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    posts = relationship('Post', backref='author', lazy='dynamic')
