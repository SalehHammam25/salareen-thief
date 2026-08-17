"""Credential-free, role-local JSON Lines event log."""

import json
import time
from pathlib import Path
from typing import Any


class EventLog:
    def __init__(self, path: str | Path, role: str, game_id: str,
                 session_id: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.role, self.game_id, self.session_id = role, game_id, session_id
        self.index = (sum(1 for _ in self.path.open(encoding="utf-8"))
                      if self.path.exists() else 0)

    def emit(self, event_type: str, *, turn: int, phase: str,
             correlation_id: str | None = None,
             result_code: str | None = None, data: dict[str, Any] | None = None) -> None:
        event = {"schema_version": "live-event-v1", "event_index": self.index,
                 "timestamp_monotonic": time.monotonic_ns(), "game_id": self.game_id,
                 "session_id": self.session_id, "game_number": 1,
                 "turn_index": turn, "phase": phase, "local_role": self.role,
                 "event_type": event_type, "correlation_id": correlation_id,
                 "related_correlation_id": None, "result_code": result_code,
                 "data": data or {}}
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
        self.index += 1
