from simple4u_bot.services.vacation import format_vacation_end_date, vacation_body_from_profile


def test_format_vacation_end_date() -> None:
    assert format_vacation_end_date("2026-08-25") == "25.08.2026"
    assert format_vacation_end_date("") is None


def test_vacation_body_custom_message() -> None:
    body = vacation_body_from_profile(
        {
            "vacation_active": True,
            "vacation_message": "Уехал в горы",
        },
        "ru",
    )
    assert body == "Уехал в горы"


def test_vacation_body_default_with_end_date() -> None:
    body = vacation_body_from_profile(
        {
            "vacation_active": True,
            "vacation_end_date": "2026-08-25",
        },
        "ru",
    )
    assert body is not None
    assert "25.08.2026" in body


def test_vacation_body_inactive() -> None:
    assert vacation_body_from_profile({"vacation_active": False}, "ru") is None
