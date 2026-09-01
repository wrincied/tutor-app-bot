from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from simple4u_bot.services.i18n_bot import LANG_META, LANGS, t


def main_menu(lang: str | None) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(lang, "btn_lessons")),
                KeyboardButton(text=t(lang, "btn_payment")),
            ],
            [KeyboardButton(text=t(lang, "btn_home"))],
        ],
        resize_keyboard=True,
    )


def home_actions_inline(lang: str | None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(lang, "btn_language"),
                    callback_data="home:language",
                ),
                InlineKeyboardButton(
                    text=t(lang, "btn_unlink"),
                    callback_data="home:unlink",
                ),
            ],
        ],
    )


def profile_menu(lang: str | None) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "btn_language"))],
            [KeyboardButton(text=t(lang, "btn_unlink"))],
            [KeyboardButton(text=t(lang, "btn_back"))],
        ],
        resize_keyboard=True,
    )


def language_inline() -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for code in LANGS:
        meta = LANG_META[code]
        row.append(
            InlineKeyboardButton(
                text=f"{meta['flag']} {meta['label']}",
                callback_data=f"lang:{code}",
            )
        )
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def unlink_confirm_inline(lang: str | None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(lang, "btn_confirm_unlink"),
                    callback_data="unlink:yes",
                ),
                InlineKeyboardButton(
                    text=t(lang, "btn_cancel"),
                    callback_data="unlink:no",
                ),
            ]
        ]
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
