from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# bot/.env — always relative to the bot project root, not the process cwd.
_BOT_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _BOT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        # utf-8-sig strips a Windows BOM that otherwise breaks TELEGRAM_BOT_TOKEN
        env_file_encoding="utf-8-sig",
        extra="ignore",
    )

    telegram_bot_token: str
    bot_api_secret: str = "change-me"
    bot_http_host: str = "0.0.0.0"
    bot_http_port: int = 8081
    bot_username: str = "simp1e4ubot"
    bot_db_path: Path = Path("data/bot.sqlite3")
    # Express backend for telegram-linked callback
    backend_url: str = "http://127.0.0.1:3001"


@lru_cache
def get_settings() -> Settings:
    return Settings()
