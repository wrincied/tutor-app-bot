from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Annotated, Any

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from simple4u_bot.config import Settings
from simple4u_bot.services.notify import NotifyService
from simple4u_bot.services.store_factory import BindingStoreProtocol

logger = logging.getLogger(__name__)


class RegisterLinkBody(BaseModel):
    student_id: str = Field(min_length=1)
    link_token: str = Field(min_length=8)
    student_name: str | None = None
    tutor_name: str | None = None
    bot_active: bool = True


class BotActiveBody(BaseModel):
    student_id: str
    bot_active: bool


class BalanceBody(BaseModel):
    student_id: str
    lessons_left: float
    tutor_name: str | None = None
    rate_unit: str | None = None
    lessons_before: float | None = None
    reason: str | None = None


class PaymentBody(BaseModel):
    student_id: str
    amount_label: str
    lessons_added: float = 0
    tutor_name: str | None = None
    rate_unit: str | None = None


class LessonStartBody(BaseModel):
    student_id: str
    minutes_before: int = Field(default=30, ge=1)
    time_label: str
    meeting_link: str | None = None
    tutor_name: str | None = None


class HomeworkBody(BaseModel):
    student_id: str
    text: str = Field(min_length=1)
    tutor_name: str | None = None


class LessonMovedBody(BaseModel):
    student_id: str
    new_time_label: str
    meeting_link: str | None = None
    tutor_name: str | None = None


class UnlinkBody(BaseModel):
    student_id: str = Field(min_length=1)


def create_api(
    *,
    settings: Settings,
    store: BindingStoreProtocol,
    notify: NotifyService,
    bot: Bot | None = None,
    dp: Dispatcher | None = None,
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        del app
        if settings.bot_mode == "webhook" and bot is not None:
            if not settings.webhook_url or not settings.webhook_secret:
                raise RuntimeError("WEBHOOK_BASE_URL and WEBHOOK_SECRET are required in webhook mode")
            await bot.set_webhook(
                url=settings.webhook_url,
                secret_token=settings.webhook_secret,
                drop_pending_updates=True,
            )
            logger.info("Telegram webhook registered: %s", settings.webhook_url)
        yield
        if settings.bot_mode == "webhook" and bot is not None:
            await bot.delete_webhook()
            logger.info("Telegram webhook removed")

    app = FastAPI(title="Simple4U Bot API", version="0.1.0", lifespan=lifespan)

    def require_secret(
        x_bot_secret: Annotated[str | None, Header(alias="X-Bot-Secret")] = None,
    ) -> None:
        if not x_bot_secret or x_bot_secret != settings.bot_api_secret:
            raise HTTPException(status_code=401, detail="invalid bot secret")

    if bot is not None and dp is not None and settings.bot_mode == "webhook":

        @app.post(settings.webhook_path)
        async def telegram_webhook(
            request: Request,
            x_telegram_bot_api_secret_token: Annotated[
                str | None, Header(alias="X-Telegram-Bot-Api-Secret-Token")
            ] = None,
        ) -> dict[str, bool]:
            if x_telegram_bot_api_secret_token != settings.webhook_secret:
                raise HTTPException(status_code=403, detail="invalid webhook secret")
            payload: dict[str, Any] = await request.json()
            update = Update.model_validate(payload, context={"bot": bot})
            await dp.feed_update(bot, update)
            return {"ok": True}

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "mode": settings.bot_mode}

    @app.post("/v1/links")
    async def register_link(
        body: RegisterLinkBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        store.upsert_link(
            student_id=body.student_id,
            link_token=body.link_token,
            student_name=body.student_name,
            tutor_name=body.tutor_name,
            bot_active=body.bot_active,
        )
        deep_link = f"https://t.me/{settings.bot_username}?start={body.link_token}"
        return {"ok": True, "deep_link": deep_link}

    @app.post("/v1/bot-active")
    async def set_bot_active(
        body: BotActiveBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        updated = store.set_bot_active(body.student_id, body.bot_active)
        if not updated:
            raise HTTPException(status_code=404, detail="student not found")
        return {"ok": True}

    @app.post("/v1/notify/balance")
    async def notify_balance(
        body: BalanceBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        return await notify.balance(
            body.student_id,
            body.lessons_left,
            tutor_name=body.tutor_name,
            rate_unit=body.rate_unit,
            lessons_before=body.lessons_before,
            reason=body.reason,
        )

    @app.post("/v1/notify/payment")
    async def notify_payment(
        body: PaymentBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        return await notify.payment(
            body.student_id,
            amount_label=body.amount_label,
            lessons_added=body.lessons_added,
            tutor_name=body.tutor_name,
            rate_unit=body.rate_unit,
        )

    @app.post("/v1/notify/lesson-start")
    async def notify_lesson_start(
        body: LessonStartBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        return await notify.lesson_start(
            body.student_id,
            minutes_before=body.minutes_before,
            time_label=body.time_label,
            meeting_link=body.meeting_link,
            tutor_name=body.tutor_name,
        )

    @app.post("/v1/notify/homework")
    async def notify_homework(
        body: HomeworkBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        return await notify.homework(
            body.student_id,
            text=body.text,
            tutor_name=body.tutor_name,
        )

    @app.post("/v1/notify/lesson-moved")
    async def notify_lesson_moved(
        body: LessonMovedBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        return await notify.lesson_moved(
            body.student_id,
            new_time_label=body.new_time_label,
            meeting_link=body.meeting_link,
            tutor_name=body.tutor_name,
        )

    @app.post("/v1/unlink")
    async def unlink_student(
        body: UnlinkBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        store.unlink_student(body.student_id)
        return {"ok": True, "student_id": body.student_id}

    @app.get("/v1/bindings/{student_id}")
    async def get_binding(
        student_id: str,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        binding = store.get_by_student(student_id)
        if binding is None:
            raise HTTPException(status_code=404, detail="not linked")
        return {
            "ok": True,
            "student_id": binding.student_id,
            "chat_id": binding.chat_id,
            "telegram_user_id": binding.telegram_user_id,
            "telegram_username": binding.telegram_username,
            "telegram_display_name": binding.telegram_display_name,
            "bot_active": binding.bot_active,
            "tutor_name": binding.tutor_name,
        }

    return app
