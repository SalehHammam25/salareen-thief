"""Stage 2 shared/private network configuration boundary."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from salareen_thief.base_logic.config_decode import decode_json


@dataclass(frozen=True, slots=True)
class NetworkConfig:
    my_port: int
    opponent_url: str
    response_timeout_sec: int
    watchdog_timeout_sec: int
    retry_backoff_sec: int
    max_retries: int


def _exact_positive_int(value: object, name: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def load_network_config(shared_path: Path, private_path: Path) -> NetworkConfig:
    shared = decode_json(shared_path.read_text(encoding="utf-8"))
    private = tomllib.loads(private_path.read_text(encoding="utf-8"))
    if type(shared) is not dict or type(private) is not dict:
        raise ValueError("configuration roots must be objects")
    shared_network = shared.get("network_and_league")
    shared_limits = shared.get("rate_limiter_gatekeeper")
    private_network = private.get("network")
    if (
        type(shared_network) is not dict
        or type(shared_limits) is not dict
        or type(private_network) is not dict
    ):
        raise ValueError("network sections are required")
    port = _exact_positive_int(private_network.get("my_port"), "my_port")
    url = private_network.get("opponent_url")
    if type(url) is not str or not url.startswith(("http://", "https://")):
        raise ValueError("opponent_url must be HTTP(S)")
    response = _exact_positive_int(
        shared_network.get("response_timeout_sec"), "response_timeout_sec"
    )
    watchdog = _exact_positive_int(
        shared_network.get("watchdog_timeout_sec"), "watchdog_timeout_sec"
    )
    backoff = _exact_positive_int(
        shared_limits.get("retry_backoff_sec"), "retry_backoff_sec"
    )
    retries = _exact_positive_int(shared_limits.get("max_retries"), "max_retries")
    return NetworkConfig(port, url, response, watchdog, backoff, retries)
