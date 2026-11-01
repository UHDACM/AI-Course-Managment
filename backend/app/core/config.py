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