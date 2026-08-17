"""FastMCP in-memory contract tests."""

import asyncio

from fastmcp import Client

from salareen_thief.mcp_transport.contracts import PROTOCOL_VERSION, TOOL_RECEIVE
from salareen_thief.mcp_transport.server import build_server


def payload(correlation: str = "in-memory-1") -> dict[str, object]:
    return {
        "protocol_version": PROTOCOL_VERSION,
        "correlation_id": correlation,
        "sender_role": "cop",
        "x": 3,
        "y": 4,
        "step": 1,
    }


def test_fastmcp_tool_returns_validated_acknowledgement() -> None:
    async def scenario() -> None:
        server, gateway = build_server("thief", "game-1")
        async with Client(server) as client:
            result = await client.call_tool(TOOL_RECEIVE, {"payload": payload()})
        assert result.data["accepted"] is True
        assert result.data["message"] == payload()
        assert gateway.state.last_received is not None

    asyncio.run(scenario())

def test_fastmcp_tool_rejects_malformed_payload() -> None:
    async def scenario() -> None:
        server, gateway = build_server("thief", "game-1")
        before = gateway.state
        async with Client(server) as client:
            result = await client.call_tool(
                TOOL_RECEIVE, {"payload": payload() | {"x": True}}
            )
        assert result.data["accepted"] is False
        assert gateway.state is before

    asyncio.run(scenario())
