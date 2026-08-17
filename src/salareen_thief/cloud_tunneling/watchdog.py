"""Deterministic watchdog evaluation without owning game outcomes."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WatchdogStatus:
    expired: bool
    elapsed: float


def evaluate_watchdog(last_heartbeat: float, now: float, timeout: float) -> WatchdogStatus:
    values = (last_heartbeat, now, timeout)
    if any(type(value) not in {int, float} for value in values):
        raise TypeError("watchdog values must be exact numbers")
    if timeout <= 0 or now < last_heartbeat:
        raise ValueError("invalid watchdog timeline")
    elapsed = now - last_heartbeat
    return WatchdogStatus(elapsed > timeout, elapsed)
