"""FastMCP server exposing the Stage 2 provisional contract."""

from typing import Any

from fastmcp import FastMCP

from .client import send_geometry
from .contracts import TOOL_RECEIVE, TOOL_RELAY
from .orchestrator import PeerOrchestrator
from .results import TransportError, TransportRejected


def build_server(
    role: str, session_id: str, opponent_url: str | None = None
) -> tuple[FastMCP, PeerOrchestrator]:
    if role not in {"cop", "thief"}:
        raise ValueError("role must be cop or thief")
    orchestrator = PeerOrchestrator(session_id)
    server = FastMCP(f"salareen-{role}")

    @server.tool(name=TOOL_RECEIVE)
    def receive_geometry(payload: dict[str, Any]) -> dict[str, Any]:
        return orchestrator.receive(payload).as_dict()

    @server.tool(name=TOOL_RELAY)
    async def relay_geometry(payload: dict[str, Any]) -> dict[str, Any]:
        prepared = orchestrator.prepare_outbound(payload)
        if isinstance(prepared, TransportRejected):
            return prepared.as_dict()
        if opponent_url is None:
            return TransportRejected(
                TransportError.REMOTE_ERROR, "opponent URL is not configured"
            ).as_dict()
        return await send_geometry(opponent_url, prepared.message.as_dict())

    return server, orchestrator
