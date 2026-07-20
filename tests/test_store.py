from pathlib import Path

from simple4u_bot.services.store import BindingStore


def test_bind_flow(tmp_path: Path) -> None:
    store = BindingStore(tmp_path / "bot.sqlite3")
    store.upsert_link(
        student_id="stu_1",
        link_token="token-abcdef",
        student_name="Anna",
        bot_active=True,
    )
    binding = store.bind_chat(
        link_token="token-abcdef",
        chat_id=42,
        telegram_user_id="99",
        telegram_username="anna_tg",
        telegram_display_name="Anna T",
    )
    assert binding is not None
    assert binding.chat_id == 42
    assert binding.telegram_username == "anna_tg"

    by_student = store.get_by_student("stu_1")
    assert by_student is not None
    assert by_student.telegram_user_id == "99"

    assert store.set_bot_active("stu_1", False) is True
    inactive = store.get_by_student("stu_1")
    assert inactive is not None
    assert inactive.bot_active is False


def test_rebind_same_chat_to_another_student(tmp_path: Path) -> None:
    store = BindingStore(tmp_path / "bot.sqlite3")
    store.upsert_link(student_id="stu_1", link_token="tok-1", student_name="A")
    store.upsert_link(student_id="stu_2", link_token="tok-2", student_name="B")
    assert store.bind_chat(link_token="tok-1", chat_id=7, telegram_user_id="1") is not None

    rebound = store.bind_chat(link_token="tok-2", chat_id=7, telegram_user_id="1")
    assert rebound is not None
    assert rebound.student_id == "stu_2"
    assert rebound.chat_id == 7

    assert store.get_by_chat(7) is not None
    assert store.get_by_chat(7).student_id == "stu_2"
    assert store.get_by_student("stu_1") is None
