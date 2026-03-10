
from datetime import datetime

from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(Integer, default=lambda: int(datetime.now().timestamp()))


class Event(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    camera_id = Column(String)
    timestamp = Column(Integer)
    type = Column(String)
    count = Column(Integer)
    image_path = Column(String)
