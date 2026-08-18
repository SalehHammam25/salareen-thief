import json

from salareen_thief.live_match.event_log import EventLog, reconstruct


def test_log_sequence_reconstructs_without_private_values(tmp_path):
    path = tmp_path / "thief.jsonl"
    log = EventLog(path, "thief", "game", "session")
    log.emit(
        "action_applied", turn=1, phase="game_initialized", correlation_id="action-0"
    )
    log.emit("ack_received", turn=1, phase="game_initialized", correlation_id="ack-0")
    log.emit(
        "terminal_agreed", turn=1, phase="terminal", data={"outcome": "cop_capture"}
    )
    log.emit(
        "score_agreed",
        turn=1,
        phase="terminal",
        data={"cop_score": 20, "thief_score": 5},
    )
    log.emit("shutdown", turn=1, phase="shutdown")
    assert reconstruct(path) == {
        "actions": 1,
        "acknowledgements": 1,
        "terminal": "cop_capture",
        "score": {"cop_score": 20, "thief_score": 5},
        "shutdown": True,
    }
    assert "token" not in json.dumps(reconstruct(path)).casefold()
