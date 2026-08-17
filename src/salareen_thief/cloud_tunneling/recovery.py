"""Bounded same-endpoint recovery with watchdog and identity gates."""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from .models import FailureKind, TunnelFailure, TunnelReady
from .provider import TunnelProvider
from .reconnection import ResumeDecision, ResumeIdentity, decide_resume


@dataclass(frozen=True, slots=True)
class RecoveryResult:
    decision: ResumeDecision
    tunnel: TunnelReady | TunnelFailure


async def recover_connection(
    provider: TunnelProvider,
    local_url: str,
    before: ResumeIdentity,
    read_identity: Callable[[], Awaitable[ResumeIdentity | None]],
    watchdog_expired: Callable[[], bool],
    *,
    max_retries: int,
    backoff: float,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> RecoveryResult:
    if type(max_retries) is not int or max_retries < 0 or backoff < 0:
        raise ValueError("invalid recovery limits")
    last = TunnelFailure(FailureKind.DISCONNECTED, "paused")
    for attempt in range(max_retries + 1):
        if watchdog_expired():
            return RecoveryResult(
                ResumeDecision.ABORT,
                TunnelFailure(FailureKind.TIMEOUT, "watchdog"),
            )
        await provider.stop()
        current = await provider.start(local_url)
        if isinstance(current, TunnelReady):
            decision = decide_resume(before, await read_identity())
            if decision is not ResumeDecision.RESUME:
                await provider.stop()
            return RecoveryResult(decision, current)
        last = current
        if attempt < max_retries:
            await sleep(backoff)
    return RecoveryResult(
        ResumeDecision.PAUSE,
        TunnelFailure(FailureKind.RETRIES_EXHAUSTED, f"last={last.kind}"),
    )
