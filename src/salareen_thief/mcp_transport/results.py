"""Transport result values."""

from dataclasses import dataclass
from enum import StrEnum

from .contracts import GeometryMessage


class TransportError(StrEnum):
    CONTRACT_REJECTED = "CONTRACT_REJECTED"
    DUPLICATE_MISMATCH = "DUPLICATE_MISMATCH"
    OUT_OF_PHASE = "OUT_OF_PHASE"
    EPISODE_TERMINAL = "EPISODE_TERMINAL"
    REMOTE_ERROR = "REMOTE_ERROR"
    TIMEOUT = "TIMEOUT"
    RETRIES_EXHAUSTED = "RETRIES_EXHAUSTED"
    WATCHDOG_EXPIRED = "WATCHDOG_EXPIRED"


@dataclass(frozen=True, slots=True)
class TransportAccepted:
    message: GeometryMessage

    def as_dict(self) -> dict[str, object]:
        return {"accepted": True, "message": self.message.as_dict()}


@dataclass(frozen=True, slots=True)
class TransportRejected:
    code: str
    detail: str

    def as_dict(self) -> dict[str, object]:
        return {"accepted": False, "code": self.code, "detail": self.detail}
