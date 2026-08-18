import json
from typing import Any

from salareen_thief.base_logic.actions import (
    BarrierAction,
    CaptureClaim,
    MoveAction,
    MoveChoice,
)
from salareen_thief.base_logic.capture import adjacent_destinations
from salareen_thief.base_logic.state_factory import build_state
from salareen_thief.base_logic.state_types import (
    CaptureCause,
    Coordinate,
    EpisodeStatus,
    Outcome,
    OutcomeKind,
    Role,
)


def restore_state(adapter: Any, saved: str):
    data = json.loads(saved)
    outcome = None
    if data["outcome"] is not None:
        cause = data["capture_cause"]
        outcome = Outcome(
            OutcomeKind(data["outcome"]),
            None if cause is None else CaptureCause(cause),
        )
    return build_state(
        adapter.config,
        thief=Coordinate(*data["thief"]),
        cop=Coordinate(*data["cop"]),
        barriers=(Coordinate(*item) for item in data["barriers"]),
        barrier_usage=data["barrier_usage"],
        valid_steps=data["valid_steps"],
        status=EpisodeStatus(data["status"]),
        outcome=outcome,
    )


def action_for(adapter: Any, payload: dict[str, Any]):
    role = Role(payload["sender_role"])
    if payload["action_kind"] != "barrier":
        return MoveAction(role, MoveChoice(payload["direction"]))
    target = Coordinate(payload["x"], payload["y"])
    destinations = adjacent_destinations(adapter.state)
    cause = None
    if target == adapter.state.positions.thief:
        cause = CaptureCause.BARRIER_ON_THIEF
    elif len(destinations) == 1 and target == destinations[0]:
        cause = CaptureCause.TRAPPED_THIEF
    claim = None if cause is None else CaptureClaim(Role.COP, cause)
    return BarrierAction(role, target, claim)
