from .recovery import bounded_call
from .session import LiveMatchSession
from .transport_helpers import base_payload, call_peer, emit_event


async def connect(url: str, session: LiveMatchSession) -> None:
    bundle = session.security.bundle()
    security_id = (
        f"security-{session.local_role}-{bundle['public_key'].encode().hex()[:12]}"
    )
    secured = await bounded_call(
        session,
        security_id,
        lambda: call_peer(
            url,
            "security_bootstrap_v1",
            {
                **base_payload(session, session.local_role, security_id),
                "bundle": bundle,
            },
        ),
        pause=False,
    )
    if not secured["accepted"]:
        raise RuntimeError("peer security bootstrap rejected")
    session.security.accept_bundle(secured["bundle"])
    session.gameplay.initialize()
    emit_event(session, "security_verified", security_id)
    recovering = session.phase == "paused_recovering"
    tool = "resume_match_v1" if recovering else "initialize_game_v1"
    fields = (
        {"turn_index": session.turn_index, "phase": session.phase}
        if recovering
        else {"config_schema_version": "3.0.0", "starting_role": "thief"}
    )
    payload = {
        **base_payload(session, session.local_role, f"init-{session.local_role}"),
        **fields,
    }
    if recovering:
        payload.pop("game_number")
        field = session.recovery_mismatch
        replacements = {
            "game_id": "mismatched-game",
            "session_id": "mismatched-session",
            "protocol_version": "mismatched-version",
            "turn_index": session.turn_index + 1,
            "phase": "mismatched-phase",
        }
        if field:
            payload[field] = replacements[field]
    response = await bounded_call(
        session,
        payload["correlation_id"],
        lambda: call_peer(url, tool, payload),
        pause=recovering,
    )
    if not response["accepted"]:
        raise RuntimeError(f"peer initialization rejected: {response['code']}")
    session.phase = "game_initialized"
    session._save("phase", session.phase)
    boundary = payload.get("turn_index", 0)
    emit_event(session, "peer_connected", turn=boundary)
    emit_event(
        session, "resume_accepted" if recovering else "game_initialized", turn=boundary
    )
