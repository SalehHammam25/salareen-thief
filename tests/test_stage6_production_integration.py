from pathlib import Path

import pytest

from salareen_thief.live_match.gameplay import GameplayAdapter
from salareen_thief.live_match.journal import Journal
from salareen_thief.live_match.security_runtime import LiveSecurity
from salareen_thief.live_match.session import LiveMatchSession
from salareen_thief.security.protocol import SecurityViolation

CONFIG = Path(__file__).parents[1] / "config" / "game.json"


def base(sender, correlation):
    return {
        "protocol_version": "1.0-provisional",
        "correlation_id": correlation,
        "sender_role": sender,
        "game_id": "game",
        "session_id": "session",
        "game_number": 1,
    }


def test_session_bootstraps_before_state_and_secures_real_action(tmp_path):
    cop_security = LiveSecurity("cop", CONFIG, "game")
    thief_security = LiveSecurity("thief", CONFIG, "game")
    gameplay = GameplayAdapter(CONFIG, defer=True)
    session = LiveMatchSession(
        "cop",
        "game",
        "session",
        1,
        Journal(tmp_path / "journal.sqlite3"),
        gameplay,
        cop_security,
    )
    assert not hasattr(gameplay, "state")
    bootstrap = {**base("thief", "security-thief"), "bundle": thief_security.bundle()}
    response = session.handle("security_bootstrap_v1", bootstrap)
    assert response["accepted"] and hasattr(gameplay, "state")
    thief_security.accept_bundle(response["bundle"])
    action = {
        **base("thief", "move-0"),
        "turn_index": 0,
        "action_kind": "stay",
        "direction": "STAY",
        "x": None,
        "y": None,
    }
    digest = thief_security.prepare("move-0", action)
    committed = session.handle(
        "security_commit_v1",
        {
            **base("thief", "commit-move-0"),
            "turn_index": 0,
            "action_correlation_id": "move-0",
            "digest": digest,
        },
    )
    assert committed["accepted"]
    thief_security.acknowledge_outgoing("move-0", action)
    assert session.handle("submit_action_v1", action)["accepted"]
    session.phase = "terminal"
    audit = {
        **base("thief", "nonce-audit"),
        "turn_index": 1,
        "nonces": thief_security.nonce_audit(),
    }
    assert session.handle("security_nonce_audit_v1", audit)["accepted"]
    assert gameplay.state.valid_steps == 1


def test_production_security_rejects_config_and_nonce_tamper():
    cop = LiveSecurity("cop", CONFIG, "game")
    thief = LiveSecurity("thief", CONFIG, "game")
    bundle = thief.bundle()
    bundle["config"] = bundle["config"][:-1] + "A"
    with pytest.raises(SecurityViolation):
        cop.accept_bundle(bundle)
    action = {"correlation_id": "move"}
    digest = thief.prepare("move", action)
    cop.peer_verified = True
    cop.accept_commit("move", digest)
    cop.accept_reveal("move", action)
    with pytest.raises(SecurityViolation):
        cop.accept_nonce_audit({"move": "AAAAAAAAAAAAAAAAAAAAAA=="})
