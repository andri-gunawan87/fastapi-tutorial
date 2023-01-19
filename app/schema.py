from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
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
    user_id: UUID
    user: CreateUser

    class Config:
        orm_mode = True
        
class ResponseData(BaseModel):
    data: ResponsePost

    class Config:
        orm_mode = True

class ResponseDataAll(BaseModel):
    data: List[ResponsePost]

    class Config:
        orm_mode = True

class Token(BaseModel):
    token: str
    schemaType: str
    
class TokenData(BaseModel):
    id: Optional[str]
    
class TokenResponse(BaseModel):
    data: Token