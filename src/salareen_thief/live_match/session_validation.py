"""Production live-session semantic validation."""

from typing import Any

from . import protocol


def validate_semantics(session: Any, tool: str, payload: dict[str, Any]):
    if tool == "security_bootstrap_v1": return None
    if tool == "security_commit_v1":
        if not session.security.peer_verified: return "SECURITY_REQUIRED", "bootstrap"
        return None if payload["turn_index"] == session.turn_index else ("INVALID_TURN", "turn_index")
    if tool == "security_nonce_audit_v1":
        return None if session.phase in {"terminal", "shutdown"} else ("ILLEGAL_PHASE", "phase")
    if tool == "initialize_game_v1":
        if session.security and not session.security.peer_verified: return "SECURITY_REQUIRED", "bootstrap"
        if session.phase not in {"configured", "game_initialized"}: return "ILLEGAL_PHASE", "phase"
        return None if payload["starting_role"] == "thief" else ("INVALID_ROLE", "starting_role")
    if tool == "resume_match_v1":
        received = session.journal.get_state(session.game_id, session.session_id, "last_received_turn")
        pending = received is not None and payload["turn_index"] == int(received)
        if (payload["turn_index"] != session.turn_index and not pending) or payload["phase"] != session.phase:
            session._save("phase", "aborted"); session.phase = "aborted"
            return "IDENTITY_MISMATCH", "recovery_identity"
        return None
    if payload["turn_index"] != session.turn_index: return "INVALID_TURN", "turn_index"
    allowed = {"reconcile_terminal_v1", "reconcile_score_v1", "shutdown_match_v1"}
    if session.phase in {"terminal", "shutdown"} and tool not in allowed: return "EPISODE_TERMINAL", "phase"
    if tool == "submit_action_v1":
        if session.security:
            try: session.security.accept_reveal(payload["correlation_id"], dict(payload))
            except (KeyError, ValueError): return "SECURITY_REJECTED", "reveal"
        issue = protocol.validate_action(payload, session.turn_index)
        return issue or (session.gameplay and session.gameplay.validate_payload(payload))
    if tool == "submit_capture_claim_v1" and session.gameplay:
        return session.gameplay.capture(payload, apply=False)
    if tool == "reconcile_score_v1":
        scores = {"cop_capture": (20, 5), "thief_survival": (5, 10),
                  "tie": (2, 2), "technical_loss": (0, 0)}
        if scores.get(payload["outcome"]) != (payload["cop_score"], payload["thief_score"]):
            return "SCORE_MISMATCH", "scores"
    return None
