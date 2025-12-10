from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://hr_user:hr_password@localhost:5432/hr_platform"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_NAME: str = "HR Platform API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    ALLOWED_ORIGINS: list = [
        "http://localhost:8501",
        "http://localhost:8000",
    ]
    
    WORK_UA_API_KEY: Optional[str] = os.getenv("WORK_UA_API_KEY")
    ROBOTA_UA_API_KEY: Optional[str] = os.getenv("ROBOTA_UA_API_KEY")
    OLX_API_KEY: Optional[str] = os.getenv("OLX_API_KEY")
    
    NOTIFICATION_PROVIDER: str = os.getenv("NOTIFICATION_PROVIDER", "console")
    WHATSAPP_API_KEY: Optional[str] = os.getenv("WHATSAPP_API_KEY")
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")
    
    EDIT_LOCK_TIMEOUT_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
