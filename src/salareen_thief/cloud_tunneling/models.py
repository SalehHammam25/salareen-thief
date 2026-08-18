"""Immutable tunnel lifecycle values and typed outcomes."""

from dataclasses import dataclass, field
from enum import StrEnum


class FailureKind(StrEnum):
    CONFIGURATION = "configuration"
    START_FAILED = "start_failed"
    NOT_READY = "not_ready"
    DNS = "dns"
    TLS = "tls"
    DISCONNECTED = "disconnected"
    TIMEOUT = "timeout"
    EXPIRED_ENDPOINT = "expired_endpoint"
    RETRIES_EXHAUSTED = "retries_exhausted"
    PROCESS_EXITED = "process_exited"
    ATTRIBUTION_UNKNOWN = "attribution_unknown"


@dataclass(frozen=True, slots=True)
class TunnelEndpoint:
    url: str = field(repr=False)


@dataclass(frozen=True, slots=True)
class TunnelReady:
    endpoint: TunnelEndpoint


@dataclass(frozen=True, slots=True)
class TunnelFailure:
    kind: FailureKind
    detail: str = ""


TunnelResult = TunnelReady | TunnelFailure
