"""Production ngrok adapter using an account-assigned stable domain."""

import asyncio
import subprocess
from collections.abc import Awaitable, Callable

from .models import (
    FailureKind,
    TunnelEndpoint,
    TunnelFailure,
    TunnelReady,
    TunnelResult,
)
from .ngrok_config import NgrokConfig
from .ngrok_probe import assigned_urls, endpoint_reachable
from .ngrok_process import NgrokProcess, command_ok, start_ngrok

AsyncProbe = Callable[[str], Awaitable[bool]]
AsyncUrls = Callable[[str], Awaitable[tuple[str, ...]]]


async def _probe(url: str) -> bool:
    return await asyncio.to_thread(endpoint_reachable, url)


async def _urls(url: str) -> tuple[str, ...]:
    return await asyncio.to_thread(assigned_urls, url)


class NgrokProvider:
    version = "ngrok-v3"

    def __init__(
        self,
        config: NgrokConfig,
        *,
        process_factory: Callable[[int, str], NgrokProcess] = start_ngrok,
        probe: AsyncProbe = _probe,
        urls: AsyncUrls = _urls,
        command_check: Callable[..., bool] = command_ok,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        self._config = config
        self._factory = process_factory
        self._probe = probe
        self._urls = urls
        self._command_check = command_check
        self._sleep = sleep
        self._process: NgrokProcess | None = None

    async def detect_version(self) -> bool:
        return await asyncio.to_thread(self._command_check, "version")

    async def authenticated_agent_ready(self) -> bool:
        return await asyncio.to_thread(self._command_check, "config", "check")

    async def start(self, local_url: str) -> TunnelResult:
        if self._process is not None and self._process.running():
            return TunnelFailure(FailureKind.START_FAILED, "already_running")
        expected = f"http://127.0.0.1:{self._config.local_port}/mcp"
        if local_url != expected or not await self._probe(local_url):
            return TunnelFailure(FailureKind.NOT_READY, "local_mcp")
        try:
            ready = await self.detect_version() and await self.authenticated_agent_ready()
        except (OSError, subprocess.TimeoutExpired):
            ready = False
        if not ready:
            return TunnelFailure(FailureKind.START_FAILED, "ngrok_not_ready")
        try:
            self._process = self._factory(
                self._config.local_port, self._config.public_url
            )
            for _ in range(self._config.readiness_attempts):
                if not self._process.running():
                    return TunnelFailure(FailureKind.PROCESS_EXITED, "ngrok")
                urls = await self._urls(self._config.api_url)
                if self._config.public_url in urls:
                    return TunnelReady(TunnelEndpoint(self._config.public_url))
                await self._sleep(self._config.readiness_interval)
        except (OSError, ValueError):
            await self.stop()
            return TunnelFailure(FailureKind.START_FAILED, "ngrok")
        await self.stop()
        return TunnelFailure(FailureKind.NOT_READY, "public_endpoint")

    async def healthy(self) -> bool:
        return bool(
            self._process
            and self._process.running()
            and await self._probe(f"{self._config.public_url}/mcp")
        )

    async def stop(self) -> None:
        process, self._process = self._process, None
        if process is None or not process.running():
            return
        process.terminate()
        try:
            await asyncio.to_thread(process.wait, 5)
        except subprocess.TimeoutExpired:
            process.kill()
            await asyncio.to_thread(process.wait, 5)
