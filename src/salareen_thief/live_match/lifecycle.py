"""Observable peer lifecycle boundaries."""

import asyncio
import time
from contextlib import suppress
from urllib.parse import urlsplit


async def wait_peer_closed(url: str, timeout: float = 5) -> None:
    endpoint = urlsplit(url)
    port = endpoint.port or (443 if endpoint.scheme == "https" else 80)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            _, writer = await asyncio.open_connection(endpoint.hostname, port)
        except OSError:
            return
        writer.close()
        with suppress(OSError):
            await writer.wait_closed()
        await asyncio.sleep(0.02)
    raise RuntimeError("peer did not close after shutdown agreement")
