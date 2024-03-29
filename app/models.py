## every model represents a table in our database
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    ## sqlalchemy model: define what our database table will looks like
    ## -responsible for defining the columns of our 'posts' table within postgres
    ## is used to query, create, delete, and update entries within the database
    
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), 
                       nullable=False, 
                       server_default=text('now()'))
    owner_id = Column(Integer,
                      ForeignKey(column="users.id",ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")
    
    
class User(Base):
    
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), 
                       nullable=False, 
                       server_default=text('now()'))
    
    
class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer,
                     ForeignKey(column="users.id", ondelete="CASCADE"),
                     primary_key=True)
    post_id = Column(Integer, 
                     ForeignKey(column="posts.id", ondelete="CASCADE"),
                     primary_key=True)