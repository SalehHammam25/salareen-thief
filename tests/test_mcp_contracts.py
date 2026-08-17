"""Stage 2 transport contract tests."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from salareen_thief.mcp_transport.contracts import (
    PROTOCOL_VERSION,
    ContractError,
    ContractRejected,
    GeometryMessage,
    decode_geometry,
)


def valid_payload() -> dict[str, object]:
    return {
        "protocol_version": PROTOCOL_VERSION,
        "correlation_id": "game1-step0",
        "sender_role": "cop",
        "x": 2,
        "y": 4,
        "step": 0,
    }


def test_valid_message_round_trips() -> None:
    decoded = decode_geometry(valid_payload())
    assert isinstance(decoded, GeometryMessage)
    assert decoded.as_dict() == valid_payload()
    assert hash(decoded) == hash(decode_geometry(valid_payload()))


def test_canonical_cross_repository_fixture_decodes() -> None:
    fixture = Path("tests/fixtures/mcp-geometry-v1-provisional.json")
    decoded = decode_geometry(json.loads(fixture.read_text(encoding="utf-8")))
    assert isinstance(decoded, GeometryMessage)
    assert decoded.correlation_id == "fixture-step-0"
    assert decoded.sender_role == "thief"


@pytest.mark.parametrize(
    ("change", "error"),
    [
        ({"extra": 1}, ContractError.UNKNOWN_FIELD),
        ({"protocol_version": "future"}, ContractError.UNSUPPORTED_VERSION),
        ({"correlation_id": "bad id"}, ContractError.INVALID_CORRELATION_ID),
        ({"sender_role": "server"}, ContractError.INVALID_ROLE),
        ({"x": True}, ContractError.WRONG_TYPE),
        ({"y": 1.5}, ContractError.WRONG_TYPE),
        ({"step": -1}, ContractError.INVALID_STEP),
        ({"step": False}, ContractError.INVALID_STEP),
    ],
)
def test_invalid_values_are_rejected(
    change: dict[str, object], error: ContractError
) -> None:
    payload = valid_payload() | change
    result = decode_geometry(payload)
    assert isinstance(result, ContractRejected)
    assert result.code is error


def test_missing_field_is_deterministic() -> None:
    payload = valid_payload()
    del payload["x"]
    del payload["y"]
    result = decode_geometry(payload)
    assert result == ContractRejected(ContractError.MISSING_FIELD, "x")


@pytest.mark.parametrize("value", [None, [], "payload", 4])
def test_non_object_payload_rejected(value: object) -> None:
    result = decode_geometry(value)
    assert isinstance(result, ContractRejected)
    assert result.code is ContractError.INVALID_SHAPE


def test_non_string_key_rejected_deterministically() -> None:
    result = decode_geometry(valid_payload() | {1: "unsafe"})
    assert result == ContractRejected(ContractError.INVALID_SHAPE, "keys must be strings")


def test_decode_is_repeatable_in_fresh_processes() -> None:
    script = (
        "import json; from salareen_thief.mcp_transport.contracts import "
        "decode_geometry; value=json.loads(input()); print(decode_geometry(value).as_dict())"
    )
    encoded = json.dumps(valid_payload())
    outputs = [
        subprocess.run(
            [sys.executable, "-c", script],
            input=encoded,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        for _ in range(2)
    ]
    assert outputs[0] == outputs[1]
