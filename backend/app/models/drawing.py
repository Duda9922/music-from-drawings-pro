"""
Drawing model for MongoDB
"""

from beanie import Document
from pydantic import Field, BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DrawingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class VisualAnalysis(BaseModel):
    """Visual analysis results"""
    colors: Dict[str, Any]
    lines: Dict[str, Any]
    density: float
    symmetry: float
    mood: str
    subject: str
    style: str
    complexity: float
    brightness: float
    contrast: float

class Drawing(Document):
    """Drawing document model"""
    
    # Basic info
    user_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    
    # Image data
    image_url: str
    image_hash: str
    width: int
    height: int
    
    # Analysis results
    visual_analysis: Optional[VisualAnalysis] = None
    status: DrawingStatus = DrawingStatus.PENDING
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None
    
    # Metadata
    processing_time: Optional[float] = None
    error_message: Optional[str] = None
    
    class Settings:
        name = "drawings"
        indexes = [
            "user_id",
            "status",
            "created_at",
            "image_hash"
        ]
