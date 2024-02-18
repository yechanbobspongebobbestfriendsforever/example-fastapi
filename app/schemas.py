    ## schema/pydantic model: define the structure of a request & response
    ## this ensures that wehn a user wants to create a post, the request will "only" go through if it has a 'title' and 'content' in the body

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

################################ USER ################################
class UserBase(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime
        
    class Config:
        from_attributes = True


############################# USER LOGIN #############################
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
################################ POST ################################

##### handles direction of the user sending data to us #####
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True #default to True
    
    
class PostCreate(PostBase):
    pass


##### handles direction for us to send data to users #####
class Post(PostBase):
    #specifies all the fields we want to include in the response
    id: int
    create_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True

############################# JWT TOKEN #############################
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None


############################# VOTE  #############################
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)