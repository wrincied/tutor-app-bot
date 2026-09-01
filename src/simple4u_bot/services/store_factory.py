from __future__ import annotations

from pathlib import Path
from typing import Protocol

from simple4u_bot.services.store import Binding, BindingStore


class BindingStoreProtocol(Protocol):
    def upsert_link(
        self,
        *,
        student_id: str,
        link_token: str,
        student_name: str | None = None,
        bot_active: bool = True,
        tutor_name: str | None = None,
    ) -> None: ...

    def bind_chat(
        self,
        *,
        link_token: str,
        chat_id: int,
        telegram_user_id: str | None = None,
        telegram_username: str | None = None,
        telegram_display_name: str | None = None,
    ) -> Binding | None: ...

    def set_lang(self, student_id: str, lang: str) -> bool: ...

    def set_tutor_name(self, student_id: str, tutor_name: str | None) -> bool: ...

    def unlink_chat(self, chat_id: int) -> Binding | None: ...

    def unlink_student(self, student_id: str) -> Binding | None: ...

    def set_bot_active(self, student_id: str, active: bool) -> bool: ...

    def get_by_student(self, student_id: str) -> Binding | None: ...

    def get_by_chat(self, chat_id: int) -> Binding | None: ...


def create_binding_store(
    *,
    binding_store: str,
    bot_db_path: Path,
    gcp_project: str | None = None,
) -> BindingStoreProtocol:
    mode = (binding_store or "sqlite").strip().lower()
    if mode == "firestore":
        from simple4u_bot.services.store_firestore import FirestoreBindingStore

        return FirestoreBindingStore(project_id=gcp_project or None)
    return BindingStore(bot_db_path)
