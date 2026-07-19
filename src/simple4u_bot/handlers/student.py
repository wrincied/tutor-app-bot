from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message

from simple4u_bot.services import messages
from simple4u_bot.services.store import BindingStore

router = Router(name="student")


@router.message(CommandStart(deep_link=True))
async def start_with_token(
    message: Message,
    command: CommandObject,
    store: BindingStore,
) -> None:
    token = (command.args or "").strip()
    if not token or message.chat is None:
        await message.answer(messages.welcome_need_link())
        return

    binding = store.bind_chat(link_token=token, chat_id=message.chat.id)
    if binding is None:
        await message.answer(messages.welcome_need_link())
        return

    await message.answer(messages.welcome_linked(student_name=binding.student_name))


@router.message(CommandStart())
async def start_plain(message: Message, store: BindingStore) -> None:
    if message.chat is None:
        return
    existing = store.get_by_chat(message.chat.id)
    if existing is not None:
        await message.answer(messages.welcome_linked(student_name=existing.student_name))
        return
    await message.answer(messages.welcome_need_link())


@router.message(Command("status"))
async def status(message: Message, store: BindingStore) -> None:
    if message.chat is None:
        return
    binding = store.get_by_chat(message.chat.id)
    if binding is None:
        await message.answer(messages.welcome_need_link())
        return
    state = "включены" if binding.bot_active else "выключены"
    await message.answer(
        f"Связка активна · ученик `{binding.student_id}` · уведомления {state}."
    )
