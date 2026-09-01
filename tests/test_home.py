from simple4u_bot.services import messages
from simple4u_bot.services.home import announcement_from_profile, build_home_message


def test_home_dashboard_standard() -> None:
    text = build_home_message(
        lang="ru",
        profile={
            "name": "Иван",
            "tutor_name": "Admin",
            "subject": "Математика",
            "vacation_active": False,
        },
        payment={
            "billing_type": "package",
            "balance_lessons": 2,
            "rate_per_hour": 15,
            "rate_currency": "EUR",
            "rate_unit": "lesson",
        },
        binding_name="Иван",
    )
    assert "<b>Главная</b>" in text
    assert "Привет, Иван!" in text
    assert "Предмет: Математика" in text
    assert "15 € / занятие" in text
    assert "+30 € (2 занятий)" in text
    assert "Репетитор: Admin" in text
    assert "Отпуск:" not in text
    assert "© Simple4U" in text


def test_home_dashboard_with_vacation() -> None:
    text = build_home_message(
        lang="ru",
        profile={
            "name": "Иван",
            "tutor_name": "Admin",
            "subject": "Математика",
            "vacation_active": True,
            "vacation_end_date": "2026-09-05",
            "vacation_message": "",
        },
        payment={
            "billing_type": "package",
            "balance_lessons": 2,
            "rate_per_hour": 15,
            "rate_currency": "EUR",
            "rate_unit": "lesson",
        },
        binding_name="Иван",
    )
    assert "Отпуск: Репетитор в отпуске до 05.09.2026" in text


def test_home_dashboard_message_template() -> None:
    text = messages.home_dashboard(
        title="Главная",
        greeting="Привет, Иван!",
        bullets=[
            "Предмет: Математика",
            "Ставка: 15 € / занятие",
            "Баланс: +30 € (2 занятий)",
            "Репетитор: Admin",
        ],
        announcement="Отпуск: Репетитор в отпуске до 05.09.2026. Ответит после возвращения.",
    )
    assert "• Предмет: Математика" in text
    assert "• Баланс: +30 € (2 занятий)" in text
    assert "Отпуск: Репетитор в отпуске" in text


def test_announcement_from_profile() -> None:
    line = announcement_from_profile(
        {
            "vacation_active": True,
            "vacation_message": "Гайс я в отпуск",
        },
        "ru",
    )
    assert line == "Отпуск: Гайс я в отпуск"
