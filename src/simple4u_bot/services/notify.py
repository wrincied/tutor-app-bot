from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from simple4u_bot.config import Settings
from simple4u_bot.services import messages
from simple4u_bot.services.store import BindingStore

logger = logging.getLogger(__name__)


class NotifyService:
    def __init__(self, bot: Bot, store: BindingStore, settings: Settings) -> None:
        self.bot = bot
        self.store = store
        self.settings = settings

    @property
    def _site_url(self) -> str:
        return (self.settings.public_site_url or messages.DEFAULT_SITE_URL).rstrip("/")

    async def _send(self, student_id: str, text: str) -> dict:
        binding = self.store.get_by_student(student_id)
        if binding is None:
            return {"ok": False, "error": "not_linked"}
        if not binding.bot_active:
            return {"ok": False, "error": "bot_inactive"}
        try:
            await self.bot.send_message(chat_id=binding.chat_id, text=text)
        except TelegramAPIError as exc:
            return {"ok": False, "error": "telegram_error", "detail": str(exc)}
        return {"ok": True, "chat_id": binding.chat_id}

    def _tutor_of(self, student_id: str, tutor_name: str | None) -> str | None:
        if tutor_name and tutor_name.strip():
            return tutor_name.strip()
        binding = self.store.get_by_student(student_id)
        return (binding.tutor_name if binding else None) or None

    async def balance(
        self,
        student_id: str,
        lessons_left: float | int,
        *,
        tutor_name: str | None = None,
        rate_unit: str | None = None,
        lessons_before: float | int | None = None,
        reason: str | None = None,
    ) -> dict:
        return await self._send(
            student_id,
            messages.balance(
                lessons_left=lessons_left,
                tutor_name=self._tutor_of(student_id, tutor_name),
                rate_unit=rate_unit,
                lessons_before=lessons_before,
                reason=reason,
                site_url=self._site_url,
            ),
        )

    async def payment(
        self,
        student_id: str,
        *,
        amount_label: str,
        lessons_added: float | int,
        tutor_name: str | None = None,
        rate_unit: str | None = None,
    ) -> dict:
        return await self._send(
            student_id,
            messages.payment(
                amount_label=amount_label,
                lessons_added=lessons_added,
                tutor_name=self._tutor_of(student_id, tutor_name),
                rate_unit=rate_unit,
                site_url=self._site_url,
            ),
        )

    async def lesson_start(
        self,
        student_id: str,
        *,
        minutes_before: int,
        time_label: str,
        meeting_link: str | None = None,
        tutor_name: str | None = None,
    ) -> dict:
        return await self._send(
            student_id,
            messages.lesson_start(
                minutes_before=minutes_before,
                time_label=time_label,
                meeting_link=meeting_link,
                tutor_name=self._tutor_of(student_id, tutor_name),
                site_url=self._site_url,
            ),
        )

    async def homework(
        self,
        student_id: str,
        *,
        text: str,
        tutor_name: str | None = None,
    ) -> dict:
        return await self._send(
            student_id,
            messages.homework(
                text=text,
                tutor_name=self._tutor_of(student_id, tutor_name),
                site_url=self._site_url,
            ),
        )

    async def lesson_moved(
        self,
        student_id: str,
        *,
        new_time_label: str,
        meeting_link: str | None = None,
        tutor_name: str | None = None,
    ) -> dict:
        return await self._send(
            student_id,
            messages.lesson_moved(
                new_time_label=new_time_label,
                meeting_link=meeting_link,
                tutor_name=self._tutor_of(student_id, tutor_name),
                site_url=self._site_url,
            ),
        )
