"""Peer-owned deterministic match loop used for local production verification."""

import asyncio
import time
from typing import Any

from fastmcp import Client

from .reconciliation import capture, finish
from .session import LiveMatchSession


def _event(session: LiveMatchSession, kind: str, correlation: str | None = None,
           data: dict[str, Any] | None = None) -> None:
    events = getattr(session, "events", None)
    if events:
        events.emit(kind, turn=session.turn_index, phase=session.phase,
                    correlation_id=correlation, data=data)
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
    for _ in range(30):
        try:
            response = await _call(url, tool, payload)
            if response["accepted"]:
                session.phase = "game_initialized"
                session._save("phase", session.phase)
                _event(session, "peer_connected")
                _event(session, "resume_accepted" if recovering else "game_initialized")
                return
        except Exception:
            await asyncio.sleep(0.2)
    raise RuntimeError("peer initialization failed")
def _intent(session: LiveMatchSession, scenario: str) -> dict[str, Any]:
    direction = "STAY"
    if scenario in {"capture", "barrier_capture"} and session.local_role == "cop":
        cop = session.gameplay.state.positions.cop
        thief = session.gameplay.state.positions.thief
        if scenario == "barrier_capture" and cop.row == thief.row and cop.col + 1 == thief.col:
            return {**_base(session, "cop", f"action-{session.turn_index}"),
                    "turn_index": session.turn_index, "action_kind": "barrier",
                    "direction": None, "x": thief.row, "y": thief.col}
        direction = "S" if cop.row < thief.row else "E" if cop.col < thief.col else "STAY"
    kind = "stay" if direction == "STAY" else "move"
    return {**_base(session, session.local_role, f"action-{session.turn_index}"),
            "turn_index": session.turn_index, "action_kind": kind,
            "direction": direction, "x": None, "y": None}
async def _local_turn(url: str, session: LiveMatchSession, scenario: str) -> None:
    _event(session, "strategy_snapshot_created")
    intent = _intent(session, scenario)
    _event(session, "strategy_proposed", intent["correlation_id"],
           {"action_kind": intent["action_kind"]})
    prepared = session.prepare_local(intent)
    if not prepared["accepted"]:
        raise RuntimeError(f"local proposal rejected: {prepared['code']}")
    _event(session, "local_validation", intent["correlation_id"])
    _event(session, "action_prepared", intent["correlation_id"])
    result = None
    for _ in range(300):
        try:
            result = await _call(url, "submit_action_v1", intent)
            break
        except Exception:
            session.phase = "paused_recovering"
            session._save("phase", session.phase)
            _event(session, "paused", intent["correlation_id"])
            _event(session, "reconnect_attempted", intent["correlation_id"])
            await asyncio.sleep(0.2)
    if result is None:
        raise RuntimeError("peer recovery exhausted")
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
    while session.gameplay.state.status.value == "active":
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
            await _local_turn(url, session, scenario)
        else:
            await asyncio.sleep(0.02)
    if session.local_role == "cop":
        if scenario in {"capture", "barrier_capture"}:
            await capture(url, session)
        outcome = "cop_capture" if scenario != "survival" else "thief_survival"
        await finish(url, session, outcome, session.gameplay.score())
    else:
        while session.phase != "shutdown":
            await asyncio.sleep(0.02)
        await asyncio.sleep(0.5)
