from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


# ---------- AUTH ----------
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- USERS ----------
class UserUpdate(BaseModel):
    bio: Optional[str] = Field(default=None, max_length=500)
    avatar_url: Optional[str] = Field(default=None, max_length=500)


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    id: int
    username: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- POSTS ----------
class PostCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    image_url: Optional[str] = Field(default=None, max_length=500)


class PostOut(BaseModel):
    id: int
    user_id: int
    content: str
    image_url: Optional[str] = None
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0

    class Config:
        from_attributes = True


# ---------- COMMENTS ----------
class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class CommentOut(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- FEED ----------
class FeedOut(BaseModel):
    items: List[PostOut]
    limit: int
    offset: int
    total: int
