"""Message templates for student Telegram notifications (HTML)."""

from __future__ import annotations

import html

DEFAULT_SITE_URL = "https://simple4u-64822.web.app"


def _esc(value: str | None) -> str:
    return html.escape((value or "").strip(), quote=False)


def _footer(*, site_url: str | None = None) -> str:
    url = (site_url or DEFAULT_SITE_URL).rstrip("/")
    safe_href = html.escape(url, quote=True)
    return f'\n\n<a href="{safe_href}">© Simple4U</a>'


def with_site_footer(text: str, *, site_url: str | None = None) -> str:
    """Append promo footer to an existing (possibly HTML) message."""
    return (text or "").rstrip() + _footer(site_url=site_url)


def branded(
    title: str,
    subtitle: str,
    *body_lines: str,
    site_url: str | None = None,
) -> str:
    """Title (bold) + subtitle + optional body + © Simple4U site link."""
    parts: list[str] = [f"<b>{_esc(title)}</b>"]
    sub = (subtitle or "").strip()
    if sub:
        parts.append(_esc(sub))
    for line in body_lines:
        text = (line or "").strip()
        if text:
            parts.append(text)
    return "\n".join(parts) + _footer(site_url=site_url)


def _tutor_line(tutor_name: str | None) -> str:
    name = (tutor_name or "").strip()
    return f"Репетитор: {_esc(name)}" if name else ""


def _fmt_units(value: float | int) -> str:
    n = float(value)
    if n == int(n):
        return str(int(n))
    return f"{n:.2f}".rstrip("0").rstrip(".")


def _unit_word(rate_unit: str | None, *, plural: bool = True) -> str:
    if (rate_unit or "").strip().lower() == "lesson":
        return "занятий" if plural else "занятие"
    return "ч"


_BALANCE_REASON_LABELS = {
    "no_show": "неявка на урок",
    "bonus": "бонусное занятие",
    "typo": "исправление",
}


def balance(
    *,
    lessons_left: float | int,
    tutor_name: str | None = None,
    rate_unit: str | None = None,
    lessons_before: float | int | None = None,
    reason: str | None = None,
    site_url: str | None = None,
) -> str:
    unit = _unit_word(rate_unit)
    tutor = _tutor_line(tutor_name)
    before = lessons_before
    if before is not None and float(before) != float(lessons_left):
        reason_key = (reason or "").strip().lower()
        reason_line = ""
        if reason_key in _BALANCE_REASON_LABELS:
            reason_line = f"Причина: {_esc(_BALANCE_REASON_LABELS[reason_key])}."
        return branded(
            "Баланс изменён",
            f"{_fmt_units(before)} → {_fmt_units(lessons_left)} {unit}.",
            f"Осталось {_fmt_units(lessons_left)} {unit}.",
            reason_line,
            tutor,
            site_url=site_url,
        )
    return branded(
        "Баланс пакета",
        f"В пакете осталось {_fmt_units(lessons_left)} {unit}.",
        tutor,
        site_url=site_url,
    )


def payment(
    *,
    amount_label: str,
    lessons_added: float | int,
    tutor_name: str | None = None,
    rate_unit: str | None = None,
    site_url: str | None = None,
) -> str:
    unit = _unit_word(rate_unit)
    tutor = _tutor_line(tutor_name)
    return branded(
        "Оплата получена",
        f"{_esc(amount_label)} · +{_fmt_units(lessons_added)} {unit}. Спасибо!",
        tutor,
        site_url=site_url,
    )


def lesson_start(
    *,
    minutes_before: int,
    time_label: str,
    meeting_link: str | None = None,
    tutor_name: str | None = None,
    site_url: str | None = None,
) -> str:
    who = f" с {_esc(tutor_name)}" if (tutor_name or "").strip() else ""
    body: list[str] = []
    if meeting_link:
        href = html.escape(meeting_link.strip(), quote=True)
        body.append(f'<a href="{href}">Ссылка на звонок</a>')
    return branded(
        "Скоро урок",
        f"Через {minutes_before} минут начинается урок{who} · {_esc(time_label)}",
        *body,
        site_url=site_url,
    )


def homework(*, text: str, tutor_name: str | None = None, site_url: str | None = None) -> str:
    tutor = _tutor_line(tutor_name)
    return branded(
        "Домашнее задание",
        _esc(text),
        tutor,
        site_url=site_url,
    )


def lesson_moved(
    *,
    new_time_label: str,
    meeting_link: str | None = None,
    tutor_name: str | None = None,
    site_url: str | None = None,
) -> str:
    who = f" ({_esc(tutor_name)})" if (tutor_name or "").strip() else ""
    body: list[str] = []
    if meeting_link:
        href = html.escape(meeting_link.strip(), quote=True)
        body.append(f'<a href="{href}">Ссылка на звонок</a>')
    return branded(
        "Урок перенесён",
        f"Новое время{who}: {_esc(new_time_label)}",
        *body,
        site_url=site_url,
    )


def welcome_linked(
    *,
    student_name: str | None = None,
    tutor_name: str | None = None,
    site_url: str | None = None,
) -> str:
    hello = f"Привет, {_esc(student_name)}!" if student_name else "Привет!"
    tutor = (
        f"Твой репетитор: <b>{_esc(tutor_name)}</b>."
        if (tutor_name or "").strip()
        else ""
    )
    return branded(
        "Simple4U",
        f"{hello} Уведомления подключены.",
        tutor,
        "Сюда будут приходить баланс, оплата, старт урока и домашка.",
        site_url=site_url,
    )


def welcome_need_link(*, site_url: str | None = None) -> str:
    return branded(
        "Simple4U",
        "Привет! Я бот Simple4U.",
        "Открой персональную ссылку от репетитора, чтобы получать уведомления.",
        site_url=site_url,
    )
