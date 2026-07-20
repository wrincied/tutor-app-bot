"""Message templates for student Telegram notifications."""

from __future__ import annotations


def _tutor_line(tutor_name: str | None) -> str:
    name = (tutor_name or "").strip()
    return f"Репетитор: {name}\n" if name else ""


def _fmt_units(value: float | int) -> str:
    n = float(value)
    if n == int(n):
        return str(int(n))
    return f"{n:.2f}".rstrip("0").rstrip(".")


def _unit_word(rate_unit: str | None, *, plural: bool = True) -> str:
    if (rate_unit or "").strip().lower() == "lesson":
        return "занятий" if plural else "занятие"
    return "ч"


def balance(
    *,
    lessons_left: float | int,
    tutor_name: str | None = None,
    rate_unit: str | None = None,
) -> str:
    unit = _unit_word(rate_unit)
    return f"{_tutor_line(tutor_name)}В пакете осталось {_fmt_units(lessons_left)} {unit}."


def payment(
    *,
    amount_label: str,
    lessons_added: float | int,
    tutor_name: str | None = None,
    rate_unit: str | None = None,
) -> str:
    unit = _unit_word(rate_unit)
    return (
        f"{_tutor_line(tutor_name)}"
        f"Оплата получена: {amount_label} · +{_fmt_units(lessons_added)} {unit}. Спасибо!"
    )


def lesson_start(
    *,
    minutes_before: int,
    time_label: str,
    meeting_link: str | None = None,
    tutor_name: str | None = None,
) -> str:
    who = f" с {tutor_name.strip()}" if (tutor_name or "").strip() else ""
    text = f"Через {minutes_before} минут начинается урок{who} · {time_label}"
    if meeting_link:
        text = f"{text}\nСсылка на звонок: {meeting_link}"
    return text


def homework(*, text: str, tutor_name: str | None = None) -> str:
    return f"{_tutor_line(tutor_name)}Домашка на сегодня: {text}"


def lesson_moved(
    *,
    new_time_label: str,
    meeting_link: str | None = None,
    tutor_name: str | None = None,
) -> str:
    who = f" ({tutor_name.strip()})" if (tutor_name or "").strip() else ""
    text = f"Урок перенесён{who}. Новое время: {new_time_label}"
    if meeting_link:
        text = f"{text}\nСсылка на звонок: {meeting_link}"
    return text


def welcome_linked(
    *,
    student_name: str | None = None,
    tutor_name: str | None = None,
) -> str:
    hello = f"Привет, {student_name}!" if student_name else "Привет!"
    tutor = (
        f"\nТвой репетитор: <b>{tutor_name.strip()}</b>."
        if (tutor_name or "").strip()
        else ""
    )
    return (
        f"{hello} Уведомления Simple4U подключены.{tutor}\n"
        "Сюда будут приходить баланс, оплата, старт урока и домашка."
    )


def welcome_need_link() -> str:
    return (
        "Привет! Я бот Simple4U.\n"
        "Открой персональную ссылку от репетитора, чтобы получать уведомления."
    )
