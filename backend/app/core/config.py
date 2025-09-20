"""
Configuration settings for the application
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    APP_NAME: str = "Music from Drawings"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API settings
    API_V1_STR: str = "/api/v1"
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Database settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "music_from_drawings"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI API Keys
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Music generation APIs
    SUNO_API_KEY: Optional[str] = None
    BEATOVEN_API_KEY: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Monitoring
    ENABLE_METRICS: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
