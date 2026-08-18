"""Byte-stable live-match v1 schemas and canonicalization."""

import json
import re
from typing import Any

from .live_schemas import SCHEMAS
from .live_schemas import STATUSES as LIVE_STATUSES

VERSION = "1.0-provisional"
ROLES = {"cop", "thief"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
STATUSES = LIVE_STATUSES


def canonical(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def validate_shape(tool: str, payload: Any) -> tuple[str, str] | None:
    if type(payload) is not dict or tool not in SCHEMAS:
        return "INVALID_SHAPE", "payload"
    schema = SCHEMAS[tool]
    extra = payload.keys() - schema.keys()
    missing = schema.keys() - payload.keys()
    if extra:
        return "UNKNOWN_FIELD", sorted(extra)[0]
    if missing:
        return "MISSING_FIELD", sorted(missing)[0]
    for field, expected in schema.items():
        value = payload[field]
        if isinstance(value, bool) or not isinstance(value, expected):
            return "WRONG_TYPE", field
    return None


def validate_action(payload: dict[str, Any], turn: int) -> tuple[str, str] | None:
    expected = "thief" if turn % 2 == 0 else "cop"
    if payload["sender_role"] != expected:
        return "INVALID_ROLE", "active_role"
    kind, direction = payload["action_kind"], payload["direction"]
    if kind not in {"move", "stay", "barrier"}:
        return "ACTION_REJECTED", "action_kind"
    if kind == "barrier":
        if payload["sender_role"] != "cop" or direction is not None:
            return "BARRIER_REJECTED", "barrier"
        if payload["x"] is None or payload["y"] is None:
            return "BARRIER_REJECTED", "coordinates"
    elif payload["x"] is not None or payload["y"] is not None:
        return "ACTION_REJECTED", "coordinates"
    elif direction not in {"N", "S", "E", "W", "STAY"}:
        return "ACTION_REJECTED", "direction"
    return None
