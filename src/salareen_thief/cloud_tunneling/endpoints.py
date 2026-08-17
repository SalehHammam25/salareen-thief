"""Remote endpoint validation and credential-safe display."""

import ipaddress
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .models import FailureKind, TunnelEndpoint, TunnelFailure

SECRET_KEYS = {"access_token", "api_key", "key", "secret", "token"}
LOCAL_HOSTS = {"localhost", "localhost.localdomain"}


def validate_remote_endpoint(value: str) -> TunnelEndpoint | TunnelFailure:
    if not isinstance(value, str) or not value:
        return TunnelFailure(FailureKind.CONFIGURATION, "endpoint is required")
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return TunnelFailure(FailureKind.CONFIGURATION, "invalid endpoint")
    if parsed.scheme != "https" or not parsed.hostname or parsed.username:
        return TunnelFailure(FailureKind.CONFIGURATION, "https endpoint required")
    if parsed.password or parsed.query or parsed.fragment or port == 0:
        return TunnelFailure(FailureKind.CONFIGURATION, "unsafe endpoint components")
    host = parsed.hostname.casefold()
    if host in LOCAL_HOSTS or host.endswith(".localhost") or _is_private_ip(host):
        return TunnelFailure(FailureKind.CONFIGURATION, "public host required")
    return TunnelEndpoint(value)


def _is_private_ip(host: str) -> bool:
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return not address.is_global


def redact_endpoint(value: str) -> str:
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return "<invalid-endpoint>"
    host = parsed.hostname or "<invalid-host>"
    netloc = host + (f":{port}" if port else "")
    query = urlencode(
        [
            (key, "REDACTED" if key.casefold() in SECRET_KEYS else item)
            for key, item in parse_qsl(parsed.query, keep_blank_values=True)
        ]
    )
    return urlunsplit((parsed.scheme, netloc, parsed.path, query, ""))
