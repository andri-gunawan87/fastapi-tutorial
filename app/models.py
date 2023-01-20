from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base
from uuid import uuid4

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(UUID(as_uuid=True), 
                     ForeignKey("users.id", ondelete="CASCADE"), 
                     nullable=False)
    user = relationship("User")
    
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    
    user_id = Column(UUID(as_uuid=True), 
                     ForeignKey("users.id", ondelete="CASCADE"), 
                     primary_key=True)
    post_id = Column(UUID(as_uuid=True), 
                     ForeignKey("posts.id", ondelete="CASCADE"), 
                     primary_key=True)