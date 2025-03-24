from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Facebook API credentials
    FACEBOOK_APP_ID: str = os.getenv("FACEBOOK_APP_ID", "")
    FACEBOOK_APP_SECRET: str = os.getenv("FACEBOOK_APP_SECRET", "")
    
    # Calendly API credentials
    CALENDLY_API_KEY: str = os.getenv("CALENDLY_API_KEY", "")
    
    # MLS API credentials
    MLS_API_KEY: str = os.getenv("MLS_API_KEY", "")
    
    # FollowUpBoss API credentials
    FOLLOWUPBOSS_API_KEY: str = os.getenv("FOLLOWUPBOSS_API_KEY", "")
    
    # OpenAI API credentials
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API endpoints
    FACEBOOK_API_VERSION: str = "v18.0"
    CALENDLY_API_URL: str = "https://api.calendly.com/v2"
    MLS_API_URL: str = "https://api.mls.com/v1"
    FOLLOWUPBOSS_API_URL: str = "https://api.followupboss.com/v1"
    
    # Rate limiting
    FACEBOOK_RATE_LIMIT: int = 200  # requests per hour
    CALENDLY_RATE_LIMIT: int = 100  # requests per minute
    
    class Config:
        env_file = ".env"

# Create global settings instance
settings = Settings() 