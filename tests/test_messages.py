from simple4u_bot.services import messages


def test_balance_message() -> None:
    assert "2" in messages.balance(lessons_left=2)
    assert "занятий" in messages.balance(lessons_left=2, rate_unit="lesson")
    assert "Репетитор: Анна" in messages.balance(lessons_left=2, tutor_name="Анна")
    assert "1.5 ч" in messages.balance(lessons_left=1.5, rate_unit="hour")


def test_payment_message() -> None:
    text = messages.payment(amount_label="€225", lessons_added=5, tutor_name="Анна", rate_unit="lesson")
    assert "€225" in text
    assert "+5" in text
    assert "Репетитор: Анна" in text
    assert "занятий" in text
    hours = messages.payment(amount_label="€60", lessons_added=1.5, rate_unit="hour")
    assert "+1.5 ч" in hours


def test_lesson_start_with_link() -> None:
    text = messages.lesson_start(
        minutes_before=30,
        time_label="11:30",
        meeting_link="https://meet.example/x",
        tutor_name="Анна",
    )
    assert "11:30" in text
    assert "https://meet.example/x" in text
    assert "с Анна" in text


def test_homework_message() -> None:
    text = messages.homework(text="упр. 4–6, стр. 18.", tutor_name="Анна")
    assert "упр. 4–6" in text
    assert "Репетитор: Анна" in text


def test_welcome_linked_includes_tutor() -> None:
    text = messages.welcome_linked(student_name="Ира", tutor_name="Анна")
    assert "Ира" in text
    assert "Анна" in text


def test_lesson_moved_message() -> None:
    text = messages.lesson_moved(
        new_time_label="пн, 21.07, 15:00",
        meeting_link="https://meet.example/x",
        tutor_name="Анна",
    )
    assert "перенесён" in text
    assert "15:00" in text
    assert "Анна" in text
    assert "https://meet.example/x" in text
