from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    telegram_bot_token: str
    bot_api_secret: str = "change-me"
    bot_http_host: str = "0.0.0.0"
    bot_http_port: int = 8081
    bot_username: str = "Simple4UBot"
    bot_db_path: Path = Path("data/bot.sqlite3")


@lru_cache
def get_settings() -> Settings:
    return Settings()
