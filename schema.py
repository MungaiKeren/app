from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    content: str
    title: str

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str
    password: str
    name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str