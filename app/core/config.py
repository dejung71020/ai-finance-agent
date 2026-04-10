# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # --- Project settings ---
    PROJECT_NAME: str = "DJW"
    DEBUG: bool = False

    # --- DB ---
    POSTGRESQL_URL: str
    REDIS_URL: str = ""

    # --- AI API ---
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    XAI_API_KEY: str = ""

    # --- Security ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

settings = Settings()