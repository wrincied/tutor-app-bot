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
    binding = store.bind_chat(link_token="token-abcdef", chat_id=42)
    assert binding is not None
    assert binding.chat_id == 42
    assert binding.student_name == "Anna"

    by_student = store.get_by_student("stu_1")
    assert by_student is not None
    assert by_student.chat_id == 42

    assert store.set_bot_active("stu_1", False) is True
    inactive = store.get_by_student("stu_1")
    assert inactive is not None
    assert inactive.bot_active is False
