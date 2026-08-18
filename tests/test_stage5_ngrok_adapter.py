"""Deterministic ngrok adapter lifecycle tests without credentials."""

import asyncio

from salareen_thief.cloud_tunneling.models import (
    FailureKind,
    TunnelFailure,
    TunnelReady,
)
from salareen_thief.cloud_tunneling.ngrok_adapter import NgrokProvider
from salareen_thief.cloud_tunneling.ngrok_config import NgrokConfig


class FakeProcess:
    def __init__(self, running: bool = True) -> None:
        self.alive = running
        self.terminated = 0
        self.killed = 0

    def running(self) -> bool:
        return self.alive

    def terminate(self) -> None:
        self.terminated += 1
        self.alive = False

    def wait(self, timeout: float) -> None:
        return None

    def kill(self) -> None:
        self.killed += 1
        self.alive = False


class Harness:
    def __init__(self) -> None:
        self.processes: list[FakeProcess] = []
        self.commands: list[tuple[str, ...]] = []
        self.probes: list[str] = []
        self.urls = ("https://stable.example.test",)

    def factory(self, port: int, url: str):
        assert (port, url) == (8802, "https://stable.example.test")
        process = FakeProcess()
        self.processes.append(process)
        return process

    async def probe(self, url: str) -> bool:
        self.probes.append(url)
        return True

    async def read_urls(self, _: str) -> tuple[str, ...]:
        return self.urls

    def command(self, *arguments: str) -> bool:
        self.commands.append(arguments)
        return True

    async def sleep(self, _: float) -> None:
        return None

    def provider(self, probe=None) -> NgrokProvider:
        return NgrokProvider(
            NgrokConfig(8802, "stable.example.test", readiness_attempts=2),
            process_factory=self.factory,
            probe=probe or self.probe,
            urls=self.read_urls,
            command_check=self.command,
            sleep=self.sleep,
        )


def test_start_checks_local_server_agent_and_exact_assigned_url() -> None:
    async def scenario() -> None:
        harness = Harness()
        provider = harness.provider()
        result = await provider.start("http://127.0.0.1:8802/mcp")
        assert isinstance(result, TunnelReady)
        assert result.endpoint.url == "https://stable.example.test"
        assert harness.commands == [("version",), ("config", "check")]
        assert harness.probes == ["http://127.0.0.1:8802/mcp"]

    asyncio.run(scenario())


def test_random_or_missing_agent_url_is_never_accepted() -> None:
    async def scenario() -> None:
        harness = Harness()
        harness.urls = ("https://random.example.test",)
        provider = harness.provider()
        result = await provider.start("http://127.0.0.1:8802/mcp")
        assert result == TunnelFailure(FailureKind.NOT_READY, "public_endpoint")
        assert harness.processes[0].terminated == 1

    asyncio.run(scenario())


def test_local_not_ready_prevents_process_start() -> None:
    async def scenario() -> None:
        harness = Harness()

        async def unavailable(_: str) -> bool:
            return False

        provider = harness.provider(unavailable)
        result = await provider.start("http://127.0.0.1:8802/mcp")
        assert result == TunnelFailure(FailureKind.NOT_READY, "local_mcp")
        assert harness.processes == []

    asyncio.run(scenario())


def test_restart_reuses_domain_and_shutdown_is_idempotent() -> None:
    async def scenario() -> None:
        harness = Harness()
        provider = harness.provider()
        first = await provider.start("http://127.0.0.1:8802/mcp")
        assert await provider.healthy() is True
        await provider.stop()
        await provider.stop()
        second = await provider.start("http://127.0.0.1:8802/mcp")
        assert first == second
        await provider.stop()
        assert [item.terminated for item in harness.processes] == [1, 1]

    asyncio.run(scenario())


def test_repeated_start_does_not_orphan_first_process() -> None:
    async def scenario() -> None:
        harness = Harness()
        provider = harness.provider()
        assert isinstance(
            await provider.start("http://127.0.0.1:8802/mcp"), TunnelReady
        )
        repeated = await provider.start("http://127.0.0.1:8802/mcp")
        assert repeated == TunnelFailure(FailureKind.START_FAILED, "already_running")
        assert len(harness.processes) == 1
        await provider.stop()

    asyncio.run(scenario())
