"""Network configuration and reliability tests."""

import asyncio
import json
from pathlib import Path

import pytest

from salareen_thief.mcp_transport.config import load_network_config
from salareen_thief.mcp_transport.reliability import (
    ReliabilityPolicy,
    watchdog_expired,
    with_retries,
)
from salareen_thief.mcp_transport.results import TransportError, TransportRejected


def write_configs(tmp_path: Path, private_extra: str = "") -> tuple[Path, Path]:
    shared = tmp_path / "game.json"
    private = tmp_path / "game.toml"
    shared.write_text(
        json.dumps(
            {
                "network_and_league": {
                    "response_timeout_sec": 30,
                    "watchdog_timeout_sec": 60,
                },
                "rate_limiter_gatekeeper": {
                    "retry_backoff_sec": 5,
                    "max_retries": 3,
                },
            }
        ),
        encoding="utf-8",
    )
    private.write_text(
        '[network]\nmy_port = 8802\nopponent_url = "http://127.0.0.1:8801/mcp"\n'
        + private_extra,
        encoding="utf-8",
    )
    return shared, private


def test_shared_timeout_values_override_private_duplicates(tmp_path: Path) -> None:
    shared, private = write_configs(
        tmp_path, "response_timeout_sec = 1\nwatchdog_timeout_sec = 2\n"
    )
    result = load_network_config(shared, private)
    assert result.response_timeout_sec == 30
    assert result.watchdog_timeout_sec == 60
    assert result.my_port == 8802
    assert result.retry_backoff_sec == 5
    assert result.max_retries == 3


@pytest.mark.parametrize("value", ["true", "0", "-1"])
def test_invalid_private_port_rejected(tmp_path: Path, value: str) -> None:
    shared, private = write_configs(tmp_path)
    private.write_text(
        f'[network]\nmy_port = {value}\nopponent_url = "http://peer/mcp"\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="my_port"):
        load_network_config(shared, private)


def test_retry_succeeds_after_timeout() -> None:
    calls = 0

    async def operation() -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            await asyncio.sleep(0.02)
        return "ok"

    policy = ReliabilityPolicy(0.001, 1, retry_backoff_sec=0.001, max_retries=1)
    assert asyncio.run(with_retries(operation, policy)) == "ok"
    assert calls == 2


def test_retry_exhaustion_is_bounded() -> None:
    async def operation() -> None:
        await asyncio.sleep(0.02)

    policy = ReliabilityPolicy(0.001, 1, retry_backoff_sec=0.001, max_retries=1)
    result = asyncio.run(with_retries(operation, policy))
    assert isinstance(result, TransportRejected)
    assert result.code is TransportError.RETRIES_EXHAUSTED
    assert result.detail == "2"


def test_cancellation_is_not_swallowed() -> None:
    async def scenario() -> None:
        async def operation() -> None:
            raise asyncio.CancelledError

        with pytest.raises(asyncio.CancelledError):
            await with_retries(operation, ReliabilityPolicy(1, 2))

    asyncio.run(scenario())


def test_watchdog_boundaries() -> None:
    assert watchdog_expired(10, 70, 60) is False
    assert watchdog_expired(10, 70.01, 60) is True
    with pytest.raises(ValueError):
        watchdog_expired(10, 9, 60)
