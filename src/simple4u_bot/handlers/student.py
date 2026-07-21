from __future__ import annotations

from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message

from simple4u_bot import keyboards
from simple4u_bot.config import get_settings
from simple4u_bot.services import messages
from simple4u_bot.services.backend_client import BackendClient
from simple4u_bot.services.i18n_bot import LANG_META, normalize_lang, status_label, t
from simple4u_bot.services.store import Binding, BindingStore

router = Router(name="student")


def _site_url() -> str:
    return (get_settings().public_site_url or messages.DEFAULT_SITE_URL).rstrip("/")


def _tutor_name(binding: Binding | None) -> str | None:
    name = (binding.tutor_name if binding else None) or ""
    name = name.strip()
    return name or None


def _with_tutor(lang: str, text: str, binding: Binding | None) -> str:
    tutor = _tutor_name(binding)
    if not tutor:
        return text
    return f"{text}\n{t(lang, 'tutor_line').format(name=tutor)}"


def _display_name(message: Message) -> str | None:
    user = message.from_user
    if user is None:
        return None
    parts = [user.first_name or "", user.last_name or ""]
    name = " ".join(p for p in parts if p).strip()
    return name or None


def _lang_of(binding: Binding | None) -> str:
    return normalize_lang(binding.bot_lang if binding else None)


def _match_action(text: str, lang: str) -> str | None:
    mapping = {
        t(lang, "btn_lessons"): "lessons",
        t(lang, "btn_payment"): "payment",
        t(lang, "btn_profile"): "profile",
        t(lang, "btn_language"): "language",
        t(lang, "btn_unlink"): "unlink",
        t(lang, "btn_back"): "back",
    }
    # Also accept labels from all languages (user may switch mid-session).
    if text in mapping:
        return mapping[text]
    for code in ("ru", "en", "de", "kz", "uk", "by"):
        for key, action in (
            ("btn_lessons", "lessons"),
            ("btn_payment", "payment"),
            ("btn_profile", "profile"),
            ("btn_language", "language"),
            ("btn_unlink", "unlink"),
            ("btn_back", "back"),
        ):
            if text == t(code, key):
                return action
    return None


def _format_lesson_line(lang: str, item: dict, timezone: str) -> str:
    raw = item.get("scheduledAt")
    when = "—"
    if raw:
        try:
            dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            when = dt.strftime("%d.%m.%Y %H:%M")
        except ValueError:
            when = str(raw)[:16]
    st = status_label(lang, str(item.get("status") or "scheduled"))
    price = item.get("price")
    currency = item.get("currency") or "EUR"
    try:
        price_label = f"{float(price):g} {currency}"
    except (TypeError, ValueError):
        price_label = f"— {currency}"
    return f"• {when} · {st} · {price_label}"


async def _require_binding(message: Message, store: BindingStore) -> Binding | None:
    if message.chat is None:
        return None
    binding = store.get_by_chat(message.chat.id)
    if binding is None:
        await message.answer(t("ru", "not_linked"))
        return None
    return binding


@router.message(CommandStart(deep_link=True))
async def start_with_token(
    message: Message,
    command: CommandObject,
    store: BindingStore,
    backend: BackendClient,
) -> None:
    token = (command.args or "").strip()
    if not token or message.chat is None or message.from_user is None:
        await message.answer(t("ru", "need_link"))
        return

    binding = store.bind_chat(
        link_token=token,
        chat_id=message.chat.id,
        telegram_user_id=str(message.from_user.id),
        telegram_username=message.from_user.username,
        telegram_display_name=_display_name(message),
    )
    if binding is None:
        await message.answer(t("ru", "need_link"))
        return

    await backend.notify_linked(
        {
            "student_id": binding.student_id,
            "telegram_user_id": binding.telegram_user_id,
            "telegram_username": binding.telegram_username,
            "telegram_display_name": binding.telegram_display_name,
            "telegram_chat_id": str(binding.chat_id),
        }
    )
    profile = await backend.get_profile(binding.student_id)
    lang = normalize_lang((profile or {}).get("bot_lang") or binding.bot_lang)
    store.set_lang(binding.student_id, lang)
    profile_tutor = (profile or {}).get("tutor_name") if profile else None
    if profile_tutor:
        store.set_tutor_name(binding.student_id, str(profile_tutor))
        binding = store.get_by_chat(message.chat.id) or binding
    name = f", {binding.student_name}" if binding.student_name else ""
    await message.answer(
        messages.branded(
            "Simple4U",
            _with_tutor(lang, t(lang, "welcome").format(name=name), binding),
            site_url=_site_url(),
        ),
        reply_markup=keyboards.main_menu(lang),
    )


@router.message(CommandStart())
async def start_plain(message: Message, store: BindingStore, backend: BackendClient) -> None:
    if message.chat is None:
        return
    existing = store.get_by_chat(message.chat.id)
    if existing is not None:
        profile = await backend.get_profile(existing.student_id)
        profile_tutor = (profile or {}).get("tutor_name") if profile else None
        if profile_tutor:
            store.set_tutor_name(existing.student_id, str(profile_tutor))
            existing = store.get_by_chat(message.chat.id) or existing
        lang = _lang_of(existing)
        name = f", {existing.student_name}" if existing.student_name else ""
        await message.answer(
            messages.branded(
                "Simple4U",
                _with_tutor(lang, t(lang, "welcome").format(name=name), existing),
                site_url=_site_url(),
            ),
            reply_markup=keyboards.main_menu(lang),
        )
        return
    await message.answer(messages.welcome_need_link(site_url=_site_url()))


