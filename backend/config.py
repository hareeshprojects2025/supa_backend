"""
Configuration Management
Loads environment variables and application settings
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database - Railway provides DATABASE_URL automatically
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://user:password@localhost/bluscan_db"
    )
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Mobile Attendance System"
    
    # Security (add JWT secrets here if needed)
    SECRET_KEY: Optional[str] = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()