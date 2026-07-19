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


class BindingStore:
    """SQLite: link_token / student_id ↔ Telegram chat_id."""

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
                  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
                )
                """
            )
            conn.commit()

    def upsert_link(
        self,
        *,
        student_id: str,
        link_token: str,
        student_name: str | None = None,
        bot_active: bool = True,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO bindings (student_id, link_token, student_name, bot_active)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(student_id) DO UPDATE SET
                  link_token = excluded.link_token,
                  student_name = COALESCE(excluded.student_name, bindings.student_name),
                  bot_active = excluded.bot_active,
                  updated_at = datetime('now')
                """,
                (student_id, link_token, student_name, int(bot_active)),
            )
            conn.commit()

    def bind_chat(self, *, link_token: str, chat_id: int) -> Binding | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM bindings WHERE link_token = ?",
                (link_token,),
            ).fetchone()
            if row is None:
                return None
            conn.execute(
                """
                UPDATE bindings
                SET chat_id = ?, updated_at = datetime('now')
                WHERE link_token = ?
                """,
                (chat_id, link_token),
            )
            conn.commit()
            return Binding(
                student_id=row["student_id"],
                chat_id=chat_id,
                link_token=link_token,
                student_name=row["student_name"],
                bot_active=bool(row["bot_active"]),
            )

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

    @staticmethod
    def _row_to_binding(row: sqlite3.Row | None) -> Binding | None:
        if row is None or row["chat_id"] is None:
            return None
        return Binding(
            student_id=row["student_id"],
            chat_id=int(row["chat_id"]),
            link_token=row["link_token"],
            student_name=row["student_name"],
            bot_active=bool(row["bot_active"]),
        )