@router.message(Command("status"))
async def status(message: Message, store: BindingStore) -> None:
    if message.chat is None:
        return
    binding = store.get_by_chat(message.chat.id)
    if binding is None:
        await message.answer(t("ru", "need_link"))
        return
    lang = _lang_of(binding)
    state = "ON" if binding.bot_active else "OFF"
    await message.answer(
        f"{t(lang, 'profile_title')} · `{binding.student_id}` · bot {state}",
        reply_markup=keyboards.main_menu(lang),
    )


@router.message(F.text)
async def menu_text(
    message: Message,
    store: BindingStore,
    backend: BackendClient,
) -> None:
    if message.chat is None or not message.text:
        return
    binding = store.get_by_chat(message.chat.id)
    if binding is None:
        await message.answer(t("ru", "not_linked"))
        return

    lang = _lang_of(binding)
    action = _match_action(message.text.strip(), lang)
    if action is None:
        await message.answer(t(lang, "menu_hint"), reply_markup=keyboards.main_menu(lang))
        return

    if action == "back":
        await message.answer(t(lang, "menu_hint"), reply_markup=keyboards.main_menu(lang))
        return

    if action == "lessons":
        data = await backend.get_lessons(binding.student_id)
        if data is None:
            await message.answer(t(lang, "error"), reply_markup=keyboards.main_menu(lang))
            return
        items = data.get("items") or []
        if not items:
            await message.answer(t(lang, "lessons_empty"), reply_markup=keyboards.main_menu(lang))
            return
        tz = str(data.get("timezone") or "UTC")
        header = _with_tutor(lang, t(lang, "lessons_title"), binding)
        lines = [header, ""]
        for item in items:
            if isinstance(item, dict):
                lines.append(_format_lesson_line(lang, item, tz))
        await message.answer("\n".join(lines), reply_markup=keyboards.main_menu(lang))
        return

    if action == "payment":
        data = await backend.get_payment_summary(binding.student_id)
        if data is None:
            await message.answer(t(lang, "error"), reply_markup=keyboards.main_menu(lang))
            return
        billing = data.get("billing_type") or "package"
        key = "payment_postpaid" if billing == "postpaid" else "payment_package"
        is_lesson_unit = data.get("rate_unit") == "lesson" or data.get("balance_unit") == "lesson"
        text = t(lang, key).format(
            topped=data.get("lessons_topped_up", 0),
            completed=data.get("lessons_completed", 0),
            balance=data.get("balance_lessons", 0),
            unpaid=data.get("unpaid_lessons_count", 0),
            credit=data.get("credit_limit", 0),
            rate=data.get("rate_per_hour", 0),
            currency=data.get("rate_currency", "EUR"),
            rate_unit=t(lang, "rate_unit_lesson" if is_lesson_unit else "rate_unit_hour"),
            balance_unit=t(
                lang, "balance_unit_lesson" if is_lesson_unit else "balance_unit_hour"
            ),
        )
        await message.answer(
            f"{_with_tutor(lang, t(lang, 'payment_title'), binding)}\n\n{text}",
            reply_markup=keyboards.main_menu(lang),
        )
        return

    if action == "profile":
        meta = LANG_META[normalize_lang(lang)]
        text = _with_tutor(
            lang,
            f"{t(lang, 'profile_title')}\n"
            f"{t(lang, 'profile_lang').format(flag=meta['flag'], label=meta['label'])}",
            binding,
        )
        await message.answer(text, reply_markup=keyboards.profile_menu(lang))
        return

    if action == "language":
        await message.answer(t(lang, "pick_lang"), reply_markup=keyboards.language_inline())
        return

    if action == "unlink":
        await message.answer(
            t(lang, "unlink_confirm"),
            reply_markup=keyboards.unlink_confirm_inline(lang),
        )


@router.callback_query(F.data.startswith("lang:"))
async def on_lang(
    query: CallbackQuery,
    store: BindingStore,
    backend: BackendClient,
) -> None:
    if query.message is None or query.from_user is None or not query.data:
        await query.answer()
        return
    code = query.data.split(":", 1)[1]
    lang = normalize_lang(code)
    binding = store.get_by_chat(query.message.chat.id)
    if binding is None:
        await query.answer()
        await query.message.answer(t("ru", "not_linked"))
        return
    store.set_lang(binding.student_id, lang)
    await backend.set_language(binding.student_id, lang)
    meta = LANG_META[lang]
    await query.answer()
    await query.message.answer(
        t(lang, "lang_set").format(flag=meta["flag"], label=meta["label"]),
        reply_markup=keyboards.main_menu(lang),
    )


@router.callback_query(F.data.startswith("unlink:"))
async def on_unlink(
    query: CallbackQuery,
    store: BindingStore,
    backend: BackendClient,
) -> None:
    if query.message is None or not query.data:
        await query.answer()
        return
    decision = query.data.split(":", 1)[1]
    binding = store.get_by_chat(query.message.chat.id)
    lang = _lang_of(binding)
    if decision != "yes":
        await query.answer()
        if binding:
            await query.message.answer(t(lang, "menu_hint"), reply_markup=keyboards.main_menu(lang))
        return
    if binding is None:
        await query.answer()
        return

    await backend.notify_unlinked(
        {
            "student_id": binding.student_id,
            "telegram_user_id": binding.telegram_user_id,
            "telegram_username": binding.telegram_username,
            "telegram_chat_id": str(binding.chat_id),
        }
    )
    store.unlink_chat(binding.chat_id)
    await query.answer()
    await query.message.answer(t(lang, "unlinked"), reply_markup=keyboards.remove_keyboard())
