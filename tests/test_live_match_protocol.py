from salareen_thief.live_match.endpoints import (
    validate_endpoint,
    validate_runtime_endpoint,
)
from salareen_thief.live_match.journal import Journal
from salareen_thief.live_match.session import LiveMatchSession


def action(**changes):
    value = {
        "protocol_version": "1.0-provisional",
        "correlation_id": "a-1",
        "sender_role": "cop",
        "game_id": "game",
        "session_id": "session",
        "game_number": 1,
        "turn_index": 1,
        "action_kind": "stay",
        "direction": "STAY",
        "x": None,
        "y": None,
    }
    value.update(changes)
    return value


def test_acknowledged_action_is_not_reapplied_after_recovery(tmp_path):
    path = tmp_path / "thief.sqlite3"
    journal = Journal(path)
    session = LiveMatchSession("thief", "game", "session", 1, journal)
    session.turn_index = 1
    session._save("turn", "1")
    first = session.handle("submit_action_v1", action())
    assert session.applied_actions == 1
    journal.close()
    recovered = LiveMatchSession("thief", "game", "session", 1, Journal(path))
    assert recovered.handle("submit_action_v1", action()) == first
    assert recovered.applied_actions == 1


def test_expected_role_and_duplicate_mismatch(tmp_path):
    session = LiveMatchSession(
        "thief", "game", "session", 1, Journal(tmp_path / "thief.sqlite3")
    )
    session.turn_index = 1
    assert session.handle("submit_action_v1", action(sender_role="thief"))["code"] == (
        "WRONG_EXPECTED_ROLE"
    )
    assert session.handle("submit_action_v1", action())["accepted"]
    assert session.handle("submit_action_v1", action(direction="N"))["code"] == (
        "DUPLICATE_MISMATCH"
    )


def test_endpoint_policy_rejects_query():
    assert validate_endpoint(
        "http://127.0.0.1:8802/mcp", mode="local", host="127.0.0.1", permitted_port=8802
    )
    try:
        validate_endpoint(
            "https://peer.example:443/mcp?token=x",
            mode="remote",
            host="peer.example",
            permitted_port=443,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("query string accepted")
def test_runtime_endpoint_accepts_public_https_default_port():
    endpoint = "https://peer.example.test/mcp"
    assert validate_runtime_endpoint(endpoint, 8802) == endpoint

