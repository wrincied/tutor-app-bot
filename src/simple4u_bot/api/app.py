from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from simple4u_bot.config import Settings
from simple4u_bot.services.notify import NotifyService
from simple4u_bot.services.store import BindingStore


class RegisterLinkBody(BaseModel):
    student_id: str = Field(min_length=1)
    link_token: str = Field(min_length=8)
    student_name: str | None = None
    bot_active: bool = True


class BotActiveBody(BaseModel):
    student_id: str
    bot_active: bool


class BalanceBody(BaseModel):
    student_id: str
    lessons_left: int = Field(ge=0)


class PaymentBody(BaseModel):
    student_id: str
    amount_label: str  # e.g. "€225"
    lessons_added: int = Field(ge=0)


class LessonStartBody(BaseModel):
    student_id: str
    minutes_before: int = Field(default=30, ge=1)
    time_label: str  # e.g. "11:30"


class HomeworkBody(BaseModel):
    student_id: str
    text: str = Field(min_length=1)


class LessonMovedBody(BaseModel):
    student_id: str
    new_time_label: str


def create_api(
    *,
    settings: Settings,
    store: BindingStore,
    notify: NotifyService,
) -> FastAPI:
    app = FastAPI(title="Simple4U Bot API", version="0.1.0")

    def require_secret(
        x_bot_secret: Annotated[str | None, Header(alias="X-Bot-Secret")] = None,
    ) -> None:
        if not x_bot_secret or x_bot_secret != settings.bot_api_secret:
            raise HTTPException(status_code=401, detail="invalid bot secret")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/links")
    async def register_link(
        body: RegisterLinkBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        store.upsert_link(
            student_id=body.student_id,
            link_token=body.link_token,
            student_name=body.student_name,
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
        return await notify.balance(body.student_id, body.lessons_left)

    @app.post("/v1/notify/payment")
    async def notify_payment(
        body: PaymentBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        return await notify.payment(
            body.student_id,
            amount_label=body.amount_label,
            lessons_added=body.lessons_added,
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
        )

    @app.post("/v1/notify/homework")
    async def notify_homework(
        body: HomeworkBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        return await notify.homework(body.student_id, text=body.text)

    @app.post("/v1/notify/lesson-moved")
    async def notify_lesson_moved(
        body: LessonMovedBody,
        _: Annotated[None, Depends(require_secret)] = None,
    ) -> dict:
        return await notify.lesson_moved(
            body.student_id,
            new_time_label=body.new_time_label,
        )

    return app