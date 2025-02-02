from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union

class PostBase(BaseModel):
    title: str
    content : str
    published: bool = True


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode: True

class Post(PostBase):
    id: int
    created_at: datetime
    user_email: str
    owner: UserOut

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None