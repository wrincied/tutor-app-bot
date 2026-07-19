from simple4u_bot.services import messages


def test_balance_message() -> None:
    assert "2" in messages.balance(lessons_left=2)


def test_payment_message() -> None:
    text = messages.payment(amount_label="€225", lessons_added=5)
    assert "€225" in text
    assert "+5" in text


def test_lesson_start_message() -> None:
    text = messages.lesson_start(minutes_before=30, time_label="11:30")
    assert "30" in text
    assert "11:30" in text


def test_homework_message() -> None:
    assert "упр. 4–6" in messages.homework(text="упр. 4–6, стр. 18.")
