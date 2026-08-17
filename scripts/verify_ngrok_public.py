"""Credential-safe, temporary ngrok verification for the test MCP endpoint."""

import argparse
import asyncio
import subprocess
import sys
import time
from collections.abc import Sequence

from fastmcp import Client

from salareen_thief.cloud_tunneling.ngrok_adapter import NgrokProvider
from salareen_thief.cloud_tunneling.ngrok_config import NgrokConfig
from salareen_thief.cloud_tunneling.ngrok_probe import assigned_urls
from salareen_thief.cloud_tunneling.reconnection import (
    ResumeDecision,
    ResumeIdentity,
    decide_resume,
)
from salareen_thief.cloud_tunneling.watchdog import evaluate_watchdog
from salareen_thief.mcp_transport.contracts import PROTOCOL_VERSION, TOOL_RECEIVE

API_URL = "http://127.0.0.1:4040/api/tunnels"


def launch(arguments: Sequence[str]) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        arguments,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def stop(process: subprocess.Popen[bytes] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def wait_for_urls() -> tuple[str, ...]:
    for _ in range(60):
        urls = assigned_urls(API_URL)
        secure = tuple(url for url in urls if url.startswith("https://"))
        if secure:
            return secure
        time.sleep(0.25)
    raise RuntimeError("ngrok endpoint was not ready")


def discover_stable_domain(ngrok: str, port: int) -> str:
    first: subprocess.Popen[bytes] | None = None
    second: subprocess.Popen[bytes] | None = None
    try:
        first = launch((ngrok, "http", str(port)))
        first_urls = wait_for_urls()
        if len(first_urls) != 1:
            raise RuntimeError("expected one account development endpoint")
        stop(first)
        first = None
        second = launch((ngrok, "http", str(port)))
        second_urls = wait_for_urls()
        if second_urls != first_urls:
            raise RuntimeError("account endpoint changed after restart")
        return first_urls[0].removeprefix("https://")
    finally:
        stop(first)
        stop(second)


async def verify_public(domain: str, port: int) -> None:
    config = NgrokConfig(port, domain, readiness_attempts=60, readiness_interval=0.25)
    provider = NgrokProvider(config)
    local_url = f"http://127.0.0.1:{port}/mcp"
    first = await provider.start(local_url)
    if not hasattr(first, "endpoint") or not await provider.healthy():
        raise RuntimeError("explicit stable endpoint was not healthy")
    async with Client(f"{config.public_url}/mcp") as client:
        result = await client.call_tool(
            TOOL_RECEIVE,
            {
                "payload": {
                    "protocol_version": PROTOCOL_VERSION,
                    "correlation_id": "stage5-public-health",
                    "sender_role": "cop",
                    "x": 1,
                    "y": 2,
                    "step": 0,
                }
            },
        )
        if result.data["accepted"] is not True:
            raise RuntimeError("public MCP tool rejected test payload")
    await provider.stop()
    if await provider.healthy():
        raise RuntimeError("stopped provider reported healthy")
    identity = ResumeIdentity(
        "game-test", "stage5-public-test", PROTOCOL_VERSION, 0, "WAITING"
    )
    if decide_resume(identity, None) is not ResumeDecision.PAUSE:
        raise RuntimeError("disconnect did not pause")
    if not evaluate_watchdog(0, 61, 60).expired:
        raise RuntimeError("watchdog did not expire")
    second = await provider.start(local_url)
    if first != second:
        raise RuntimeError("stable endpoint changed after explicit restart")
    if decide_resume(identity, identity) is not ResumeDecision.RESUME:
        raise RuntimeError("matching identity did not resume")
    await provider.stop()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ngrok", required=True)
    parser.add_argument("--port", required=True, type=int)
    args = parser.parse_args()
    peer = launch(
        (
            sys.executable,
            "-m",
            "salareen_thief.mcp_transport.peer",
            "--role",
            "thief",
            "--session-id",
            "stage5-public-test",
            "--port",
            str(args.port),
        )
    )
    try:
        domain = discover_stable_domain(args.ngrok, args.port)
        asyncio.run(verify_public(domain, args.port))
        print("stable_domain=<redacted> restart=same mcp=passed shutdown=passed")
    finally:
        stop(peer)


if __name__ == "__main__":
    main()
