"""Bounded retry, disconnect, latency, DNS, and TLS tests."""

import asyncio
import ssl
from socket import gaierror

import pytest

from salareen_thief.cloud_tunneling.failures import classify_failure
from salareen_thief.cloud_tunneling.models import FailureKind, TunnelFailure
from salareen_thief.cloud_tunneling.retries import bounded_remote_call


@pytest.mark.parametrize(
    "error,kind",
    [
        (gaierror("dns"), FailureKind.DNS),
        (ssl.SSLError("certificate"), FailureKind.TLS),
        (ConnectionResetError("disconnect"), FailureKind.DISCONNECTED),
        (TimeoutError(), FailureKind.TIMEOUT),
        (RuntimeError("provider"), FailureKind.ATTRIBUTION_UNKNOWN),
    ],
)
def test_failure_categories_are_stable_and_secret_free(error, kind) -> None:
    result = classify_failure(error)
    assert result.kind is kind
    if str(error):
        assert str(error) not in result.detail


def test_retry_success_and_backoff_are_bounded() -> None:
    async def scenario() -> None:
        attempts = 0
        waits: list[float] = []

        async def operation() -> str:
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise ConnectionError("private endpoint")
            return "ready"

        async def sleep(value: float) -> None:
            waits.append(value)

        result = await bounded_remote_call(
            operation, timeout=1, backoff=5, max_retries=3, sleep=sleep
        )
        assert result == "ready"
        assert (attempts, waits) == (3, [5, 5])

    asyncio.run(scenario())


def test_retry_exhaustion_produces_one_deterministic_failure() -> None:
    async def scenario() -> None:
        async def operation() -> None:
            raise ConnectionError("secret URL")

        async def no_wait(_: float) -> None:
            return None

        first = await bounded_remote_call(
            operation, timeout=1, backoff=1, max_retries=2, sleep=no_wait
        )
        second = await bounded_remote_call(
            operation, timeout=1, backoff=1, max_retries=2, sleep=no_wait
        )
        assert first == second == TunnelFailure(
            FailureKind.RETRIES_EXHAUSTED,
            "attempts=3; last=disconnected",
        )

    asyncio.run(scenario())


def test_high_latency_times_out_without_hanging() -> None:
    async def scenario() -> None:
        async def slow() -> None:
            await asyncio.sleep(1)

        async def no_wait(_: float) -> None:
            return None

        result = await bounded_remote_call(
            slow, timeout=0.001, backoff=1, max_retries=0, sleep=no_wait
        )
        assert isinstance(result, TunnelFailure)
        assert result.kind is FailureKind.RETRIES_EXHAUSTED

    asyncio.run(scenario())


def test_caller_cancellation_propagates() -> None:
    async def scenario() -> None:
        async def cancelled() -> None:
            raise asyncio.CancelledError

        with pytest.raises(asyncio.CancelledError):
            await bounded_remote_call(
                cancelled, timeout=1, backoff=1, max_retries=0
            )

    asyncio.run(scenario())
