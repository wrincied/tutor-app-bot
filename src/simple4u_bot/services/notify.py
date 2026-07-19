from __future__ import annotations

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from simple4u_bot.services import messages
from simple4u_bot.services.store import BindingStore


class NotifyService:
    def __init__(self, bot: Bot, store: BindingStore) -> None:
        self.bot = bot
        self.store = store

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

    async def balance(self, student_id: str, lessons_left: int) -> dict:
        return await self._send(student_id, messages.balance(lessons_left=lessons_left))

    async def payment(
        self,
        student_id: str,
        *,
        amount_label: str,
        lessons_added: int,
    ) -> dict:
        return await self._send(
            student_id,
            messages.payment(amount_label=amount_label, lessons_added=lessons_added),
        )

    async def lesson_start(
        self,
        student_id: str,
        *,
        minutes_before: int,
        time_label: str,
    ) -> dict:
        return await self._send(
            student_id,
            messages.lesson_start(
                minutes_before=minutes_before,
                time_label=time_label,
            ),
        )

    async def homework(self, student_id: str, *, text: str) -> dict:
        return await self._send(student_id, messages.homework(text=text))

    async def lesson_moved(self, student_id: str, *, new_time_label: str) -> dict:
        return await self._send(
            student_id,
            messages.lesson_moved(new_time_label=new_time_label),
        )
