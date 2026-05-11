from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    APP_NAME: str = "CareerAI"
    DEBUG: bool = False
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    MONGODB_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "careerai"
    MAX_FILE_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: list = ["pdf", "docx", "txt"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
