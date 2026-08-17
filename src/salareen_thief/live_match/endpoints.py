"""Strict and identical local/remote live-match endpoint policy."""

import ipaddress
from urllib.parse import urlsplit


def validate_endpoint(value: str, *, mode: str, host: str,
                      permitted_port: int | None = None) -> str:
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except (TypeError, ValueError) as error:
        raise ValueError("invalid endpoint") from error
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("unsafe endpoint components")
    if parsed.path != "/mcp" or parsed.hostname != host or port != permitted_port:
        raise ValueError("endpoint does not match configured authority")
    local = _local(parsed.hostname)
    if mode == "remote" and (parsed.scheme != "https" or local):
        raise ValueError("remote endpoint must be public HTTPS")
    if mode == "local" and (parsed.scheme != "http" or not local):
        raise ValueError("local endpoint must be loopback HTTP")
    if mode not in {"local", "remote"}:
        raise ValueError("invalid endpoint mode")
    return value


def _local(host: str | None) -> bool:
    if host in {"localhost", "localhost.localdomain"}:
        return True
    try:
        return not ipaddress.ip_address(host or "").is_global
    except ValueError:
        return bool(host and host.endswith(".localhost"))
