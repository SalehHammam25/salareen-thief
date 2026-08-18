"""Stable classification without claiming unverifiable outage attribution."""

import ssl
from socket import gaierror

from .models import FailureKind, TunnelFailure


def classify_failure(error: BaseException) -> TunnelFailure:
    if isinstance(error, TimeoutError):
        return TunnelFailure(FailureKind.TIMEOUT, type(error).__name__)
    if isinstance(error, gaierror):
        return TunnelFailure(FailureKind.DNS, type(error).__name__)
    if isinstance(error, ssl.SSLError):
        return TunnelFailure(FailureKind.TLS, type(error).__name__)
    if isinstance(error, (ConnectionError, EOFError)):
        return TunnelFailure(FailureKind.DISCONNECTED, type(error).__name__)
    return TunnelFailure(FailureKind.ATTRIBUTION_UNKNOWN, type(error).__name__)
