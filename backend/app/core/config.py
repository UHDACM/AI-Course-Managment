from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class DatabaseSettings(BaseSettings):
    mongodb_url: str="mongodb://localhost:27017"
    mongodb_database: str="TestingMongo"

    mongodb_min_pool_size: int=10
    mongodb_max_pool_size: int=100

    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


class Settings(BaseSettings):
    """Settings for the auth / classes / assignments / submissions API (app/main.py)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mongodb_url: str
    mongodb_database: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    max_upload_bytes: int = 10 * 1024 * 1024  # 10 MB


@lru_cache
def get_settings() -> Settings:
    return Settings()
