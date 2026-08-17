"""Peer-owned deterministic match loop used for local production verification."""

import asyncio
from typing import Any

from fastmcp import Client

from .session import LiveMatchSession


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
                return
        except Exception:
            await asyncio.sleep(0.2)
    raise RuntimeError("peer initialization failed")


def _intent(session: LiveMatchSession, scenario: str) -> dict[str, Any]:
    direction = "STAY"
    if scenario == "capture" and session.local_role == "cop":
        cop = session.gameplay.state.positions.cop
        thief = session.gameplay.state.positions.thief
        direction = "S" if cop.row < thief.row else "E" if cop.col < thief.col else "STAY"
    kind = "stay" if direction == "STAY" else "move"
    return {**_base(session, session.local_role, f"action-{session.turn_index}"),
            "turn_index": session.turn_index, "action_kind": kind,
            "direction": direction, "x": None, "y": None}


async def _local_turn(url: str, session: LiveMatchSession, scenario: str) -> None:
    intent = _intent(session, scenario)
    prepared = session.prepare_local(intent)
    if not prepared["accepted"]:
        raise RuntimeError(f"local proposal rejected: {prepared['code']}")
    result = None
    for _ in range(300):
        try:
            result = await _call(url, "submit_action_v1", intent)
            break
        except Exception:
            session.phase = "paused_recovering"
            session._save("phase", session.phase)
            await asyncio.sleep(0.2)
    if result is None:
        raise RuntimeError("peer recovery exhausted")
    if not result["accepted"]:
        raise RuntimeError(f"remote action rejected: {result['code']}")
    remote = session.remote_role
    ack = {**_base(session, remote, f"ack-{session.turn_index}"),
           "turn_index": session.turn_index,
           "action_correlation_id": intent["correlation_id"], "result": "applied",
           "result_code": "OK", "next_turn_index": session.turn_index + 1,
           "next_role": remote}
    if not session.handle("acknowledge_action_v1", ack)["accepted"]:
        raise RuntimeError("acknowledgement rejected")


async def _capture(url: str, session: LiveMatchSession) -> None:
    state = session.gameplay.state
    values = {"turn_index": session.turn_index, "claimant_role": "cop",
              "capture_kind": "cooccupancy", "cop_x": state.positions.cop.row,
              "cop_y": state.positions.cop.col, "thief_x": state.positions.thief.row,
              "thief_y": state.positions.thief.col}
    remote = {**_base(session, "cop", "capture-cop"), **values}
    if not (await _call(url, "submit_capture_claim_v1", remote))["accepted"]:
        raise RuntimeError("remote capture disagreement")
    local = {**_base(session, "thief", "capture-thief"), **values}
    if not session.handle("submit_capture_claim_v1", local)["accepted"]:
        raise RuntimeError("local capture disagreement")


async def _finish(url: str, session: LiveMatchSession, outcome: str,
                  scores: tuple[int, int]) -> None:
    winner = "cop" if outcome == "cop_capture" else "thief"
    loser = "thief" if winner == "cop" else "cop"
    for tool, correlation, fields in (
        ("reconcile_terminal_v1", "terminal", {"outcome": outcome,
         "winner_role": winner, "loser_role": loser, "attribution": "none",
         "reason_code": outcome}),
        ("reconcile_score_v1", "score", {"outcome": outcome,
         "cop_score": scores[0], "thief_score": scores[1]}),
        ("shutdown_match_v1", "shutdown", {"mode": "terminal",
         "reason_code": "complete"})):
        remote = {**_base(session, "cop", f"{correlation}-cop"),
                  "turn_index": session.turn_index, **fields}
        assert (await _call(url, tool, remote))["accepted"]
        local = {**_base(session, "thief", f"{correlation}-thief"),
                 "turn_index": session.turn_index, **fields}
        assert session.handle(tool, local)["accepted"]


async def run_autoplay(url: str, session: LiveMatchSession, scenario: str) -> None:
    await _connect(url, session)
    while session.gameplay.state.status.value == "active":
        positions = session.gameplay.state.positions
        if positions.cop == positions.thief:
            break
        active = "thief" if session.turn_index % 2 == 0 else "cop"
        if active == session.local_role:
            await _local_turn(url, session, scenario)
        else:
            await asyncio.sleep(0.02)
    if session.local_role == "cop":
        if scenario == "capture":
            await _capture(url, session)
        outcome = "cop_capture" if scenario == "capture" else "thief_survival"
        await _finish(url, session, outcome, session.gameplay.score())
    else:
        while session.phase != "shutdown":
            await asyncio.sleep(0.02)
        await asyncio.sleep(0.5)
