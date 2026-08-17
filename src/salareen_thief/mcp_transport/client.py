"""FastMCP HTTP client connector."""

from typing import Any

from fastmcp import Client

from .contracts import TOOL_RECEIVE
from .results import TransportError, TransportRejected


async def send_geometry(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        async with Client(url) as client:
            result = await client.call_tool(TOOL_RECEIVE, {"payload": payload})
    except Exception as error:
        return TransportRejected(
            TransportError.REMOTE_ERROR, type(error).__name__
        ).as_dict()
    structured = result.structured_content
    if type(structured) is not dict:
        return TransportRejected(
            TransportError.REMOTE_ERROR, "missing structured response"
        ).as_dict()
    return structured
