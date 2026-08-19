import json
from pathlib import Path

import pytest

from salareen_thief.base_logic.state_types import CaptureCause, OutcomeKind
from salareen_thief.live_match.gameplay import GameplayAdapter
from salareen_thief.live_match.journal import Journal
from salareen_thief.live_match.session import LiveMatchSession

CONFIG = Path(__file__).parents[1] / "config" / "game.json"


def action(turn, role, kind="stay", direction="STAY", x=None, y=None):
    return {
        "protocol_version": "1.0-provisional",
        "correlation_id": f"action-{turn}",
        "sender_role": role,
        "game_id": "game",
        "session_id": "session",
        "game_number": 1,
        "turn_index": turn,
        "action_kind": kind,
        "direction": direction,
        "x": x,
        "y": y,
    }


def test_trapped_thief_is_established_by_accepted_actions(tmp_path):
    game = GameplayAdapter(CONFIG)
    cop_steps = (
        ("move", "S", None),
        ("move", "S", None),
        ("move", "E", None),
        ("move", "E", None),
        ("barrier", None, (2, 3)),
        ("barrier", None, (3, 2)),
        ("move", "W", None),
        ("move", "S", None),
        ("move", "S", None),
        ("move", "E", None),
        ("barrier", None, (4, 3)),
        ("move", "S", None),
        ("move", "E", None),
        ("move", "E", None),
        ("move", "N", None),
        ("barrier", None, (3, 4)),
    )
    for turn in range(32):
        kind, direction, target = (
            cop_steps[turn // 2] if turn % 2 else ("stay", "STAY", None)
        )
        payload = action(
            turn,
            "thief" if turn % 2 == 0 else "cop",
            kind,
            direction,
            *(target or (None, None)),
        )
        assert game.validate_payload(payload) is None
        assert game.apply_payload(payload)[0]
    assert game.state.outcome.kind is OutcomeKind.CAPTURE
    assert game.state.outcome.capture_cause is CaptureCause.TRAPPED_THIEF
    assert game.state.valid_steps == 32


def test_capture_has_priority_on_survival_boundary(tmp_path):
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    data["movement_and_barriers"]["max_moves"] = 36
    data["movement_and_barriers"]["survival_threshold"] = 36
    path = tmp_path / "priority.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    game = GameplayAdapter(path)
    cop_moves = ["S", "S", "S", "E", "E"]
    for turn in range(35):
        role = "thief" if turn % 2 == 0 else "cop"
        direction = cop_moves.pop(0) if role == "cop" and cop_moves else "STAY"
        kind = "stay" if direction == "STAY" else "move"
        assert game.apply_payload(action(turn, role, kind, direction))[0]
    thief = game.state.positions.thief
    final = action(35, "cop", "barrier", None, thief.row, thief.col)
    assert game.validate_payload(final) is None and game.apply_payload(final)[0]
    assert game.state.outcome.kind is OutcomeKind.CAPTURE
    assert game.state.outcome.capture_cause is CaptureCause.BARRIER_ON_THIEF
    assert game.state.valid_steps == 36


@pytest.mark.parametrize(
    "field", ["game_id", "session_id", "protocol_version", "turn_index", "phase"]
)
def test_recovery_identity_component_mismatch_aborts(tmp_path, field):
    journal = Journal(tmp_path / f"{field}.sqlite3")
    session = LiveMatchSession("cop", "game", "session", 1, journal)
    session.phase = "paused_recovering"
    session._save("phase", session.phase)
    payload = {
        "protocol_version": "1.0-provisional",
        "correlation_id": "resume",
        "sender_role": "thief",
        "game_id": "game",
        "session_id": "session",
        "turn_index": 0,
        "phase": "paused_recovering",
    }
    payload[field] = 1 if field == "turn_index" else f"wrong-{field}"
    result = session.handle("resume_match_v1", payload)
    assert not result["accepted"] and session.phase == "aborted"
    assert session.applied_actions == 0
