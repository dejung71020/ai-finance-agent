# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # --- Project settings ---
    PROJECT_NAME: str = "DJW"
    VERSION: str ='0.1.1'
    DEBUG: bool = False

    # --- DB ---
    POSTGRESQL_URL: str = Field(..., alias="POSTGRESQL_URL")
    REDIS_URL: str = ""

    # --- AI API ---
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    XAI_API_KEY: Optional[str] = None

    # --- Security ---
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ALGORITHM: str = "HS256"

settings = Settings()