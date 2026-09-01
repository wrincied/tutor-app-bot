from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# bot/.env — always relative to the bot project root, not the process cwd.
_BOT_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _BOT_ROOT / ".env"

BotMode = Literal["polling", "webhook"]
BindingStoreKind = Literal["sqlite", "firestore"]


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
    bot_http_port: int = Field(default=8081, validation_alias=AliasChoices("BOT_HTTP_PORT", "PORT"))
    bot_username: str = "simp1e4ubot"
    bot_db_path: Path = Path("data/bot.sqlite3")
    bot_mode: BotMode = "polling"
    binding_store: BindingStoreKind = "sqlite"
    gcp_project: str = ""
    webhook_base_url: str = ""
    webhook_path: str = "/telegram/webhook"
    webhook_secret: str = ""
    # Express backend for telegram-linked callback
    backend_url: str = "http://127.0.0.1:3001"
    public_site_url: str = "https://simple4u.at"

    @property
    def webhook_url(self) -> str:
        base = (self.webhook_base_url or "").rstrip("/")
        path = self.webhook_path if self.webhook_path.startswith("/") else f"/{self.webhook_path}"
        return f"{base}{path}" if base else ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
