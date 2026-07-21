from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Binding:
    student_id: str
    chat_id: int
    link_token: str
    student_name: str | None = None
    bot_active: bool = True
    telegram_user_id: str | None = None
    telegram_username: str | None = None
    telegram_display_name: str | None = None
    bot_lang: str = "ru"
    tutor_name: str | None = None


class BindingStore:
    """SQLite: link_token / student_id ↔ Telegram chat_id + profile."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS bindings (
                  student_id TEXT PRIMARY KEY,
                  chat_id INTEGER UNIQUE,
                  link_token TEXT UNIQUE NOT NULL,
                  student_name TEXT,
                  bot_active INTEGER NOT NULL DEFAULT 1,
                  telegram_user_id TEXT,
                  telegram_username TEXT,
                  telegram_display_name TEXT,
                  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
                )
                """
            )
            cols = {row[1] for row in conn.execute("PRAGMA table_info(bindings)")}
            for col, decl in (
                ("telegram_user_id", "TEXT"),
                ("telegram_username", "TEXT"),
                ("telegram_display_name", "TEXT"),
                ("bot_lang", "TEXT NOT NULL DEFAULT 'ru'"),
                ("tutor_name", "TEXT"),
            ):
                if col not in cols:
                    conn.execute(f"ALTER TABLE bindings ADD COLUMN {col} {decl}")
            conn.commit()

    def upsert_link(
        self,
        *,
        student_id: str,
        link_token: str,
        student_name: str | None = None,
        bot_active: bool = True,
        tutor_name: str | None = None,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO bindings (student_id, link_token, student_name, bot_active, tutor_name)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(student_id) DO UPDATE SET
                  link_token = excluded.link_token,
                  student_name = COALESCE(excluded.student_name, bindings.student_name),
                  bot_active = excluded.bot_active,
                  tutor_name = COALESCE(excluded.tutor_name, bindings.tutor_name),
                  updated_at = datetime('now')
                """,
                (student_id, link_token, student_name, int(bot_active), tutor_name),
            )
            conn.commit()

    def bind_chat(
        self,
        *,
        link_token: str,
        chat_id: int,
        telegram_user_id: str | None = None,
        telegram_username: str | None = None,
        telegram_display_name: str | None = None,
    ) -> Binding | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM bindings WHERE link_token = ?",
                (link_token,),
            ).fetchone()
            if row is None:
                return None

            # Один chat_id может быть только у одной связки: снимаем со старых строк.
            conn.execute(
                """
                UPDATE bindings
                SET chat_id = NULL,
                    telegram_user_id = NULL,
                    telegram_username = NULL,
                    telegram_display_name = NULL,
                    updated_at = datetime('now')
                WHERE chat_id = ?
                  AND student_id != ?
                """,
                (chat_id, row["student_id"]),
            )

            conn.execute(
                """
                UPDATE bindings
                SET chat_id = ?,
                    telegram_user_id = COALESCE(?, telegram_user_id),
                    telegram_username = COALESCE(?, telegram_username),
                    telegram_display_name = COALESCE(?, telegram_display_name),
                    updated_at = datetime('now')
                WHERE link_token = ?
                """,
                (
                    chat_id,
                    telegram_user_id,
                    telegram_username,
                    telegram_display_name,
                    link_token,
                ),
            )
            conn.commit()
            return Binding(
                student_id=row["student_id"],
                chat_id=chat_id,
                link_token=link_token,
                student_name=row["student_name"],
                bot_active=bool(row["bot_active"]),
                telegram_user_id=telegram_user_id or row["telegram_user_id"],
                telegram_username=telegram_username or row["telegram_username"],
                telegram_display_name=telegram_display_name or row["telegram_display_name"],
                bot_lang=(row["bot_lang"] if "bot_lang" in row.keys() else None) or "ru",
                tutor_name=(row["tutor_name"] if "tutor_name" in row.keys() else None),
            )

    def set_lang(self, student_id: str, lang: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                """
                UPDATE bindings
                SET bot_lang = ?, updated_at = datetime('now')
                WHERE student_id = ?
                """,
                (lang, student_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def set_tutor_name(self, student_id: str, tutor_name: str | None) -> bool:
        name = (tutor_name or "").strip() or None
        with self._connect() as conn:
            cur = conn.execute(
                """
                UPDATE bindings
                SET tutor_name = ?, updated_at = datetime('now')
                WHERE student_id = ?
                """,
                (name, student_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def unlink_chat(self, chat_id: int) -> Binding | None:
        """Clear Telegram binding for this chat; keep student row + link_token."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM bindings WHERE chat_id = ?",
                (chat_id,),
            ).fetchone()
            if row is None:
                return None
            binding = self._row_to_binding(row)
            conn.execute(
                """
                UPDATE bindings
                SET chat_id = NULL,
                    telegram_user_id = NULL,
                    telegram_username = NULL,
                    telegram_display_name = NULL,
                    bot_active = 0,
                    updated_at = datetime('now')
                WHERE chat_id = ?
                """,
                (chat_id,),
            )
            conn.commit()
            return binding

    def unlink_student(self, student_id: str) -> Binding | None:
        """Tutor-side disconnect: clear Telegram fields, keep invite token."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM bindings WHERE student_id = ?",
                (student_id,),
            ).fetchone()
            if row is None:
                return None
            # May already be unlinked (chat_id NULL) — still clear profile fields.
            binding = self._row_to_binding(row) if row["chat_id"] is not None else None
            conn.execute(
                """
                UPDATE bindings
                SET chat_id = NULL,
                    telegram_user_id = NULL,
                    telegram_username = NULL,
                    telegram_display_name = NULL,
                    bot_active = 0,
                    updated_at = datetime('now')
                WHERE student_id = ?
                """,
                (student_id,),
            )
            conn.commit()
            return binding

    def set_bot_active(self, student_id: str, active: bool) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                """
                UPDATE bindings
                SET bot_active = ?, updated_at = datetime('now')
                WHERE student_id = ?
                """,
                (int(active), student_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def get_by_student(self, student_id: str) -> Binding | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM bindings WHERE student_id = ?",
                (student_id,),
            ).fetchone()
        return self._row_to_binding(row)

    def get_by_chat(self, chat_id: int) -> Binding | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM bindings WHERE chat_id = ?",
                (chat_id,),
            ).fetchone()
        return self._row_to_binding(row)

    @staticmethod
    def _row_to_binding(row: sqlite3.Row | None) -> Binding | None:
        if row is None or row["chat_id"] is None:
            return None
        keys = row.keys()
        return Binding(
            student_id=row["student_id"],
            chat_id=int(row["chat_id"]),
            link_token=row["link_token"],
            student_name=row["student_name"],
            bot_active=bool(row["bot_active"]),
            telegram_user_id=row["telegram_user_id"],
            telegram_username=row["telegram_username"],
            telegram_display_name=row["telegram_display_name"],
            bot_lang=(row["bot_lang"] if "bot_lang" in keys else None) or "ru",
            tutor_name=(row["tutor_name"] if "tutor_name" in keys else None),
        )
