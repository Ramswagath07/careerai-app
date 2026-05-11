"""User data models and schemas"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: Optional[str] = None
    hashed_password: str
    role: UserRole = UserRole.user
    is_active: bool = True
    plan: str = "free"
    avatar_url: Optional[str] = None
    target_role: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resume_count: int = 0

class UserPublic(BaseModel):
    id: str
    email: str
    full_name: str
    role: UserRole
    plan: str
    target_role: Optional[str]
    location: Optional[str]
    experience_level: Optional[str]
    resume_count: int
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    target_role: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[str] = None
