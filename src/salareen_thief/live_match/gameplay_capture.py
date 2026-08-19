"""Capture verification for the live gameplay adapter."""

from typing import Any

from salareen_thief.base_logic.action_results import ActionAccepted
from salareen_thief.base_logic.actions import CaptureClaim
from salareen_thief.base_logic.state_types import CaptureCause, EpisodeStatus, Role

from .capture_security import verify_live_capture


def verify_capture(adapter, payload: dict[str, Any], *, apply: bool):
    causes = {
        "cooccupancy": CaptureCause.COORDINATE_OVERLAP,
        "barrier": CaptureCause.BARRIER_ON_THIEF,
        "trapped": CaptureCause.TRAPPED_THIEF,
    }
    cause = causes.get(payload["capture_kind"])
    if payload["claimant_role"] != "cop" or cause is None:
        return "CAPTURE_REJECTED", "capture_kind"
    expected = (
        adapter.state.positions.cop.row,
        adapter.state.positions.cop.col,
        adapter.state.positions.thief.row,
        adapter.state.positions.thief.col,
    )
    claimed = tuple(payload[key] for key in ("cop_x", "cop_y", "thief_x", "thief_y"))
    if claimed != expected:
        return "CAPTURE_REJECTED", "coordinates"
    if not verify_live_capture(payload, adapter.state):
        return "CAPTURE_REJECTED", "security_evidence"
    if adapter.state.status is EpisodeStatus.TERMINAL:
        if adapter.state.outcome and adapter.state.outcome.capture_cause:
            return None
        return "CAPTURE_REJECTED", "local_consistency"
    result = adapter.rules.apply(adapter.state, CaptureClaim(Role.COP, cause))
    if not isinstance(result, ActionAccepted):
        return "CAPTURE_REJECTED", "local_consistency"
    if apply:
        adapter.state = result.state
    return None
