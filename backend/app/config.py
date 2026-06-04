# backend/app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TalentLink"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    DATABASE_URL: str = os.getenv("DATABASE_URL","postgresql+psycopg2://postgres:postgres@localhost:5432/talentlink")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/app/uploads")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    class Config:
        env_file = ".env"

settings = Settings()
