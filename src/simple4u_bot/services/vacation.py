from __future__ import annotations

from simple4u_bot.services.i18n_bot import t


def format_vacation_end_date(iso: str | None) -> str | None:
    raw = (iso or "").strip()
    if len(raw) < 10 or raw[4] != "-":
        return None
    try:
        year, month, day = raw.split("-", 2)
        return f"{day}.{month}.{year}"
    except ValueError:
        return raw


def vacation_body_from_profile(profile: dict | None, lang: str) -> str | None:
    if not profile or not profile.get("vacation_active"):
        return None
    custom = str(profile.get("vacation_message") or "").strip()
    if custom:
        return custom
    end_label = format_vacation_end_date(str(profile.get("vacation_end_date") or ""))
    if end_label:
        return t(lang, "vacation_default").format(end_date=end_label)
    return t(lang, "vacation_default_no_date")
