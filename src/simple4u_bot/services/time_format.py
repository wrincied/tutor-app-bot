"""Locale-aware lesson time labels for bot messages (de / en / ru)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone as dt_timezone
from zoneinfo import ZoneInfo

from simple4u_bot.services.i18n_bot import normalize_lang

_MONTH_SHORT: dict[str, tuple[str, ...]] = {
    "de": (
        "Jan",
        "Feb",
        "Mär",
        "Apr",
        "Mai",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Okt",
        "Nov",
        "Dez",
    ),
    "en": (
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ),
    "ru": (
        "янв",
        "фев",
        "мар",
        "апр",
        "мая",
        "июн",
        "июл",
        "авг",
        "сен",
        "окт",
        "ноя",
        "дек",
    ),
}


def parse_iso(raw: object | None) -> datetime | None:
    if raw is None:
        return None
    try:
        dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=dt_timezone.utc)
    return dt


def to_local(dt: datetime, timezone_name: str | None) -> datetime:
    try:
        zone = ZoneInfo(timezone_name or "UTC")
    except Exception:
        return dt.astimezone(dt_timezone.utc)
    return dt.astimezone(zone)


def _date_part(local: datetime, lang: str | None) -> str:
    code = normalize_lang(lang)
    if code not in _MONTH_SHORT:
        code = "en"
    month = _MONTH_SHORT[code][local.month - 1]
    day = local.day
    year_now = datetime.now(tz=local.tzinfo).year
    if local.year != year_now:
        if code == "de":
            return f"{day:02d}. {month} {local.year}"
        return f"{day:02d} {month} {local.year}"
    if code == "de":
        return f"{day:02d}. {month}"
    return f"{day:02d} {month}"


def _hm(local: datetime) -> str:
    return local.strftime("%H:%M")


def format_range(
    start_raw: object | None,
    *,
    duration_minutes: int | float | None = 60,
    timezone_name: str | None = "UTC",
    lang: str | None = None,
) -> str:
    start = parse_iso(start_raw)
    if start is None:
        return str(start_raw or "—")[:16]
    local = to_local(start, timezone_name)
    minutes = int(duration_minutes) if duration_minutes else 60
    if minutes <= 0:
        minutes = 60
    end = local + timedelta(minutes=minutes)
    return f"{_date_part(local, lang)} · {_hm(local)}–{_hm(end)}"


def format_clock(
    start_raw: object | None,
    *,
    timezone_name: str | None = "UTC",
    lang: str | None = None,
) -> str:
    start = parse_iso(start_raw)
    if start is None:
        return str(start_raw or "—")[:16]
    local = to_local(start, timezone_name)
    return f"{_date_part(local, lang)} · {_hm(local)}"


def format_moved(
    old_raw: object | None,
    new_raw: object | None,
    *,
    timezone_name: str | None = "UTC",
    lang: str | None = None,
) -> str:
    old_dt = parse_iso(old_raw)
    new_dt = parse_iso(new_raw)
    if old_dt is None and new_dt is None:
        return "—"
    if old_dt is None:
        return format_clock(new_raw, timezone_name=timezone_name, lang=lang)
    if new_dt is None:
        return format_clock(old_raw, timezone_name=timezone_name, lang=lang)

    old_l = to_local(old_dt, timezone_name)
    new_l = to_local(new_dt, timezone_name)
    if old_l.date() == new_l.date():
        return f"{_date_part(old_l, lang)} · {_hm(old_l)} → {_hm(new_l)}"
    return (
        f"{_date_part(old_l, lang)} · {_hm(old_l)} → "
        f"{_date_part(new_l, lang)} · {_hm(new_l)}"
    )


def format_new_clock_only(
    new_raw: object | None,
    *,
    timezone_name: str | None = "UTC",
) -> str:
    start = parse_iso(new_raw)
    if start is None:
        return "—"
    return _hm(to_local(start, timezone_name))
