"""Recoverable SQLite journal for exactly-once protocol boundaries."""

import sqlite3
from pathlib import Path


class Journal:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=FULL")
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS messages (
            game_id TEXT NOT NULL, session_id TEXT NOT NULL, tool_name TEXT NOT NULL,
            correlation_id TEXT NOT NULL, boundary TEXT NOT NULL, request TEXT NOT NULL,
            response TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(game_id, session_id, tool_name, correlation_id))"""
        )
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS state (
            game_id TEXT NOT NULL, session_id TEXT NOT NULL, name TEXT NOT NULL,
            value TEXT NOT NULL, PRIMARY KEY(game_id, session_id, name))"""
        )
        self.connection.commit()

    def lookup(self, key: tuple[str, str, str, str]) -> tuple[str, str] | None:
        row = self.connection.execute(
            "SELECT request,response FROM messages WHERE game_id=? AND session_id=? "
            "AND tool_name=? AND correlation_id=?", key
        ).fetchone()
        return None if row is None else (str(row[0]), str(row[1]))

    def record(
        self, key: tuple[str, str, str, str], boundary: str,
        request: str, response: str,
    ) -> None:
        with self.connection:
            self.connection.execute(
                "INSERT INTO messages(game_id,session_id,tool_name,correlation_id,"
                "boundary,request,response) VALUES(?,?,?,?,?,?,?)",
                (*key, boundary, request, response),
            )

    def set_state(self, game_id: str, session_id: str, name: str, value: str) -> None:
        with self.connection:
            self.connection.execute(
                "INSERT INTO state VALUES(?,?,?,?) ON CONFLICT(game_id,session_id,name) "
                "DO UPDATE SET value=excluded.value", (game_id, session_id, name, value)
            )

    def get_state(self, game_id: str, session_id: str, name: str) -> str | None:
        row = self.connection.execute(
            "SELECT value FROM state WHERE game_id=? AND session_id=? AND name=?",
            (game_id, session_id, name),
        ).fetchone()
        return None if row is None else str(row[0])

    def close(self) -> None:
        self.connection.close()
