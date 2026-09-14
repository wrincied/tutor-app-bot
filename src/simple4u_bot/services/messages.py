"""Message templates for student Telegram notifications (HTML)."""

from __future__ import annotations

import html
from collections.abc import Sequence

from simple4u_bot.services.i18n_bot import balance_reason_label, t, unit_word
from simple4u_bot.services.time_format import (
    format_moved,
    format_new_clock_only,
    format_range,
)

DEFAULT_SITE_URL = "https://simple4u.at"


def _esc(value: str | None) -> str:
    return html.escape((value or "").strip(), quote=False)


def _footer(*, lang: str | None = None, site_url: str | None = None) -> str:
    url = (site_url or DEFAULT_SITE_URL).rstrip("/")
    safe_href = html.escape(url, quote=True)
    label = _esc(t(lang, "footer_brand"))
    return f'\n\n<a href="{safe_href}">{label}</a>'


def with_site_footer(text: str, *, lang: str | None = None, site_url: str | None = None) -> str:
    """Append promo footer to an existing (possibly HTML) message."""
    return (text or "").rstrip() + _footer(lang=lang, site_url=site_url)


def _tutor_line(tutor_name: str | None, lang: str | None = None) -> str:
    name = (tutor_name or "").strip()
    if not name:
        return ""
    return t(lang, "tutor_line").format(name=_esc(name))


