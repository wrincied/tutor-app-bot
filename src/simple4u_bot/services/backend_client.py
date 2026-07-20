from __future__ import annotations

import logging
from typing import Any

import httpx

from simple4u_bot.config import Settings

logger = logging.getLogger(__name__)


class BackendClient:
    """Bot → Express CRM API (X-Bot-Secret)."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.base = (settings.backend_url or "").rstrip("/")
        self.secret = settings.bot_api_secret

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Bot-Secret": self.secret,
        }

    async def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any] | None:
        if not self.base:
            logger.warning("BACKEND_URL not set")
            return None
        url = f"{self.base}{path}"
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.request(method, url, headers=self._headers(), **kwargs)
                if res.status_code >= 400:
                    logger.error("backend %s %s → %s %s", method, path, res.status_code, res.text)
                    return None
                data = res.json()
                return data if isinstance(data, dict) else {"data": data}
        except Exception:
            logger.exception("backend request failed: %s %s", method, path)
            return None

    async def notify_linked(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        return await self._request("POST", "/api/bot/telegram-linked", json=payload)

    async def notify_unlinked(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        return await self._request("POST", "/api/bot/telegram-unlinked", json=payload)

    async def get_lessons(self, student_id: str, *, limit: int = 15) -> dict[str, Any] | None:
        return await self._request(
            "GET",
            f"/api/bot/students/{student_id}/lessons",
            params={"limit": limit},
        )

    async def get_payment_summary(self, student_id: str) -> dict[str, Any] | None:
        return await self._request("GET", f"/api/bot/students/{student_id}/payment-summary")

    async def get_profile(self, student_id: str) -> dict[str, Any] | None:
        return await self._request("GET", f"/api/bot/students/{student_id}/profile")

    async def set_language(self, student_id: str, lang: str) -> dict[str, Any] | None:
        return await self._request(
            "POST",
            f"/api/bot/students/{student_id}/language",
            json={"lang": lang},
        )
