"""FastMCP exposure for all live-match v1 tools."""

from typing import Any

from fastmcp import FastMCP

from .event_log import EventLog
from .protocol import SCHEMAS
from .session import LiveMatchSession


def build_live_server(session: LiveMatchSession, events: EventLog | None = None) -> FastMCP:
    server = FastMCP(f"salareen-{session.local_role}-live-match")

    def dispatch(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
        correlation = payload.get("correlation_id") if type(payload) is dict else None
        if events:
            events.emit("message_received", turn=session.turn_index,
                        phase=session.phase, correlation_id=correlation,
                        data={"tool": tool})
        result = session.handle(tool, payload)
        if events:
            kind = "message_accepted" if result["accepted"] else "message_rejected"
            events.emit(kind, turn=session.turn_index, phase=session.phase,
                        correlation_id=correlation,
                        result_code=result.get("code") or result.get("status"))
        return result

    for tool_name in SCHEMAS:
        def handler(payload: dict[str, Any], name: str = tool_name) -> dict[str, Any]:
            return dispatch(name, payload)

        handler.__name__ = tool_name
        server.tool(name=tool_name)(handler)
    return server
