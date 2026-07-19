"""Message templates matching landing-v2 / CRM bot copy (RU default)."""

from __future__ import annotations


def balance(*, lessons_left: int) -> str:
    return f"Привет! В пакете осталось {lessons_left} занятий."


def payment(*, amount_label: str, lessons_added: int) -> str:
    return f"Оплата получена: {amount_label} · +{lessons_added} занятий. Спасибо!"


def lesson_start(*, minutes_before: int, time_label: str) -> str:
    return f"Через {minutes_before} минут начинается урок · {time_label}"


def homework(*, text: str) -> str:
    return f"Домашка на сегодня: {text}"


def lesson_moved(*, new_time_label: str) -> str:
    return f"Урок перенесён. Новое время: {new_time_label}"


def welcome_linked(*, student_name: str | None = None) -> str:
    if student_name:
        return (
            f"Привет, {student_name}! Уведомления Simple4U подключены.\n"
            "Сюда будут приходить баланс, оплата, старт урока и домашка."
        )
    return (
        "Привет! Уведомления Simple4U подключены.\n"
        "Сюда будут приходить баланс, оплата, старт урока и домашка."
    )


def welcome_need_link() -> str:
    return (
        "Привет! Я бот Simple4U.\n"
        "Открой персональную ссылку от репетитора, чтобы получать уведомления."
    )
