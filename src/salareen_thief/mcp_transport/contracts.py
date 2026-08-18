"""Owner-approved Stage 2 geometric transport contract."""

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

PROTOCOL_VERSION = "1.0-provisional"
TOOL_RECEIVE = "receive_geometry"
TOOL_RELAY = "relay_geometry"
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
_KEYS = {"protocol_version", "correlation_id", "sender_role", "x", "y", "step"}


class ContractError(StrEnum):
    INVALID_SHAPE = "INVALID_SHAPE"
    UNKNOWN_FIELD = "UNKNOWN_FIELD"
    MISSING_FIELD = "MISSING_FIELD"
    WRONG_TYPE = "WRONG_TYPE"
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    INVALID_CORRELATION_ID = "INVALID_CORRELATION_ID"
    INVALID_ROLE = "INVALID_ROLE"
    INVALID_STEP = "INVALID_STEP"


@dataclass(frozen=True, slots=True)
class GeometryMessage:
    protocol_version: str
    correlation_id: str
    sender_role: str
    x: int
    y: int
    step: int

    def as_dict(self) -> dict[str, str | int]:
        return {
            "protocol_version": self.protocol_version,
            "correlation_id": self.correlation_id,
            "sender_role": self.sender_role,
            "x": self.x,
            "y": self.y,
            "step": self.step,
        }


@dataclass(frozen=True, slots=True)
class ContractRejected:
    code: ContractError
    detail: str


def decode_geometry(value: Any) -> GeometryMessage | ContractRejected:
    if type(value) is not dict:
        return ContractRejected(
            ContractError.INVALID_SHAPE, "payload must be an object"
        )
    if any(type(key) is not str for key in value):
        return ContractRejected(ContractError.INVALID_SHAPE, "keys must be strings")
    keys = set(value)
    unknown = sorted(keys - _KEYS)
    if unknown:
        return ContractRejected(ContractError.UNKNOWN_FIELD, unknown[0])
    missing = sorted(_KEYS - keys)
    if missing:
        return ContractRejected(ContractError.MISSING_FIELD, missing[0])
    if type(value["protocol_version"]) is not str:
        return ContractRejected(ContractError.WRONG_TYPE, "protocol_version")
    if value["protocol_version"] != PROTOCOL_VERSION:
        return ContractRejected(ContractError.UNSUPPORTED_VERSION, "protocol_version")
    correlation = value["correlation_id"]
    if type(correlation) is not str or not _ID.fullmatch(correlation):
        return ContractRejected(ContractError.INVALID_CORRELATION_ID, "correlation_id")
    role = value["sender_role"]
    if type(role) is not str or role not in {"cop", "thief"}:
        return ContractRejected(ContractError.INVALID_ROLE, "sender_role")
    if type(value["x"]) is not int or type(value["y"]) is not int:
        return ContractRejected(ContractError.WRONG_TYPE, "coordinate")
    step = value["step"]
    if type(step) is not int or step < 0:
        return ContractRejected(ContractError.INVALID_STEP, "step")
    return GeometryMessage(
        PROTOCOL_VERSION, correlation, role, value["x"], value["y"], step
    )
