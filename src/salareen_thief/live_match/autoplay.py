"""Peer-owned deterministic match loop used for local production verification."""

import asyncio
import time
from typing import Any

from fastmcp import Client

from .lifecycle import wait_peer_closed
from .reconciliation import capture, finish
from .recovery import bounded_call
from .session import LiveMatchSession
from .test_strategy import choose


def _event(session: LiveMatchSession, kind: str, correlation: str | None = None,
           data: dict[str, Any] | None = None, turn: int | None = None) -> None:
    events = getattr(session, "events", None)
    if events:
        events.emit(kind, turn=session.turn_index if turn is None else turn,
                    phase=session.phase, correlation_id=correlation, data=data)
def _base(session: LiveMatchSession, sender: str, correlation: str) -> dict[str, Any]:
    return {"protocol_version": "1.0-provisional", "correlation_id": correlation,
            "sender_role": sender, "game_id": session.game_id,
            "session_id": session.session_id, "game_number": session.game_number}
async def _call(url: str, tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    async with Client(url) as client:
        result = await client.call_tool(tool, {"payload": payload})
    if not isinstance(result.structured_content, dict):
        raise RuntimeError("invalid peer response")
    return result.structured_content
async def _connect(url: str, session: LiveMatchSession) -> None:
    recovering = session.phase == "paused_recovering"
    tool = "resume_match_v1" if recovering else "initialize_game_v1"
    fields = ({"turn_index": session.turn_index, "phase": session.phase}
              if recovering else {"config_schema_version": "3.0.0",
                                  "starting_role": "thief"})
    payload = {**_base(session, session.local_role, f"init-{session.local_role}"),
               **fields}
    if recovering:
        payload.pop("game_number")
        field = session.recovery_mismatch
        replacements = {"game_id": "mismatched-game", "session_id": "mismatched-session",
                        "protocol_version": "mismatched-version",
                        "turn_index": session.turn_index + 1,
                        "phase": "mismatched-phase"}
        if field:
            payload[field] = replacements[field]
    response = await bounded_call(session, payload["correlation_id"],
        lambda: _call(url, tool, payload), pause=recovering)
    if not response["accepted"]:
        raise RuntimeError(f"peer initialization rejected: {response['code']}")
    session.phase = "game_initialized"
    session._save("phase", session.phase)
    boundary = payload.get("turn_index", 0)
    _event(session, "peer_connected", turn=boundary)
    _event(session, "resume_accepted" if recovering else "game_initialized",
           turn=boundary)
async def _local_turn(url: str, session: LiveMatchSession, scenario: str) -> None:
    _event(session, "strategy_snapshot_created")
    intent = choose(session, scenario)
    _event(session, "strategy_proposed", intent["correlation_id"],
           {"action_kind": intent["action_kind"]})
    prepared = session.prepare_local(intent)
    if not prepared["accepted"]:
        raise RuntimeError(f"local proposal rejected: {prepared['code']}")
    _event(session, "local_validation", intent["correlation_id"])
    _event(session, "action_prepared", intent["correlation_id"])
    result = await bounded_call(session, intent["correlation_id"],
        lambda: _call(url, "submit_action_v1", intent))
    if not result["accepted"]:
        raise RuntimeError(f"remote action rejected: {result['code']}")
    if getattr(session, "crash_after_send", -1) == session.turn_index:
        _event(session, "controlled_interruption", intent["correlation_id"])
        raise RuntimeError("controlled interruption after remote application")
    remote = session.remote_role
    ack = {**_base(session, remote, f"ack-{session.turn_index}"),
           "turn_index": session.turn_index,
           "action_correlation_id": intent["correlation_id"], "result": "applied",
           "result_code": "OK", "next_turn_index": session.turn_index + 1,
           "next_role": remote}
    if not session.handle("acknowledge_action_v1", ack)["accepted"]:
        raise RuntimeError("acknowledgement rejected")
    _event(session, "ack_received", ack["correlation_id"])
    _event(session, "action_applied", intent["correlation_id"])
    scent, hint = await session.gameplay.stage4.outbound(
        session.game_id, session.turn_index, session.gameplay.scent)
    scent_message = {**_base(session, session.local_role,
                     f"scent-{session.turn_index}"),
                     "turn_index": session.turn_index, **scent}
    assert (await _call(url, "publish_scent_v1", scent_message))["accepted"]
    _event(session, "scent_updated", scent_message["correlation_id"])
    _event(session, "token_budget_updated", data={
        "consumed": session.gameplay.stage4.ledger.consumed})
    if hint:
        hint_message = {**_base(session, session.local_role,
                        f"hint-{session.turn_index}"),
                        "turn_index": session.turn_index, **hint}
        assert (await _call(url, "send_language_hint_v1", hint_message))["accepted"]
        _event(session, "hint_sent", hint_message["correlation_id"])
async def run_autoplay(url: str, session: LiveMatchSession, scenario: str) -> None:
    await _connect(url, session)
    while (session.gameplay.state.status.value == "active" and
           session.phase != "aborted"):
        positions = session.gameplay.state.positions
        if positions.cop == positions.thief:
            break
        active = "thief" if session.turn_index % 2 == 0 else "cop"
        if active == session.local_role:
            if (session.turn_index and
                    (session.gameplay.stage4.last_scent_turn != session.turn_index or
                     session.gameplay.stage4.last_hint_turn != session.turn_index)):
                started = getattr(session, "stage4_wait_started", time.monotonic())
                session.stage4_wait_started = started
                if time.monotonic() - started >= 1 and session.phase != "paused_recovering":
                    session.phase = "paused_recovering"
                    session._save("phase", session.phase)
                    _event(session, "paused")
                await asyncio.sleep(0.02)
                continue
            session.stage4_wait_started = time.monotonic()
            await asyncio.sleep(getattr(session, "action_delay", 0.0))
            if session.phase == "aborted":
                break
            await _local_turn(url, session, scenario)
        else:
            await asyncio.sleep(0.02)
    if session.phase == "aborted":
        return
    if session.local_role == "cop":
        if scenario == "survival":
            while (session.gameplay.stage4.last_scent_turn != session.turn_index or
                   session.gameplay.stage4.last_hint_turn != session.turn_index):
                await asyncio.sleep(0.02)
        if scenario in {"capture", "barrier_capture", "trapped", "capture_priority"}:
            await capture(url, session)
        outcome = "cop_capture" if scenario != "survival" else "thief_survival"
        await finish(url, session, outcome, session.gameplay.score())
    else:
        while session.phase != "shutdown":
            await asyncio.sleep(0.02)
        await wait_peer_closed(url)
