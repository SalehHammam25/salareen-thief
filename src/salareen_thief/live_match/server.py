"""FastMCP exposure for all live-match v1 tools."""

from typing import Any

from fastmcp import FastMCP

from .protocol import SCHEMAS
from .session import LiveMatchSession


def build_live_server(session: LiveMatchSession) -> FastMCP:
    server = FastMCP(f"salareen-{session.local_role}-live-match")

    def dispatch(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
        return session.handle(tool, payload)

    for tool_name in SCHEMAS:
        def handler(payload: dict[str, Any], name: str = tool_name) -> dict[str, Any]:
            return dispatch(name, payload)

        handler.__name__ = tool_name
        server.tool(name=tool_name)(handler)
    return server
