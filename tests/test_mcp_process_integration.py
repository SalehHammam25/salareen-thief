"""Real localhost HTTP integration using two independent processes."""

import asyncio
import socket
import subprocess
import sys
import time
from contextlib import ExitStack

from fastmcp import Client

from salareen_thief.mcp_transport.contracts import (
    PROTOCOL_VERSION,
    TOOL_RECEIVE,
    TOOL_RELAY,
)


def free_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


def wait_for_port(port: int) -> None:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        with socket.socket() as probe:
            probe.settimeout(0.1)
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.05)
    raise AssertionError(f"peer port {port} did not open")


def start_peer(role: str, port: int, opponent: int) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "salareen_thief.mcp_transport.peer",
            "--role",
            role,
            "--port",
            str(port),
            "--opponent-url",
            f"http://127.0.0.1:{opponent}/mcp",
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def stop_peer(peer: subprocess.Popen[bytes]) -> None:
    if peer.poll() is None:
        peer.terminate()
        try:
            peer.wait(timeout=5)
        except subprocess.TimeoutExpired:
            peer.kill()
            peer.wait(timeout=5)


def message(correlation: str, role: str) -> dict[str, object]:
    return {
        "protocol_version": PROTOCOL_VERSION,
        "correlation_id": correlation,
        "sender_role": role,
        "x": 1,
        "y": 2,
        "step": 0,
    }


def test_two_processes_serve_and_call_symmetrically() -> None:
    thief_port, cop_port = free_port(), free_port()
    with ExitStack() as stack:
        thief = start_peer("thief", thief_port, cop_port)
        cop = start_peer("cop", cop_port, thief_port)
        stack.callback(stop_peer, thief)
        stack.callback(stop_peer, cop)
        wait_for_port(thief_port)
        wait_for_port(cop_port)

        async def scenario() -> None:
            async with Client(f"http://127.0.0.1:{thief_port}/mcp") as client:
                direct = await client.call_tool(
                    TOOL_RECEIVE, {"payload": message("cop-to-thief", "cop")}
                )
                relayed = await client.call_tool(
                    TOOL_RELAY, {"payload": message("thief-to-cop", "thief")}
                )
            async with Client(f"http://127.0.0.1:{cop_port}/mcp") as client:
                reverse = await client.call_tool(
                    TOOL_RELAY, {"payload": message("cop-relay-to-thief", "cop")}
                )
            assert direct.data["accepted"] is True
            assert relayed.data["accepted"] is True
            assert reverse.data["accepted"] is True

        asyncio.run(scenario())
        assert thief.poll() is None
        assert cop.poll() is None
    assert thief.poll() is not None
    assert cop.poll() is not None
