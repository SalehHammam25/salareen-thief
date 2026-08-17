"""Typed private/environment configuration without secret display."""

from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class TunnelConfig:
    opponent_url: str | None = field(repr=False)
    response_timeout_sec: float = 30.0
    watchdog_timeout_sec: float = 60.0
    retry_backoff_sec: float = 5.0
    max_retries: int = 3
    provider_name: str | None = None
    credential: str | None = field(default=None, repr=False)


def _number(value: object, name: str, minimum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return float(value)


def load_tunnel_config(
    env: Mapping[str, str], shared: Mapping[str, object] | None = None
) -> TunnelConfig:
    shared = shared or {}
    network = shared.get("network_and_league", {})
    limiter = shared.get("rate_limiter_gatekeeper", {})
    if not isinstance(network, Mapping) or not isinstance(limiter, Mapping):
        raise ValueError("shared network sections must be objects")
    retries = limiter.get("max_retries", 3)
    if isinstance(retries, bool) or not isinstance(retries, int) or retries < 3:
        raise ValueError("max_retries must be an integer of at least 3")
    return TunnelConfig(
        env.get("SALAREEN_OPPONENT_URL"),
        _number(network.get("response_timeout_sec", 30), "response_timeout_sec", 0.001),
        _number(network.get("watchdog_timeout_sec", 60), "watchdog_timeout_sec", 0.001),
        _number(limiter.get("retry_backoff_sec", 5), "retry_backoff_sec", 5),
        retries,
        env.get("SALAREEN_TUNNEL_PROVIDER"),
        env.get("SALAREEN_TUNNEL_TOKEN"),
    )
