"""Bounded remote operation retries with injectable waiting."""

import asyncio
from collections.abc import Awaitable, Callable

from .failures import classify_failure
from .models import FailureKind, TunnelFailure


async def bounded_remote_call[T](
    operation: Callable[[], Awaitable[T]],
    *,
    timeout: float,
    backoff: float,
    max_retries: int,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> T | TunnelFailure:
    last = TunnelFailure(FailureKind.ATTRIBUTION_UNKNOWN)
    for attempt in range(max_retries + 1):
        try:
            return await asyncio.wait_for(operation(), timeout)
        except asyncio.CancelledError:
            raise
        except Exception as error:
            last = classify_failure(error)
            if attempt < max_retries:
                await sleep(backoff)
    return TunnelFailure(
        FailureKind.RETRIES_EXHAUSTED,
        f"attempts={max_retries + 1}; last={last.kind}",
    )
