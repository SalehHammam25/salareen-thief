from typing import Any

from fastmcp import Client

from .session import LiveMatchSession


def emit_event(
    session: LiveMatchSession,
    kind: str,
    correlation: str | None = None,
    data: dict[str, Any] | None = None,
    turn: int | None = None,
) -> None:
    events = getattr(session, "events", None)
    if events:
        events.emit(
            kind,
            turn=session.turn_index if turn is None else turn,
            phase=session.phase,
            correlation_id=correlation,
            data=data,
        )


def base_payload(
    session: LiveMatchSession, sender: str, correlation: str
) -> dict[str, Any]:
    return {
        "protocol_version": "1.0-provisional",
        "correlation_id": correlation,
        "sender_role": sender,
        "game_id": session.game_id,
        "session_id": session.session_id,
        "game_number": session.game_number,
    }


async def call_peer(url: str, tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    async with Client(url) as client:
        result = await client.call_tool(tool, {"payload": payload})
    if not isinstance(result.structured_content, dict):
        raise RuntimeError("invalid peer response")
    return result.structured_content
