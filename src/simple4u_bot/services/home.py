from __future__ import annotations

from simple4u_bot.services import messages
from simple4u_bot.services.i18n_bot import t
from simple4u_bot.services.vacation import vacation_body_from_profile

_CURRENCY_SYMBOL: dict[str, str] = {
    "EUR": "€",
    "USD": "$",
    "RUB": "₽",
    "BYN": "Br",
}


def _fmt_amount(value: float | int) -> str:
    n = float(value)
    if n == int(n):
        return str(int(n))
    return f"{n:.2f}".rstrip("0").rstrip(".")


def _currency_suffix(code: str | None) -> str:
    cur = (code or "EUR").strip().upper()
    sym = _CURRENCY_SYMBOL.get(cur)
    if sym:
        return sym
    return cur


def _signed_money(amount: float, *, positive_prefix: bool = True) -> str:
    if amount > 0 and positive_prefix:
        return f"+{_fmt_amount(amount)}"
    if amount < 0:
        return f"-{_fmt_amount(abs(amount))}"
    return _fmt_amount(amount)


def format_rate_label(
    *,
    lang: str,
    rate: float | int,
    currency: str | None,
    rate_unit: str | None,
) -> str:
    unit_key = "rate_unit_lesson" if (rate_unit or "").strip().lower() == "lesson" else "rate_unit_hour"
    unit = t(lang, unit_key).lstrip("/").strip()
    money = _fmt_amount(rate)
    suffix = _currency_suffix(currency)
    return f"{money} {suffix} / {unit}"


def format_balance_label(
    *,
    lang: str,
    billing_type: str | None,
    balance: float | int,
    rate: float | int,
    currency: str | None,
    rate_unit: str | None,
    unpaid: float | int = 0,
) -> str:
    unit_key = "balance_unit_lesson" if (rate_unit or "").strip().lower() == "lesson" else "balance_unit_hour"
    unit = t(lang, unit_key)
    count = _fmt_amount(balance if billing_type != "postpaid" else unpaid)
    money = float(rate) * float(balance if billing_type != "postpaid" else unpaid)
    money_label = _signed_money(money)
    suffix = _currency_suffix(currency)
    if suffix == "€":
        money_part = f"{money_label} {suffix}"
    else:
        money_part = f"{money_label} {suffix}"
    if billing_type == "postpaid":
        return t(lang, "home_balance_postpaid").format(money=money_part, count=count, unit=unit)
    return t(lang, "home_balance_package").format(money=money_part, count=count, unit=unit)


def announcement_from_profile(profile: dict | None, lang: str) -> str | None:
    if not profile:
        return None
    vacation_body = vacation_body_from_profile(profile, lang)
    if vacation_body:
        return t(lang, "home_announcement_vacation").format(text=vacation_body)
    return None


def resolve_student_name(
    profile: dict | None,
    binding_name: str | None,
    telegram_name: str | None = None,
) -> str:
    for candidate in (
        (profile or {}).get("name"),
        binding_name,
        telegram_name,
    ):
        text = str(candidate or "").strip()
        if text:
            return text
    return ""


def build_home_message(
    *,
    lang: str,
    profile: dict | None,
    payment: dict | None,
    binding_name: str | None,
    site_url: str | None = None,
) -> str:
    name = resolve_student_name(profile, binding_name)
    greeting = t(lang, "home_greeting").format(name=name) if name else t(lang, "home_greeting_anon")

    bullets: list[str] = []
    subject = str((profile or {}).get("subject") or (payment or {}).get("subject") or "").strip()
    if subject:
        bullets.append(t(lang, "home_subject").format(subject=subject))

    if payment:
        bullets.append(
            t(lang, "home_rate").format(
                rate=format_rate_label(
                    lang=lang,
                    rate=payment.get("rate_per_hour") or 0,
                    currency=payment.get("rate_currency"),
                    rate_unit=payment.get("rate_unit"),
                ),
            ),
        )
        bullets.append(
            t(lang, "home_balance").format(
                balance=format_balance_label(
                    lang=lang,
                    billing_type=payment.get("billing_type"),
                    balance=payment.get("balance_lessons") or 0,
                    rate=payment.get("rate_per_hour") or 0,
                    currency=payment.get("rate_currency"),
                    rate_unit=payment.get("rate_unit"),
                    unpaid=payment.get("unpaid_lessons_count") or 0,
                ),
            ),
        )

    tutor_name = str((profile or {}).get("tutor_name") or "").strip()
    if tutor_name:
        bullets.append(t(lang, "home_tutor").format(name=tutor_name))

    announcement = announcement_from_profile(profile, lang)
    return messages.home_dashboard(
        title=t(lang, "home_title"),
        greeting=greeting,
        bullets=bullets,
        announcement=announcement,
        lang=lang,
        site_url=site_url,
    )
