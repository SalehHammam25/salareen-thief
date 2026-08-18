"""Bounded Stage 5 recovery integration tests."""

import asyncio

from salareen_thief.cloud_tunneling.models import (
    FailureKind,
    TunnelEndpoint,
    TunnelFailure,
    TunnelReady,
)
from salareen_thief.cloud_tunneling.reconnection import ResumeDecision, ResumeIdentity
from salareen_thief.cloud_tunneling.recovery import recover_connection


class Provider:
    version = "fake"

    def __init__(self, results) -> None:
        self.results = iter(results)
        self.starts = 0
        self.stops = 0

    async def start(self, _: str):
        self.starts += 1
        return next(self.results)

    async def healthy(self) -> bool:
        return True

    async def stop(self) -> None:
        self.stops += 1


IDENTITY = ResumeIdentity("game", "session", "protocol", 3, "phase")
READY = TunnelReady(TunnelEndpoint("https://stable.example.test"))
FAILED = TunnelFailure(FailureKind.DISCONNECTED)


def run(provider, after=IDENTITY, expired=lambda: False, retries=2):
    async def identity():
        return after

    async def no_wait(_: float) -> None:
        return None

    return asyncio.run(
        recover_connection(
            provider,
            "http://127.0.0.1:8802/mcp",
            IDENTITY,
            identity,
            expired,
            max_retries=retries,
            backoff=0,
            sleep=no_wait,
        )
    )


def test_retry_is_bounded_and_resumes_only_matching_identity() -> None:
    provider = Provider([FAILED, READY])
    result = run(provider)
    assert result.decision is ResumeDecision.RESUME
    assert result.tunnel == READY
    assert (provider.starts, provider.stops) == (2, 2)


def test_identity_mismatch_aborts_and_stops_endpoint() -> None:
    provider = Provider([READY])
    result = run(provider, ResumeIdentity("other", "session", "protocol", 3, "phase"))
    assert result.decision is ResumeDecision.ABORT
    assert provider.stops == 2


def test_exhaustion_stays_paused_without_winner() -> None:
    provider = Provider([FAILED, FAILED, FAILED])
    result = run(provider)
    assert result.decision is ResumeDecision.PAUSE
    assert result.tunnel.kind is FailureKind.RETRIES_EXHAUSTED
    assert provider.starts == 3


def test_expired_watchdog_aborts_before_restart() -> None:
    provider = Provider([])
    result = run(provider, expired=lambda: True)
    assert result.decision is ResumeDecision.ABORT
    assert result.tunnel == TunnelFailure(FailureKind.TIMEOUT, "watchdog")
    assert provider.starts == 0
