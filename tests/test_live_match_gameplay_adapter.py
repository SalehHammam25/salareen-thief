from pathlib import Path

from salareen_thief.live_match.gameplay import GameplayAdapter
from salareen_thief.live_match.journal import Journal
from salareen_thief.live_match.session import LiveMatchSession

CONFIG = Path(__file__).parents[1] / "config" / "game.json"


def intent(**changes):
    value = {
        "protocol_version": "1.0-provisional",
        "correlation_id": "move-1",
        "sender_role": "cop",
        "game_id": "game",
        "session_id": "session",
        "game_number": 1,
        "turn_index": 1,
        "action_kind": "move",
        "direction": "S",
        "x": None,
        "y": None,
    }
    value.update(changes)
    return value


def test_session_applies_base_logic_and_restores_state(tmp_path):
    path = tmp_path / "thief.sqlite3"
    journal = Journal(path)
    gameplay = GameplayAdapter(CONFIG)
    session = LiveMatchSession("thief", "game", "session", 1, journal, gameplay)
    session.turn_index = 1
    result = session.handle("submit_action_v1", intent())
    assert result["accepted"] and gameplay.state.valid_steps == 1
    saved = gameplay.snapshot()
    journal.close()
    recovered_journal = Journal(path)
    recovered = GameplayAdapter(
        CONFIG, recovered_journal.get_state("game", "session", "game_state")
    )
    assert recovered.snapshot() == saved


def test_barrier_replaces_movement_and_emits_no_scent(tmp_path):
    gameplay = GameplayAdapter(CONFIG)
    scent = gameplay.scent
    session = LiveMatchSession(
        "thief", "game", "session", 1, Journal(tmp_path / "thief.sqlite3"), gameplay
    )
    session.turn_index = 1
    result = session.handle(
        "submit_action_v1", intent(action_kind="barrier", direction=None, x=0, y=1)
    )
    assert result["accepted"]
    assert gameplay.state.valid_steps == 1 and gameplay.state.barrier_usage == 1
    assert gameplay.scent == scent


def test_acknowledgement_applies_prepared_local_action_once(tmp_path):
    gameplay = GameplayAdapter(CONFIG)
    session = LiveMatchSession(
        "thief", "game", "session", 1, Journal(tmp_path / "thief.sqlite3"), gameplay
    )
    local = intent(
        correlation_id="thief-0",
        sender_role="thief",
        turn_index=0,
        action_kind="stay",
        direction="STAY",
    )
    assert session.prepare_local(local)["accepted"]
    acknowledgement = {
        "protocol_version": "1.0-provisional",
        "correlation_id": "ack-0",
        "sender_role": "cop",
        "game_id": "game",
        "session_id": "session",
        "game_number": 1,
        "turn_index": 0,
        "action_correlation_id": "thief-0",
        "result": "applied",
        "result_code": "OK",
        "next_turn_index": 1,
        "next_role": "cop",
    }
    first = session.handle("acknowledge_action_v1", acknowledgement)
    assert first["accepted"] and gameplay.state.valid_steps == 1
    assert session.handle("acknowledge_action_v1", acknowledgement) == first
    assert gameplay.state.valid_steps == 1
