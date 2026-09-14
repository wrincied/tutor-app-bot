from __future__ import annotations

import logging
from typing import Any

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from simple4u_bot import keyboards
from simple4u_bot.config import Settings
from simple4u_bot.services import messages
from simple4u_bot.services.store import BindingStore
from simple4u_bot.services.telegram_send import send_text

logger = logging.getLogger(__name__)


class NotifyService:
    def __init__(self, bot: Bot, store: BindingStore, settings: Settings) -> None:
        self.bot = bot
        self.store = store
        self.settings = settings

    @property
    def _site_url(self) -> str:
        return (self.settings.public_site_url or messages.DEFAULT_SITE_URL).rstrip("/")

    async def _send(
        self,
        student_id: str,
        text: str,
        *,
        require_active: bool = True,
        reply_markup: Any = None,
    ) -> dict:
        binding = self.store.get_by_student(student_id)
        if binding is None or binding.chat_id is None:
            return {"ok": False, "error": "not_linked"}
        if require_active and not binding.bot_active:
            return {"ok": False, "error": "bot_inactive"}
        try:
            kwargs: dict[str, Any] = {}
            if reply_markup is not None:
                kwargs["reply_markup"] = reply_markup
            await send_text(self.bot, binding.chat_id, text, link_preview=False, **kwargs)
        except TelegramAPIError as exc:
            logger.warning("telegram send failed for %s: %s", student_id, exc)
            return {"ok": False, "error": "telegram_error", "detail": str(exc)}
        return {"ok": True, "chat_id": binding.chat_id}

    def _tutor_of(self, student_id: str, tutor_name: str | None) -> str | None:
        if tutor_name and tutor_name.strip():
            return tutor_name.strip()
        binding = self.store.get_by_student(student_id)
        return (binding.tutor_name if binding else None) or None

    def _lang_of(self, student_id: str) -> str:
        binding = self.store.get_by_student(student_id)
        return (binding.bot_lang if binding else None) or "en"

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
                lang=self._lang_of(student_id),
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
        balance_after: float | int | None = None,
        paid_at: str | None = None,
        timezone_name: str | None = None,
    ) -> dict:
        return await self._send(
            student_id,
            messages.payment(
                amount_label=amount_label,
                lessons_added=lessons_added,
                tutor_name=self._tutor_of(student_id, tutor_name),
                rate_unit=rate_unit,
                balance_after=balance_after,
                paid_at=paid_at,
                timezone_name=timezone_name,
                lang=self._lang_of(student_id),
                site_url=self._site_url,
            ),
        )

    async def lesson_start(
        self,
        student_id: str,
        *,
        minutes_before: int,
        time_label: str | None = None,
        scheduled_at: str | None = None,
        duration_minutes: int | float | None = 60,
        timezone_name: str | None = None,
        meeting_link: str | None = None,
        tutor_name: str | None = None,
        subject: str | None = None,
    ) -> dict:
        return await self._send(
            student_id,
            messages.lesson_start(
                minutes_before=minutes_before,
                time_label=time_label,
                scheduled_at=scheduled_at,
                duration_minutes=duration_minutes,
                timezone_name=timezone_name,
                meeting_link=meeting_link,
                tutor_name=self._tutor_of(student_id, tutor_name),
                subject=subject,
                lang=self._lang_of(student_id),
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
        from simple4u_bot.services.i18n_bot import t
        from simple4u_bot.services.translate import translate_text

        lang = self._lang_of(student_id)
        body = (text or "").strip()
        if not body:
            body = t(lang, "notify_homework_fallback")
        else:
            body = await translate_text(body, target_lang=lang)
        return await self._send(
            student_id,
            messages.homework(
                text=body,
                tutor_name=self._tutor_of(student_id, tutor_name),
                lang=lang,
                site_url=self._site_url,
            ),
        )

    async def lesson_moved(
        self,
        student_id: str,
        *,
        new_time_label: str | None = None,
        old_scheduled_at: str | None = None,
        new_scheduled_at: str | None = None,
        timezone_name: str | None = None,
        meeting_link: str | None = None,
        tutor_name: str | None = None,
        subject: str | None = None,
    ) -> dict:
        return await self._send(
            student_id,
            messages.lesson_moved(
                new_time_label=new_time_label,
                old_scheduled_at=old_scheduled_at,
                new_scheduled_at=new_scheduled_at,
                timezone_name=timezone_name,
                meeting_link=meeting_link,
                tutor_name=self._tutor_of(student_id, tutor_name),
                subject=subject,
                lang=self._lang_of(student_id),
                site_url=self._site_url,
            ),
        )

    async def unlinked_by_tutor(
        self,
        student_id: str,
        *,
        tutor_name: str | None = None,
    ) -> dict:
        """CRM tutor disconnected the student — notify before clearing the binding."""
        return await self._send(
            student_id,
            messages.unlinked_by_tutor(
                tutor_name=self._tutor_of(student_id, tutor_name),
                lang=self._lang_of(student_id),
                site_url=self._site_url,
            ),
            require_active=False,
            reply_markup=keyboards.remove_keyboard(),
        )
