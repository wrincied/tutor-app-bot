from __future__ import annotations

from aiogram import Bot
from aiogram.types import LinkPreviewOptions, Message

LINK_PREVIEW_OFF = LinkPreviewOptions(is_disabled=True)


async def send_text(
    bot: Bot,
    chat_id: int,
    text: str,
    *,
    link_preview: bool = False,
    **kwargs,
) -> None:
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        link_preview_options=None if link_preview else LINK_PREVIEW_OFF,
        **kwargs,
    )


async def reply_text(
    message: Message,
    text: str,
    *,
    link_preview: bool = False,
    **kwargs,
) -> Message:
    return await message.answer(
        text,
        link_preview_options=None if link_preview else LINK_PREVIEW_OFF,
        **kwargs,
    )
