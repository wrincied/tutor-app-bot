from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from google.cloud import firestore

from simple4u_bot.services.store import Binding

_COLLECTION = "bot_bindings"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class FirestoreBindingStore:
    """Firestore: link_token / student_id ↔ Telegram chat_id + profile."""

    def __init__(self, project_id: str | None = None) -> None:
        self._db = firestore.Client(project=project_id or None)

    def _doc(self, student_id: str) -> firestore.DocumentReference:
        return self._db.collection(_COLLECTION).document(student_id)

    @staticmethod
    def _to_binding(student_id: str, data: dict[str, Any]) -> Binding | None:
        chat_id = data.get("chat_id")
        if chat_id is None:
            return None
        return Binding(
            student_id=student_id,
            chat_id=int(chat_id),
            link_token=str(data.get("link_token") or ""),
            student_name=data.get("student_name"),
            bot_active=bool(data.get("bot_active", True)),
            telegram_user_id=data.get("telegram_user_id"),
            telegram_username=data.get("telegram_username"),
            telegram_display_name=data.get("telegram_display_name"),
            bot_lang=str(data.get("bot_lang") or "ru"),
            tutor_name=data.get("tutor_name"),
        )

    def _row_to_binding(self, snap: firestore.DocumentSnapshot) -> Binding | None:
        if not snap.exists:
            return None
        return self._to_binding(snap.id, snap.to_dict() or {})

    def upsert_link(
        self,
        *,
        student_id: str,
        link_token: str,
        student_name: str | None = None,
        bot_active: bool = True,
        tutor_name: str | None = None,
    ) -> None:
        ref = self._doc(student_id)
        snap = ref.get()
        payload: dict[str, Any] = {
            "link_token": link_token,
            "student_name": student_name,
            "bot_active": bot_active,
            "tutor_name": tutor_name,
            "updated_at": _now_iso(),
        }
        if snap.exists:
            ref.set(payload, merge=True)
        else:
            ref.set(
                {
                    **payload,
                    "chat_id": None,
                    "telegram_user_id": None,
                    "telegram_username": None,
                    "telegram_display_name": None,
                    "bot_lang": "ru",
                }
            )

    def bind_chat(
        self,
        *,
        link_token: str,
        chat_id: int,
        telegram_user_id: str | None = None,
        telegram_username: str | None = None,
        telegram_display_name: str | None = None,
    ) -> Binding | None:
        matches = list(
            self._db.collection(_COLLECTION).where("link_token", "==", link_token).limit(1).stream()
        )
        if not matches:
            return None
        snap = matches[0]
        data = snap.to_dict() or {}
        student_id = snap.id

        batch = self._db.batch()
        for other in self._db.collection(_COLLECTION).where("chat_id", "==", chat_id).stream():
            if other.id != student_id:
                batch.update(
                    other.reference,
                    {
                        "chat_id": None,
                        "telegram_user_id": None,
                        "telegram_username": None,
                        "telegram_display_name": None,
                        "updated_at": _now_iso(),
                    },
                )
        batch.update(
            snap.reference,
            {
                "chat_id": chat_id,
                "telegram_user_id": telegram_user_id or data.get("telegram_user_id"),
                "telegram_username": telegram_username or data.get("telegram_username"),
                "telegram_display_name": telegram_display_name or data.get("telegram_display_name"),
                "updated_at": _now_iso(),
            },
        )
        batch.commit()

        updated = snap.reference.get().to_dict() or {}
        return Binding(
            student_id=student_id,
            chat_id=chat_id,
            link_token=link_token,
            student_name=updated.get("student_name"),
            bot_active=bool(updated.get("bot_active", True)),
            telegram_user_id=updated.get("telegram_user_id"),
            telegram_username=updated.get("telegram_username"),
            telegram_display_name=updated.get("telegram_display_name"),
            bot_lang=str(updated.get("bot_lang") or "ru"),
            tutor_name=updated.get("tutor_name"),
        )

    def set_lang(self, student_id: str, lang: str) -> bool:
        ref = self._doc(student_id)
        if not ref.get().exists:
            return False
        ref.update({"bot_lang": lang, "updated_at": _now_iso()})
        return True

    def set_tutor_name(self, student_id: str, tutor_name: str | None) -> bool:
        name = (tutor_name or "").strip() or None
        ref = self._doc(student_id)
        if not ref.get().exists:
            return False
        ref.update({"tutor_name": name, "updated_at": _now_iso()})
        return True

    def unlink_chat(self, chat_id: int) -> Binding | None:
        matches = list(
            self._db.collection(_COLLECTION).where("chat_id", "==", chat_id).limit(1).stream()
        )
        if not matches:
            return None
        snap = matches[0]
        binding = self._row_to_binding(snap)
        snap.reference.update(
            {
                "chat_id": None,
                "telegram_user_id": None,
                "telegram_username": None,
                "telegram_display_name": None,
                "bot_active": False,
                "updated_at": _now_iso(),
            }
        )
        return binding

    def unlink_student(self, student_id: str) -> Binding | None:
        ref = self._doc(student_id)
        snap = ref.get()
        if not snap.exists:
            return None
        binding = self._row_to_binding(snap)
        ref.update(
            {
                "chat_id": None,
                "telegram_user_id": None,
                "telegram_username": None,
                "telegram_display_name": None,
                "bot_active": False,
                "updated_at": _now_iso(),
            }
        )
        return binding

    def set_bot_active(self, student_id: str, active: bool) -> bool:
        ref = self._doc(student_id)
        if not ref.get().exists:
            return False
        ref.update({"bot_active": active, "updated_at": _now_iso()})
        return True

    def get_by_student(self, student_id: str) -> Binding | None:
        return self._row_to_binding(self._doc(student_id).get())

    def get_by_chat(self, chat_id: int) -> Binding | None:
        matches = list(
            self._db.collection(_COLLECTION).where("chat_id", "==", chat_id).limit(1).stream()
        )
        if not matches:
            return None
        return self._row_to_binding(matches[0])
