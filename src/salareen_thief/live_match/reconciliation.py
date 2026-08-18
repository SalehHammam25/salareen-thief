"""Capture, terminal, score, and shutdown reconciliation."""

from typing import Any

from fastmcp import Client

from .recovery import bounded_call
from .session import LiveMatchSession


def _base(session: LiveMatchSession, sender: str, correlation: str) -> dict[str, Any]:
    return {
        "protocol_version": "1.0-provisional",
        "correlation_id": correlation,
        "sender_role": sender,
        "game_id": session.game_id,
        "session_id": session.session_id,
        "game_number": session.game_number,
    }


async def _call(url: str, tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    async with Client(url) as client:
        result = await client.call_tool(tool, {"payload": payload})
    assert isinstance(result.structured_content, dict)
    return result.structured_content


def _event(
    session: LiveMatchSession,
    kind: str,
    correlation: str,
    data: dict[str, Any] | None = None,
) -> None:
    events = getattr(session, "events", None)
    if events:
        events.emit(
            kind,
            turn=session.turn_index,
            phase=session.phase,
            correlation_id=correlation,
            data=data,
        )


async def capture(url: str, session: LiveMatchSession) -> None:
    state = session.gameplay.state
    causes = {
        "coordinate_overlap": "cooccupancy",
        "barrier_on_thief": "barrier",
        "trapped_thief": "trapped",
    }
    cause = state.outcome.capture_cause.value if state.outcome else "coordinate_overlap"
    values = {
        "turn_index": session.turn_index,
        "claimant_role": "cop",
        "capture_kind": causes[cause],
        "cop_x": state.positions.cop.row,
        "cop_y": state.positions.cop.col,
        "thief_x": state.positions.thief.row,
        "thief_y": state.positions.thief.col,
    }
    remote = {**_base(session, "cop", "capture-cop"), **values}
    response = await bounded_call(
        session,
        remote["correlation_id"],
        lambda: _call(url, "submit_capture_claim_v1", remote),
        pause=False,
    )
    if not response["accepted"]:
        raise RuntimeError("remote capture disagreement")
    local = {**_base(session, "thief", "capture-thief"), **values}
    if not session.handle("submit_capture_claim_v1", local)["accepted"]:
        raise RuntimeError("local capture disagreement")


async def finish(
    url: str, session: LiveMatchSession, outcome: str, scores: tuple[int, int]
) -> None:
    winner = "cop" if outcome == "cop_capture" else "thief"
    loser = "thief" if winner == "cop" else "cop"
    messages = (
        (
            "reconcile_terminal_v1",
            "terminal",
            {
                "outcome": outcome,
                "winner_role": winner,
                "loser_role": loser,
                "attribution": "none",
                "reason_code": outcome,
            },
        ),
        (
            "reconcile_score_v1",
            "score",
            {"outcome": outcome, "cop_score": scores[0], "thief_score": scores[1]},
        ),
        (
            "shutdown_match_v1",
            "shutdown",
            {"mode": "terminal", "reason_code": "complete"},
        ),
    )
    event_names = {
        "reconcile_terminal_v1": "terminal_agreed",
        "reconcile_score_v1": "score_agreed",
        "shutdown_match_v1": "shutdown",
    }
    for tool, correlation, fields in messages:
        remote = {
            **_base(session, "cop", f"{correlation}-cop"),
            "turn_index": session.turn_index,
            **fields,
        }
        response = await bounded_call(
            session,
            remote["correlation_id"],
            lambda selected=tool, payload=remote: _call(url, selected, payload),
            pause=False,
        )
        assert response["accepted"]
        local = {
            **_base(session, "thief", f"{correlation}-thief"),
            "turn_index": session.turn_index,
            **fields,
        }
        assert session.handle(tool, local)["accepted"]
        _event(session, event_names[tool], local["correlation_id"], fields)
    audit = {
        **_base(session, "cop", "nonce-audit-cop"),
        "turn_index": session.turn_index,
        "nonces": session.security.nonce_audit(),
    }
    response = await bounded_call(
        session,
        audit["correlation_id"],
        lambda: _call(url, "security_nonce_audit_v1", audit),
        pause=False,
    )
    if not response["accepted"]:
        raise RuntimeError("final nonce audit rejected")
