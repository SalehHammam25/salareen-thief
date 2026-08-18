"""Byte-stable live-match v1 schemas and canonicalization."""

import json
import re
from typing import Any

VERSION = "1.0-provisional"
ROLES = {"cop", "thief"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
IDENTITY = {
    "protocol_version": str,
    "correlation_id": str,
    "sender_role": str,
    "game_id": str,
    "session_id": str,
    "game_number": int,
}
SCHEMAS: dict[str, dict[str, type]] = {
    "security_bootstrap_v1": {**IDENTITY, "bundle": dict},
    "security_commit_v1": {**IDENTITY, "turn_index": int,
        "action_correlation_id": str, "digest": str},
    "security_nonce_audit_v1": {**IDENTITY, "turn_index": int, "nonces": dict},
    "initialize_game_v1": {**IDENTITY, "config_schema_version": str, "starting_role": str},
    "submit_action_v1": {**IDENTITY, "turn_index": int, "action_kind": str,
        "direction": (str, type(None)), "x": (int, type(None)), "y": (int, type(None))},
    "acknowledge_action_v1": {**IDENTITY, "turn_index": int,
        "action_correlation_id": str, "result": str, "result_code": str,
        "next_turn_index": int, "next_role": str},
    "publish_scent_v1": {**IDENTITY, "turn_index": int, "axis_start_index": int,
        "width": int, "height": int, "values": list},
    "send_language_hint_v1": {**IDENTITY, "turn_index": int, "text": str,
        "word_count": int},
    "submit_capture_claim_v1": {**IDENTITY, "turn_index": int,
        "claimant_role": str, "capture_kind": str, "cop_x": int, "cop_y": int,
        "thief_x": int, "thief_y": int},
    "reconcile_terminal_v1": {**IDENTITY, "turn_index": int, "outcome": str,
        "winner_role": (str, type(None)), "loser_role": (str, type(None)),
        "attribution": str, "reason_code": str},
    "reconcile_score_v1": {**IDENTITY, "turn_index": int, "outcome": str,
        "cop_score": int, "thief_score": int},
    "resume_match_v1": {"protocol_version": str, "correlation_id": str,
        "sender_role": str, "game_id": str, "session_id": str, "turn_index": int,
        "phase": str},
    "shutdown_match_v1": {**IDENTITY, "turn_index": int, "mode": str,
        "reason_code": str},
}
STATUSES = {"security_bootstrap_v1": "security_verified",
    "security_commit_v1": "commitment_acknowledged",
    "security_nonce_audit_v1": "nonce_audit_verified",
    "initialize_game_v1": "initialized", "submit_action_v1": "applied",
    "acknowledge_action_v1": "acknowledged", "publish_scent_v1": "observed",
    "send_language_hint_v1": "hint_accepted",
    "submit_capture_claim_v1": "capture_confirmed",
    "reconcile_terminal_v1": "terminal_agreed", "reconcile_score_v1": "score_agreed",
    "resume_match_v1": "resume_allowed", "shutdown_match_v1": "shutdown_ready"}


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
