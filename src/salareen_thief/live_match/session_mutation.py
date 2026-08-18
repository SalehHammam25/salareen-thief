import json
from typing import Any


def mutate_session(session: Any, tool: str, payload: dict[str, Any]) -> None:
    if tool == "security_bootstrap_v1":
        session.security.accept_bundle(payload["bundle"])
        session.gameplay.initialize()
    elif tool == "security_commit_v1":
        session.security.accept_commit(
            payload["action_correlation_id"], payload["digest"]
        )
    elif tool == "security_nonce_audit_v1":
        session.security.accept_nonce_audit(payload["nonces"])
    elif tool == "initialize_game_v1":
        session.phase = "game_initialized"
        session._save("phase", session.phase)
    elif tool == "submit_action_v1":
        _apply_remote_action(session, payload)
    elif tool == "acknowledge_action_v1" and payload["result"] != "rejected":
        _apply_acknowledged_action(session, payload)
    elif tool == "reconcile_terminal_v1":
        session.phase = "terminal"
        session._save("phase", session.phase)
    elif tool == "resume_match_v1":
        session.recovery_epoch += 1
        session.phase = "game_initialized"
        session._save("phase", session.phase)
    elif tool == "submit_capture_claim_v1" and session.gameplay:
        assert session.gameplay.capture(payload, apply=True) is None
        session._save("game_state", session.gameplay.snapshot())
    elif tool == "shutdown_match_v1":
        session.phase = "shutdown"
        session._save("phase", session.phase)


def _apply_remote_action(session: Any, payload: dict[str, Any]) -> None:
    if session.gameplay:
        accepted, _ = session.gameplay.apply_payload(payload)
        assert accepted
        session._save("game_state", session.gameplay.snapshot())
    session.applied_actions += 1
    session._save("applied", str(session.applied_actions))
    session.turn_index += 1
    session._save("turn", str(session.turn_index))
    session._save("last_received_turn", str(payload["turn_index"]))


def _apply_acknowledged_action(session: Any, payload: dict[str, Any]) -> None:
    pending = session.journal.get_state(
        session.game_id, session.session_id, "pending_action"
    )
    if pending and session.gameplay:
        action = json.loads(pending)
        assert action["correlation_id"] == payload["action_correlation_id"]
        assert session.gameplay.apply_payload(action)[0]
        session._save("game_state", session.gameplay.snapshot())
        session._save("pending_action", "")
    session.turn_index = payload["next_turn_index"]
    session._save("turn", str(session.turn_index))
