"""Role-local deterministic strategies used only by production verification."""

from typing import Any

from .session import LiveMatchSession


def _base(session: LiveMatchSession) -> dict[str, Any]:
    return {
        "protocol_version": "1.0-provisional",
        "correlation_id": f"action-{session.turn_index}",
        "sender_role": session.local_role,
        "game_id": session.game_id,
        "session_id": session.session_id,
        "game_number": session.game_number,
        "turn_index": session.turn_index,
    }


def choose(session: LiveMatchSession, scenario: str) -> dict[str, Any]:
    direction = "STAY"
    state = session.gameplay.state
    if scenario == "trapped" and session.local_role == "cop":
        steps = (
            ("S", None),
            ("S", None),
            ("E", None),
            ("E", None),
            (None, (2, 3)),
            (None, (3, 2)),
            ("W", None),
            ("S", None),
            ("S", None),
            ("E", None),
            (None, (4, 3)),
            ("S", None),
            ("E", None),
            ("E", None),
            ("N", None),
            (None, (3, 4)),
        )
        direction, target = steps[session.turn_index // 2]
        if target:
            return {
                **_base(session),
                "action_kind": "barrier",
                "direction": None,
                "x": target[0],
                "y": target[1],
            }
    if (
        scenario == "capture_priority"
        and session.local_role == "cop"
        and (state.valid_steps == 35)
    ):
        thief = state.positions.thief
        return {
            **_base(session),
            "action_kind": "barrier",
            "direction": None,
            "x": thief.row,
            "y": thief.col,
        }
    if scenario == "capture_priority" and session.local_role == "cop":
        cop, thief = state.positions.cop, state.positions.thief
        direction = (
            "S" if cop.row < thief.row else ("E" if cop.col + 1 < thief.col else "STAY")
        )
    if scenario in {"capture", "barrier_capture"} and session.local_role == "cop":
        cop, thief = state.positions.cop, state.positions.thief
        if (
            scenario == "barrier_capture"
            and cop.row == thief.row
            and (cop.col + 1 == thief.col)
        ):
            return {
                **_base(session),
                "action_kind": "barrier",
                "direction": None,
                "x": thief.row,
                "y": thief.col,
            }
        direction = (
            "S" if cop.row < thief.row else ("E" if cop.col < thief.col else "STAY")
        )
    kind = "stay" if direction == "STAY" else "move"
    return {
        **_base(session),
        "action_kind": kind,
        "direction": direction,
        "x": None,
        "y": None,
    }
