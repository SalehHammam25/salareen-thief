import asyncio

from .recovery import bounded_call
from .session import LiveMatchSession
from .test_strategy import choose
from .transport_helpers import base_payload, call_peer, emit_event


async def local_turn(url: str, session: LiveMatchSession, scenario: str) -> None:
    emit_event(session, "strategy_snapshot_created")
    intent = choose(session, scenario)
    emit_event(
        session,
        "strategy_proposed",
        intent["correlation_id"],
        {"action_kind": intent["action_kind"]},
    )
    prepared = session.prepare_local(intent)
    if not prepared["accepted"]:
        raise RuntimeError(f"local proposal rejected: {prepared['code']}")
    emit_event(session, "local_validation", intent["correlation_id"])
    emit_event(session, "action_prepared", intent["correlation_id"])
    digest = session.security.prepare(intent["correlation_id"], intent)
    commit_message = {
        **base_payload(
            session, session.local_role, f"commit-{intent['correlation_id']}"
        ),
        "turn_index": session.turn_index,
        "action_correlation_id": intent["correlation_id"],
        "digest": digest,
    }
    committed = await _commit_when_verified(url, session, commit_message)
    if not committed["accepted"]:
        raise RuntimeError("remote commitment rejected")
    session.security.acknowledge_outgoing(intent["correlation_id"], intent)
    result = await bounded_call(
        session,
        intent["correlation_id"],
        lambda: call_peer(url, "submit_action_v1", intent),
    )
    if not result["accepted"]:
        raise RuntimeError(f"remote action rejected: {result['code']}")
    if getattr(session, "crash_after_send", -1) == session.turn_index:
        emit_event(session, "controlled_interruption", intent["correlation_id"])
        raise RuntimeError("controlled interruption after remote application")
    remote = session.remote_role
    ack = {
        **base_payload(session, remote, f"ack-{session.turn_index}"),
        "turn_index": session.turn_index,
        "action_correlation_id": intent["correlation_id"],
        "result": "applied",
        "result_code": "OK",
        "next_turn_index": session.turn_index + 1,
        "next_role": remote,
    }
    if not session.handle("acknowledge_action_v1", ack)["accepted"]:
        raise RuntimeError("acknowledgement rejected")
    emit_event(session, "ack_received", ack["correlation_id"])
    emit_event(session, "action_applied", intent["correlation_id"])
    scent, hint = await session.gameplay.stage4.outbound(
        session.game_id, session.turn_index, session.gameplay.scent
    )
    scent_message = {
        **base_payload(session, session.local_role, f"scent-{session.turn_index}"),
        "turn_index": session.turn_index,
        **scent,
    }
    result = await bounded_call(
        session,
        scent_message["correlation_id"],
        lambda: call_peer(url, "publish_scent_v1", scent_message),
    )
    assert result["accepted"]
    emit_event(session, "scent_updated", scent_message["correlation_id"])
    emit_event(
        session,
        "token_budget_updated",
        data={"consumed": session.gameplay.stage4.ledger.consumed},
    )
    if hint:
        hint_message = {
            **base_payload(session, session.local_role, f"hint-{session.turn_index}"),
            "turn_index": session.turn_index,
            **hint,
        }
        result = await bounded_call(
            session,
            hint_message["correlation_id"],
            lambda: call_peer(url, "send_language_hint_v1", hint_message),
        )
        assert result["accepted"]
        emit_event(session, "hint_sent", hint_message["correlation_id"])
    session._save("game_state", session.gameplay.snapshot())
    emit_event(
        session,
        "stage4_boundary_complete",
        intent["correlation_id"],
        {"hint_sent": hint is not None},
    )


async def _commit_when_verified(url, session, message):
    for attempt in range(5):
        result = await bounded_call(
            session,
            message["correlation_id"],
            lambda: call_peer(url, "security_commit_v1", message),
        )
        if result["accepted"] or result.get("code") != "SECURITY_REQUIRED":
            return result
        if attempt < 4:
            await asyncio.sleep(0.25)
    return result
