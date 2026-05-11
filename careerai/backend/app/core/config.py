from pydantic_settings import BaseSettings
from typing import List
import secrets

class Settings(BaseSettings):
    APP_NAME: str = "CareerAI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: str = "production"
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    MONGODB_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "careerai"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173","http://localhost:3000","https://careerai.vercel.app"]
    MAX_FILE_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "docx", "txt"]
    SPACY_MODEL: str = "en_core_web_sm"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
