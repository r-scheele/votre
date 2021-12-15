from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Boolean, text, String, DateTime, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship, backref

from app.config.database import Base


class Comment(Base):
    __tablename__ = "comments"
    _N = 6

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))
    text = Column(String(140))
    owner_id = Column(Integer, ForeignKey('users.id'))
    disabled = Column(Boolean)
    created_at = Column(DateTime(), default=datetime.utcnow, index=True)
    path = Column(Text, index=True)
    parent_id = Column(Integer, ForeignKey('comment.id'))
    replies = relationship(
        'Comment', backref=backref('parent', remote_side=[id]),
        lazy='dynamic')
    likes = relationship('Like', backref='author', lazy='dynamic',
                         primaryjoin="Comment.id == Like.post_id")

    def save(self, db):
        db.add(self)
        db.commit()
        prefix = self.parent.path + '.' if self.parent else ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)
        db.commit()

    def level(self):
        return len(self.path)