def compose_message(
    *,
    icon: str,
    title: str,
    body_lines: Sequence[str | None] = (),
    html_lines: Sequence[str | None] = (),
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    """
    Unified shell:
      [ICON] Title

      primary facts...

      Tutor: Name

      © Simple4U
    """
    head = f"{(icon or '').strip()} {_esc(title)}".strip()
    parts: list[str] = [f"<b>{head}</b>", ""]
    for raw in body_lines:
        if raw is None:
            continue
        text = str(raw).rstrip()
        if not text:
            parts.append("")
            continue
        parts.append(_esc(text))
    for raw in html_lines:
        if raw is None:
            continue
        text = str(raw).rstrip()
        if text:
            parts.append(text)
    tutor = _tutor_line(tutor_name, lang)
    if tutor:
        if parts and parts[-1] != "":
            parts.append("")
        parts.append(tutor)
    # Drop trailing blank lines before footer
    while len(parts) > 1 and parts[-1] == "":
        parts.pop()
    return "\n".join(parts) + _footer(lang=lang, site_url=site_url)


def branded(
    title: str,
    subtitle: str,
    *body_lines: str,
    icon: str = "",
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    """Legacy helper → unified shell (title may already include emoji)."""
    lines = [subtitle, *body_lines]
    # If caller put tutor HTML-escaped line in body, keep it as body; prefer compose.
    return compose_message(
        icon=icon,
        title=title,
        body_lines=[ln for ln in lines if (ln or "").strip()],
        lang=lang,
        site_url=site_url,
    )


def _fmt_units(value: float | int) -> str:
    n = float(value)
    if n == int(n):
        return str(int(n))
    return f"{n:.2f}".rstrip("0").rstrip(".")


def balance(
    *,
    lessons_left: float | int,
    tutor_name: str | None = None,
    rate_unit: str | None = None,
    lessons_before: float | int | None = None,
    reason: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    unit = unit_word(lang, rate_unit)
    before = lessons_before
    reason_key = str(reason or "").strip().lower()
    left = float(lessons_left)

    if before is not None and float(before) != left:
        reason_label = balance_reason_label(lang, reason)
        lines = [
            t(lang, "notify_balance_changed_delta").format(
                before=_fmt_units(before),
                after=_fmt_units(lessons_left),
                unit=unit,
            ),
        ]
        if reason_label:
            lines.append(t(lang, "notify_balance_reason").format(reason=reason_label))
        lines.append("")
        lines.append(
            t(lang, "notify_balance_remaining").format(
                count=_fmt_units(lessons_left),
                unit=unit,
            ),
        )
        return compose_message(
            icon="💳",
            title=t(lang, "notify_balance_changed_title"),
            body_lines=lines,
            tutor_name=tutor_name,
            lang=lang,
            site_url=site_url,
        )

    if reason_key == "low_balance":
        if left <= 0:
            return compose_message(
                icon="⚠️",
                title=t(lang, "notify_balance_empty_title"),
                body_lines=[
                    t(lang, "notify_balance_empty_body"),
                    t(lang, "notify_balance_empty_hint"),
                ],
                tutor_name=tutor_name,
                lang=lang,
                site_url=site_url,
            )
        return compose_message(
            icon="⚠️",
            title=t(lang, "notify_balance_low_title"),
            body_lines=[
                t(lang, "notify_balance_low_lead"),
                t(lang, "notify_balance_low_body").format(
                    count=_fmt_units(lessons_left),
                    unit=unit,
                ),
            ],
            tutor_name=tutor_name,
            lang=lang,
            site_url=site_url,
        )

    return compose_message(
        icon="💳",
        title=t(lang, "notify_balance_package_title"),
        body_lines=[
            t(lang, "notify_balance_package_body").format(
                count=_fmt_units(lessons_left),
                unit=unit,
            ),
        ],
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )


def payment(
    *,
    amount_label: str,
    lessons_added: float | int,
    tutor_name: str | None = None,
    rate_unit: str | None = None,
    balance_after: float | int | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    unit = unit_word(lang, rate_unit)
    delta = float(lessons_added)
    if delta > 0:
        delta_label = f"+{_fmt_units(delta)} {unit}"
    elif delta < 0:
        delta_label = f"{_fmt_units(delta)} {unit}"
    else:
        delta_label = f"0 {unit}"
    amount = (amount_label or "").strip()
    headline = f"{delta_label} · {amount}" if amount else delta_label
    lines = [headline, ""]
    if balance_after is not None:
        lines.append(
            t(lang, "notify_payment_new_balance").format(
                count=_fmt_units(balance_after),
                unit=unit,
            ),
        )
    return compose_message(
        icon="✅",
        title=t(lang, "notify_payment_title"),
        body_lines=lines,
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )


def lesson_start(
    *,
    minutes_before: int,
    time_label: str | None = None,
    scheduled_at: str | None = None,
    duration_minutes: int | float | None = 60,
    timezone_name: str | None = None,
    meeting_link: str | None = None,
    tutor_name: str | None = None,
    subject: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    when = (
        format_range(
            scheduled_at,
            duration_minutes=duration_minutes,
            timezone_name=timezone_name,
            lang=lang,
        )
        if scheduled_at
        else (time_label or "—")
    )
    lines: list[str | None] = [
        t(lang, "notify_lesson_start_body").format(minutes=minutes_before),
        "",
        when,
    ]
    if (subject or "").strip():
        lines.append(subject.strip())
    html_lines: list[str | None] = []
    if meeting_link:
        href = html.escape(meeting_link.strip(), quote=True)
        html_lines.append(f'<a href="{href}">{_esc(t(lang, "notify_meeting_link"))}</a>')
    return compose_message(
        icon="⏰",
        title=t(lang, "notify_lesson_start_title"),
        body_lines=lines,
        html_lines=html_lines,
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )


def homework(
    *,
    text: str,
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    return compose_message(
        icon="📝",
        title=t(lang, "notify_homework_title"),
        body_lines=[text],
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )


def lesson_moved(
    *,
    new_time_label: str | None = None,
    old_scheduled_at: str | None = None,
    new_scheduled_at: str | None = None,
    timezone_name: str | None = None,
    meeting_link: str | None = None,
    tutor_name: str | None = None,
    subject: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    if old_scheduled_at or new_scheduled_at:
        moved = format_moved(
            old_scheduled_at,
            new_scheduled_at or new_time_label,
            timezone_name=timezone_name,
            lang=lang,
        )
        new_clock = format_new_clock_only(new_scheduled_at, timezone_name=timezone_name)
    else:
        moved = new_time_label or "—"
        new_clock = new_time_label or "—"
    lines: list[str | None] = [
        moved,
        "",
        t(lang, "notify_lesson_moved_body").format(time=new_clock),
    ]
    if (subject or "").strip():
        lines.insert(1, subject.strip())
    html_lines: list[str | None] = []
    if meeting_link:
        href = html.escape(meeting_link.strip(), quote=True)
        html_lines.append(f'<a href="{href}">{_esc(t(lang, "notify_meeting_link"))}</a>')
    return compose_message(
        icon="📅",
        title=t(lang, "notify_lesson_moved_title"),
        body_lines=lines,
        html_lines=html_lines,
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )


def section_screen(
    *,
    icon: str,
    title: str,
    body: str,
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    lines = (body or "").splitlines()
    return compose_message(
        icon=icon,
        title=title,
        body_lines=lines if any(ln.strip() for ln in lines) else [body],
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )


def lessons_screen(
    *,
    title: str,
    blocks: list[tuple[str, str, str]],
    empty_text: str | None = None,
    page_label: str | None = None,
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    """Two-line lesson cards: date · start–end / subject · status + bold price."""
    parts_html: list[str | None] = []
    if page_label:
        parts_html.append(_esc(page_label))
        parts_html.append("")
    if not blocks:
        if empty_text:
            parts_html.append(_esc(empty_text))
    else:
        for index, (when_line, meta_line, price_label) in enumerate(blocks):
            if index:
                parts_html.append("")
            parts_html.append(_esc(when_line))
            meta = _esc(meta_line)
            price = _esc(price_label)
            if meta and price:
                parts_html.append(f"{meta}{'\u00a0' * 6}<b>{price}</b>")
            elif meta:
                parts_html.append(meta)
            elif price:
                parts_html.append(f"<b>{price}</b>")
    return compose_message(
        icon="📚",
        title=title,
        html_lines=parts_html,
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )


def home_dashboard(
    *,
    title: str,
    greeting: str,
    bullets: list[str],
    announcement: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    lines: list[str | None] = [greeting, ""]
    for line in bullets:
        text = (line or "").strip()
        if text:
            lines.append(text)
    if announcement:
        lines.extend(["", announcement])
    return compose_message(
        icon="🏠",
        title=title,
        body_lines=lines,
        lang=lang,
        site_url=site_url,
    )


def vacation_notice(
    *,
    text: str,
    title: str,
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    return compose_message(
        icon="🌴",
        title=title,
        body_lines=[text],
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )


def welcome_linked(
    *,
    student_name: str | None = None,
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    hello = (
        t(lang, "welcome_linked_hello").format(name=student_name)
        if student_name
        else t(lang, "welcome_linked_hello_anon")
    )
    lines = [
        t(lang, "welcome_linked_subtitle").format(hello=hello),
        t(lang, "welcome_linked_body"),
    ]
    return compose_message(
        icon="✨",
        title=t(lang, "brand_title"),
        body_lines=lines,
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )


def welcome_need_link(*, lang: str | None = None, site_url: str | None = None) -> str:
    return compose_message(
        icon="✨",
        title=t(lang, "brand_title"),
        body_lines=[
            t(lang, "welcome_need_link_hello"),
            t(lang, "welcome_need_link_body"),
        ],
        lang=lang,
        site_url=site_url,
    )


def unlinked_by_tutor(
    *,
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    return compose_message(
        icon="🔕",
        title=t(lang, "unlinked_by_tutor_title"),
        body_lines=[t(lang, "unlinked_by_tutor_body")],
        tutor_name=tutor_name,
        lang=lang,
        site_url=site_url,
    )

