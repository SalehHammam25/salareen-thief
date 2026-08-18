"""Bounded recovery policy for a paused live peer."""

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import Any

from .session import LiveMatchSession


def event(session: LiveMatchSession, kind: str, correlation: str | None = None,
          data: dict[str, Any] | None = None) -> None:
    events = getattr(session, "events", None)
    if events:
        events.emit(kind, turn=session.turn_index, phase=session.phase,
                    correlation_id=correlation, data=data)


def abort(session: LiveMatchSession, kind: str, correlation: str | None) -> None:
    session.phase = "aborted"
    session._save("phase", session.phase)
    event(session, kind, correlation, {"attribution": "unknown"})


async def bounded_call(session: LiveMatchSession, correlation: str,
                       operation: Callable[[], Awaitable[dict[str, Any]]],
                       *, pause: bool = True) -> dict[str, Any]:
    started = time.monotonic()
    for attempt in range(session.max_retries + 1):
        try:
            response = await asyncio.wait_for(
                operation(), getattr(session, "response_timeout", 30))
            if not response["accepted"]:
                abort(session, "recovery_rejected", correlation)
                return response
            return response
        except Exception as error:
            if session.phase == "aborted":
                raise RuntimeError("match aborted during recovery") from error
            if pause and session.phase != "paused_recovering":
                session.phase = "paused_recovering"
                session._save("phase", session.phase)
                event(session, "paused", correlation)
            elapsed = time.monotonic() - started
            if elapsed >= session.watchdog_timeout:
                abort(session, "watchdog_expired", correlation)
                raise RuntimeError("recovery watchdog expired") from error
            if attempt == session.max_retries:
                abort(session, "recovery_exhausted", correlation)
                raise RuntimeError("peer recovery exhausted") from error
            event(session, "reconnect_attempted", correlation,
                  {"attempt": attempt + 1})
            await asyncio.sleep(session.retry_backoff)
    raise AssertionError("unreachable")
