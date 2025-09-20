"""
Music generation model for MongoDB
"""

from beanie import Document
from pydantic import Field, BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MusicStatus(str, Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"

class MusicParameters(BaseModel):
    """Music generation parameters"""
    tempo: int
    key: str
    scale: str
    genre: str
    mood: str
    instruments: List[str]
    duration: int
    dynamics: str
    rhythm_pattern: str

class MusicGeneration(Document):
    """Music generation document model"""
    
    # References
    drawing_id: str
    user_id: Optional[str] = None
    
    # Music parameters
    parameters: MusicParameters
    
    # Generated content
    prompt: str
    audio_url: Optional[str] = None
    audio_duration: Optional[float] = None
    
    # Status and metadata
    status: MusicStatus = MusicStatus.PENDING
    provider: str  # suno, beatoven, etc.
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    generated_at: Optional[datetime] = None
    
    # Processing info
    generation_time: Optional[float] = None
    error_message: Optional[str] = None
    
    # Analytics
    play_count: int = 0
    rating: Optional[float] = None
    
    class Settings:
        name = "music_generations"
        indexes = [
            "drawing_id",
            "user_id",
            "status",
            "created_at",
            "provider"
        ]
