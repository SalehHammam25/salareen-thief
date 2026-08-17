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
        cached = False
        if type(payload) is dict and all(key in payload for key in (
                "game_id", "session_id", "correlation_id")):
            key = (payload["game_id"], payload["session_id"], tool,
                   payload["correlation_id"])
            cached = session.journal.lookup(key) is not None
        if events:
            events.emit("message_received", turn=session.turn_index,
                        phase=session.phase, correlation_id=correlation,
                        data={"tool": tool})
        result = session.handle(tool, payload)
        if result["accepted"] and session.gameplay and not cached:
            if tool == "publish_scent_v1":
                assert session.gameplay.stage4.receive_scent(
                    payload["turn_index"], payload)
            elif tool == "send_language_hint_v1":
                assert session.gameplay.stage4.receive_hint(
                    payload["turn_index"], payload["text"])
        if events:
            kind = "message_accepted" if result["accepted"] else "message_rejected"
            events.emit(kind, turn=session.turn_index, phase=session.phase,
                        correlation_id=correlation,
                        result_code=result.get("code") or result.get("status"))
            accepted_events = {"initialize_game_v1": "game_initialized",
                "submit_action_v1": "action_applied",
                "acknowledge_action_v1": "ack_received",
                "publish_scent_v1": "scent_updated",
                "send_language_hint_v1": "hint_received",
                "submit_capture_claim_v1": "capture_evaluated",
                "resume_match_v1": "resume_accepted",
                "reconcile_terminal_v1": "terminal_agreed",
                "reconcile_score_v1": "score_agreed",
                "shutdown_match_v1": "shutdown"}
            if result["accepted"]:
                event_name = "duplicate_replayed" if cached else accepted_events[tool]
                events.emit(event_name, turn=session.turn_index,
                            phase=session.phase, correlation_id=correlation,
                            result_code=result["status"])
        return result

    for tool_name in SCHEMAS:
        def handler(payload: dict[str, Any], name: str = tool_name) -> dict[str, Any]:
            return dispatch(name, payload)

        handler.__name__ = tool_name
        server.tool(name=tool_name)(handler)
    return server
