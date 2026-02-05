from typing import Literal, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
# for response format
class Post(PostBase):
    created_at: datetime
    id: int
    user_id: int
    user: UserOut
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Posts: Post
    votes: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr #email valid checks
    password: str

# for response format
class UserOut(BaseModel):
    created_at: datetime
    id: int
    email: EmailStr #email valid checks
    # password: str
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr #email valid checks
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Votes(BaseModel):
    post_id: int
    dir: Literal[0,1]