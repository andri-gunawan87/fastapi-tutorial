from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, conint

class CreateUser(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    
class CreateUserResponse(BaseModel):
    data: CreateUser

    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(BasePost):
    pass

class ResponsePost(BasePost):
    id: UUID
    user: CreateUser

    class Config:
        orm_mode = True
        
class ResponseData(BaseModel):
    data: ResponsePost

    class Config:
        orm_mode = True

class ResponseDataAll(BaseModel):
    Post: ResponsePost
    Vote: int

    class Config:
        orm_mode = True

class PostResponseJoin(BaseModel):
    data: List[ResponseDataAll]
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    token: str
    schemaType: str
    
class TokenData(BaseModel):
    id: Optional[str]
    
class TokenResponse(BaseModel):
    data: Token
    
class Vote(BaseModel):
    post_id: str
    dir: conint(le=1)

class VoteResponse(BaseModel):
    data: Vote