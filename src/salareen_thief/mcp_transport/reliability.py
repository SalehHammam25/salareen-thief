"""Bounded retry and watchdog values."""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from .results import TransportError, TransportRejected


@dataclass(frozen=True, slots=True)
class ReliabilityPolicy:
    response_timeout_sec: float
    watchdog_timeout_sec: float
    retry_backoff_sec: float = 5.0
    max_retries: int = 3

    def __post_init__(self) -> None:
        values = (
            self.response_timeout_sec,
            self.watchdog_timeout_sec,
            self.retry_backoff_sec,
        )
        if any(type(value) not in {int, float} or value <= 0 for value in values):
            raise ValueError("timeouts and backoff must be positive numbers")
        if type(self.max_retries) is not int or self.max_retries < 0:
            raise ValueError("max_retries must be a nonnegative integer")


async def with_retries[T](
    operation: Callable[[], Awaitable[T]], policy: ReliabilityPolicy
) -> T | TransportRejected:
    for attempt in range(policy.max_retries + 1):
        try:
            return await asyncio.wait_for(operation(), policy.response_timeout_sec)
        except TimeoutError:
            if attempt == policy.max_retries:
                return TransportRejected(
                    TransportError.RETRIES_EXHAUSTED, str(attempt + 1)
                )
            await asyncio.sleep(policy.retry_backoff_sec)
        except asyncio.CancelledError:
            raise
        except Exception as error:  # transport libraries expose varied failures
            return TransportRejected(TransportError.REMOTE_ERROR, type(error).__name__)
    raise AssertionError("bounded loop exhausted unexpectedly")


def watchdog_expired(last_heartbeat: float, now: float, timeout: float) -> bool:
    if any(type(value) not in {int, float} for value in (last_heartbeat, now, timeout)):
        raise TypeError("watchdog values must be exact numbers")
    if timeout <= 0 or now < last_heartbeat:
        raise ValueError("invalid watchdog timeline")
    return now - last_heartbeat > timeout
