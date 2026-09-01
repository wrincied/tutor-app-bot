"""Message templates for student Telegram notifications (HTML)."""

from __future__ import annotations

import html

from simple4u_bot.services.i18n_bot import balance_reason_label, t, unit_word

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


def branded(
    title: str,
    subtitle: str,
    *body_lines: str,
    lang: str | None = None,
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
    return "\n".join(parts) + _footer(lang=lang, site_url=site_url)


def _tutor_line(tutor_name: str | None, lang: str | None = None) -> str:
    name = (tutor_name or "").strip()
    if not name:
        return ""
    return t(lang, "tutor_line").format(name=_esc(name))


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
    tutor = _tutor_line(tutor_name, lang)
    before = lessons_before
    if before is not None and float(before) != float(lessons_left):
        reason_label = balance_reason_label(lang, reason)
        reason_line = (
            t(lang, "notify_balance_reason").format(reason=_esc(reason_label))
            if reason_label
            else ""
        )
        return branded(
            t(lang, "notify_balance_changed_title"),
            t(lang, "notify_balance_changed_delta").format(
                before=_fmt_units(before),
                after=_fmt_units(lessons_left),
                unit=unit,
            ),
            t(lang, "notify_balance_remaining").format(
                count=_fmt_units(lessons_left),
                unit=unit,
            ),
            reason_line,
            tutor,
            lang=lang,
            site_url=site_url,
        )
    return branded(
        t(lang, "notify_balance_package_title"),
        t(lang, "notify_balance_package_body").format(
            count=_fmt_units(lessons_left),
            unit=unit,
        ),
        tutor,
        lang=lang,
        site_url=site_url,
    )


def payment(
    *,
    amount_label: str,
    lessons_added: float | int,
    tutor_name: str | None = None,
    rate_unit: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    unit = unit_word(lang, rate_unit)
    tutor = _tutor_line(tutor_name, lang)
    delta = float(lessons_added)
    if delta > 0:
        delta_label = f"+{_fmt_units(delta)} {unit}"
    elif delta < 0:
        delta_label = f"{_fmt_units(delta)} {unit}"
    else:
        delta_label = f"0 {unit}"
    return branded(
        t(lang, "notify_payment_title"),
        t(lang, "notify_payment_body").format(
            amount=_esc(amount_label),
            delta=delta_label,
            thanks=t(lang, "notify_payment_thanks"),
        ),
        tutor,
        lang=lang,
        site_url=site_url,
    )


def lesson_start(
    *,
    minutes_before: int,
    time_label: str,
    meeting_link: str | None = None,
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    with_tutor = ""
    if (tutor_name or "").strip():
        with_tutor = t(lang, "notify_lesson_start_with_tutor").format(name=_esc(tutor_name))
    body: list[str] = []
    if meeting_link:
        href = html.escape(meeting_link.strip(), quote=True)
        body.append(f'<a href="{href}">{_esc(t(lang, "notify_meeting_link"))}</a>')
    return branded(
        t(lang, "notify_lesson_start_title"),
        t(lang, "notify_lesson_start_body").format(
            minutes=minutes_before,
            with_tutor=with_tutor,
            time=_esc(time_label),
        ),
        *body,
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
    tutor = _tutor_line(tutor_name, lang)
    return branded(
        t(lang, "notify_homework_title"),
        _esc(text),
        tutor,
        lang=lang,
        site_url=site_url,
    )


def lesson_moved(
    *,
    new_time_label: str,
    meeting_link: str | None = None,
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    who = ""
    if (tutor_name or "").strip():
        who = t(lang, "notify_lesson_moved_who").format(name=_esc(tutor_name))
    body: list[str] = []
    if meeting_link:
        href = html.escape(meeting_link.strip(), quote=True)
        body.append(f'<a href="{href}">{_esc(t(lang, "notify_meeting_link"))}</a>')
    return branded(
        t(lang, "notify_lesson_moved_title"),
        t(lang, "notify_lesson_moved_body").format(
            who=who,
            time=_esc(new_time_label),
        ),
        *body,
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
    parts: list[str] = [f"<b>{icon} {_esc(title)}</b>", ""]
    text = (body or "").strip()
    if text:
        parts.extend(_esc(line) for line in text.splitlines() if line.strip())
    tutor = _tutor_line(tutor_name, lang)
    if tutor:
        parts.append(tutor)
    return "\n".join(parts) + _footer(lang=lang, site_url=site_url)


def home_dashboard(
    *,
    title: str,
    greeting: str,
    bullets: list[str],
    announcement: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    parts: list[str] = [f"<b>{_esc(title)}</b>", "", _esc(greeting)]
    for line in bullets:
        text = (line or "").strip()
        if text:
            parts.append(f"• {_esc(text)}")
    if announcement:
        parts.extend(["", _esc(announcement)])
    return "\n".join(parts) + _footer(lang=lang, site_url=site_url)


def vacation_notice(
    *,
    text: str,
    title: str,
    tutor_name: str | None = None,
    lang: str | None = None,
    site_url: str | None = None,
) -> str:
    tutor = _tutor_line(tutor_name, lang)
    return branded(
        title,
        _esc(text),
        tutor,
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
        t(lang, "welcome_linked_hello").format(name=_esc(student_name))
        if student_name
        else t(lang, "welcome_linked_hello_anon")
    )
    tutor = ""
    if (tutor_name or "").strip():
        tutor = t(lang, "welcome_linked_tutor").format(name=f"<b>{_esc(tutor_name)}</b>")
    return branded(
        t(lang, "brand_title"),
        t(lang, "welcome_linked_subtitle").format(hello=hello),
        tutor,
        t(lang, "welcome_linked_body"),
        lang=lang,
        site_url=site_url,
    )


def welcome_need_link(*, lang: str | None = None, site_url: str | None = None) -> str:
    return branded(
        t(lang, "brand_title"),
        t(lang, "welcome_need_link_hello"),
        t(lang, "welcome_need_link_body"),
        lang=lang,
        site_url=site_url,
    )
