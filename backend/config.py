"""
Configuration management for the Storyblok Voice Assistant backend.
Loads environment variables and provides validated settings.
"""

from typing import List
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # AWS Bedrock Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_session_token: str = ""  # Optional, for temporary credentials
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    
    # Storyblok Configuration
    storyblok_token: str
    storyblok_space_id: str
    storyblok_api_base: str = "https://api-staging-d1.storyblok.com"
    
    # Application Configuration
    app_name: str = "Storyblok Voice Assistant"
    debug: bool = False
    cors_origins: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    
    # API Configuration
    max_conversation_history: int = 10
    default_search_limit: int = 10
    request_timeout: int = 30
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields in .env
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure settings are only loaded once.
    """
    return Settings()