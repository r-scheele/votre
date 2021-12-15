from sqlalchemy import Column, Integer, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from app.config.database import Base


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    # The post_id here should not be, i need something to reference comment and post, and then populate according to
    # whichever it is maybe - Many to One relationship maybe?
    post_id = Column(Integer, ForeignKey('posts.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    disabled = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
