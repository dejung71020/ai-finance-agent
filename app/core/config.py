# app/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'
    )

    # --- Project settings ---
    PROJECT_NAME: str = "DJW"
    VERSION: str ='0.1.1'
    DEBUG: bool = False

    # --- DB ---
    POSTGRESQL_URL: str = Field(..., alias="POSTGRESQL_URL", description="PostgreSQL 연결 주소")
    REDIS_URL: str = Field(..., alias="REDIS_URL", description="Redis 연결 주소")

    # --- AI API ---
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    XAI_API_KEY: Optional[str] = None

    # --- Security ---
    SECRET_KEY: str = Field(..., alias="SECRET_KEY", description="JWT 토큰 비밀키")
    ALGORITHM: str = "HS256"
    ENCRYPTION_KEY: str = Field(..., alias="ENCRYPTION_KEY", description="AES-256 암호화 키 (64자 hex)")
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()