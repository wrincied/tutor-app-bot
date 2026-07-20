from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

import uvicorn
from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from simple4u_bot.api.app import create_api
from simple4u_bot.config import get_settings
from simple4u_bot.handlers.student import router as student_router
from simple4u_bot.services.backend_client import BackendClient
from simple4u_bot.services.notify import NotifyService
from simple4u_bot.services.store import BindingStore

logger = logging.getLogger(__name__)


class InjectMiddleware(BaseMiddleware):
    def __init__(
        self,
        store: BindingStore,
        notify: NotifyService,
        backend: BackendClient,
    ) -> None:
        self.store = store
        self.notify = notify
        self.backend = backend

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        data["store"] = self.store
        data["notify"] = self.notify
        data["backend"] = self.backend
        return await handler(event, data)


async def run() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    settings = get_settings()
    store = BindingStore(settings.bot_db_path)

    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    notify = NotifyService(bot, store, settings)
    backend = BackendClient(settings)

    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(InjectMiddleware(store, notify, backend))
    dp.include_router(student_router)

    api = create_api(settings=settings, store=store, notify=notify)
    config = uvicorn.Config(
        api,
        host=settings.bot_http_host,
        port=settings.bot_http_port,
        log_level="info",
    )
    server = uvicorn.Server(config)

    logger.info(
        "Starting Simple4U bot · HTTP :%s · DB %s · backend %s",
        settings.bot_http_port,
        settings.bot_db_path,
        settings.backend_url,
    )

    await asyncio.gather(
        dp.start_polling(bot),
        server.serve(),
    )


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
