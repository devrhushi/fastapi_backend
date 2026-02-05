#tables 
from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship
class Posts(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key = True, nullable = False)
  title = Column(String, nullable = False)
  content = Column(String, nullable = False)
  published = Column(Boolean, server_default='True')
  created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

  user = relationship("Users")# when we fetch posts it will automatically bring the user info who created tht post internal relation


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))

class Votes(Base):
   __tablename__ = "votes"
   user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
   post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)