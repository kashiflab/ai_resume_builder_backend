# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Resume Builder API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for generating professional resumes with JWT authentication"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]  # In production, replace with specific origins
    
    # JWT settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "ai_reume_anty_dolphin")
    ALGORITHM: str = "HS256"
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings() 