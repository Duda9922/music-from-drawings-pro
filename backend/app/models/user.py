"""
User model for MongoDB
"""

from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    PREMIUM = "premium"

class User(Document):
    """User document model"""
    
    # Basic info
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    
    # Authentication
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False
    
    # Profile
    role: UserRole = UserRole.USER
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    
    # Usage tracking
    drawings_count: int = 0
    music_generations_count: int = 0
    total_play_time: float = 0.0
    
    # Preferences
    preferred_genres: List[str] = []
    preferred_instruments: List[str] = []
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Subscription
    subscription_tier: str = "free"
    subscription_expires: Optional[datetime] = None
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "username",
            "is_active",
            "created_at"
        ]
