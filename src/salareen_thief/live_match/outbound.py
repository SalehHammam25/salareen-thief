"""Immutable local action preparation before first transmission."""

from typing import Any

from .protocol import canonical, validate_action, validate_shape


def prepare(session: Any, payload: dict[str, Any]) -> dict[str, Any]:
    issue = validate_shape("submit_action_v1", payload)
    if not issue and payload.get("sender_role") != session.local_role:
        issue = ("INVALID_ROLE", "sender_role")
    if not issue:
        issue = validate_action(payload, session.turn_index)
    if not issue and session.gameplay:
        issue = session.gameplay.validate_payload(payload)
    if issue:
        return session._reject(payload.get("correlation_id"), *issue)
    session._save("pending_action", canonical(payload))
    return {
        "accepted": True,
        "correlation_id": payload["correlation_id"],
        "status": "prepared",
    }
