"""Provider-neutral tunnel lifecycle and shutdown tests."""

import asyncio

from salareen_thief.cloud_tunneling.lifecycle import TunnelController
from salareen_thief.cloud_tunneling.models import (
    FailureKind,
    TunnelEndpoint,
    TunnelFailure,
    TunnelReady,
)


class FakeProvider:
    version = "fake-1.0"

    def __init__(self, result=None, healthy=True) -> None:
        self.result = result or TunnelReady(TunnelEndpoint("https://thief.example.test/mcp"))
        self.is_healthy = healthy
        self.starts = 0
        self.stops = 0

    async def start(self, local_url: str):
        self.starts += 1
        assert local_url == "http://127.0.0.1:8000/mcp"
        return self.result

    async def healthy(self) -> bool:
        return self.is_healthy

    async def stop(self) -> None:
        self.stops += 1


class RaisingProvider(FakeProvider):
    async def start(self, local_url: str):
        raise ConnectionError("private provider detail")


def test_start_health_stop_lifecycle_is_idempotent() -> None:
    async def scenario() -> None:
        provider = FakeProvider()
        controller = TunnelController(provider)
        ready = await controller.start("http://127.0.0.1:8000/mcp")
        assert isinstance(ready, TunnelReady)
        assert await controller.start("http://127.0.0.1:8000/mcp") == ready
        assert await controller.health() == ready
        await controller.stop()
        await controller.stop()
        assert (provider.starts, provider.stops) == (1, 1)
        assert controller.state.running is False

    asyncio.run(scenario())


def test_invalid_assigned_url_stops_provider_without_leak() -> None:
    async def scenario() -> None:
        provider = FakeProvider(TunnelReady(TunnelEndpoint("http://localhost:8000")))
        result = await TunnelController(provider).start("http://127.0.0.1:8000/mcp")
        assert isinstance(result, TunnelFailure)
        assert result.kind is FailureKind.CONFIGURATION
        assert provider.stops == 1

    asyncio.run(scenario())


def test_health_reports_provider_exit() -> None:
    async def scenario() -> None:
        provider = FakeProvider(healthy=False)
        controller = TunnelController(provider)
        await controller.start("http://127.0.0.1:8000/mcp")
        result = await controller.health()
        assert result == TunnelFailure(FailureKind.PROCESS_EXITED)

    asyncio.run(scenario())


def test_context_manager_prevents_orphan_provider() -> None:
    async def scenario() -> None:
        provider = FakeProvider()
        async with TunnelController(provider) as controller:
            await controller.start("http://127.0.0.1:8000/mcp")
        assert provider.stops == 1

    asyncio.run(scenario())


def test_provider_start_exception_is_typed_and_redacted() -> None:
    async def scenario() -> None:
        result = await TunnelController(RaisingProvider()).start(
            "http://127.0.0.1:8000/mcp"
        )
        assert result == TunnelFailure(FailureKind.START_FAILED, "disconnected")
        assert "private" not in repr(result)

    asyncio.run(scenario())
