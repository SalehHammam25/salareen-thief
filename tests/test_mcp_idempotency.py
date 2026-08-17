"""Owner-approved Stage 2 duplicate-request policy tests."""

import asyncio

import pytest

from salareen_thief.mcp_transport.contracts import PROTOCOL_VERSION
from salareen_thief.mcp_transport.orchestrator import PeerOrchestrator
from salareen_thief.mcp_transport.reliability import ReliabilityPolicy, with_retries
from salareen_thief.mcp_transport.results import TransportError


def payload(correlation: str = "request-1", x: int = 1) -> dict[str, object]:
    return {
        "protocol_version": PROTOCOL_VERSION,
        "correlation_id": correlation,
        "sender_role": "cop",
        "x": x,
        "y": 2,
        "step": 0,
    }


def test_identical_duplicate_returns_cached_result_without_mutation() -> None:
    gateway = PeerOrchestrator("game-1")
    first = gateway.receive(payload())
    after_first = gateway.state
    repeated = gateway.receive(payload())
    assert repeated == first
    assert gateway.state is after_first
    assert len(gateway.state.processed) == 1


def test_correlation_reuse_with_different_content_rejects_without_mutation() -> None:
    gateway = PeerOrchestrator("game-1")
    gateway.receive(payload())
    before = gateway.state
    rejected = gateway.receive(payload(x=9))
    assert rejected.code is TransportError.DUPLICATE_MISMATCH
    assert rejected.detail == "request-1"
    assert gateway.state is before


def test_tracking_is_bounded_and_fifo() -> None:
    gateway = PeerOrchestrator("game-1", max_tracked=2)
    for correlation in ("one", "two", "three"):
        gateway.receive(payload(correlation))
    assert [item.correlation_id for item in gateway.state.processed] == ["two", "three"]


def test_tracking_is_local_to_session_and_process_object() -> None:
    first = PeerOrchestrator("game-1")
    second = PeerOrchestrator("game-2")
    assert first.receive(payload()).as_dict()["accepted"] is True
    assert second.receive(payload()).as_dict()["accepted"] is True
    assert first.state.session_id != second.state.session_id


def test_duplicate_sequence_is_repeatable_across_fresh_gateways() -> None:
    def run() -> tuple[list[dict[str, object]], object]:
        gateway = PeerOrchestrator("game-1", max_tracked=2)
        results = [
            gateway.receive(payload("one")),
            gateway.receive(payload("one")),
            gateway.receive(payload("one", x=8)),
        ]
        return [result.as_dict() for result in results], gateway.state

    assert run() == run()


def test_retry_after_lost_response_does_not_repeat_mutation() -> None:
    gateway = PeerOrchestrator("game-1")
    calls = 0

    async def operation() -> object:
        nonlocal calls
        calls += 1
        result = gateway.receive(payload())
        if calls == 1:
            await asyncio.sleep(0.02)
        return result

    policy = ReliabilityPolicy(0.001, 1, retry_backoff_sec=0.001, max_retries=1)
    result = asyncio.run(with_retries(operation, policy))
    assert result == gateway.receive(payload())
    assert calls == 2
    assert len(gateway.state.processed) == 1


@pytest.mark.parametrize("value", ["", None, 4])
def test_invalid_session_identity_rejected(value: object) -> None:
    with pytest.raises(ValueError, match="session_id"):
        PeerOrchestrator(value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [0, -1, True])
def test_invalid_tracking_bound_rejected(value: object) -> None:
    with pytest.raises(ValueError, match="max_tracked"):
        PeerOrchestrator("game-1", value)  # type: ignore[arg-type]
