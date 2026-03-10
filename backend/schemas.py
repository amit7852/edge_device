
from typing import Optional
from pydantic import BaseModel


# User schemas
class UserBase(BaseModel):
    """Base user schema"""
    username: str


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: int

    class Config:
        from_attributes = True


# Event schemas
class EventBase(BaseModel):
    """Base event schema"""
    camera_id: str
    timestamp: int
    type: str
    count: int


class EventCreate(EventBase):
    """Schema for creating a new event"""
    image_path: Optional[str] = None


class EventResponse(EventBase):
    """Schema for event response"""
    id: int
    image_path: Optional[str] = None

    class Config:
        from_attributes = True

