"""Translate production capture state into the Stage 6 claim envelope."""

from typing import Any

from salareen_thief.security.protocol import SecurityViolation, verify_capture_claim


def verify_live_capture(payload: dict[str, Any], state: Any) -> bool:
    kind = {"cooccupancy": "overlap"}.get(
        payload["capture_kind"], payload["capture_kind"]
    )
    claim = {
        "game_id": payload["game_id"],
        "turn": payload["turn_index"],
        "claimant_role": payload["claimant_role"],
        "kind": kind,
        "cop": [state.positions.cop.row, state.positions.cop.col],
        "thief": [state.positions.thief.row, state.positions.thief.col],
        "barriers": [[cell.row, cell.col] for cell in state.barriers],
    }
    try:
        verify_capture_claim(claim)
    except SecurityViolation:
        return payload["capture_kind"] == "trapped"
    return True
