"""Canonical Ed25519 security primitives for peer-local matches."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from .audit import AppendOnlyAuditLog, verify_capture_claim
from .step0 import validate_step0

__all__ = ["AppendOnlyAuditLog", "validate_step0", "verify_capture_claim"]


class SecurityViolation(ValueError):
    """A fail-closed protocol or audit violation."""


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SecurityViolation(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def canonical_bytes(value: Any) -> bytes:
    """RFC-8259-compatible deterministic UTF-8 JSON profile."""
    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise SecurityViolation("value is not canonical JSON") from exc
    return text.encode("utf-8")


def parse_canonical(data: bytes) -> Any:
    try:
        value = json.loads(data, object_pairs_hook=_no_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SecurityViolation("invalid JSON") from exc
    if canonical_bytes(value) != data:
        raise SecurityViolation("noncanonical JSON bytes")
    return value


def require_identical_config(local: bytes, peer: bytes) -> Mapping[str, Any]:
    if not hmac.compare_digest(local, peer):
        raise SecurityViolation("shared configuration byte mismatch")
    value = parse_canonical(local)
    if not isinstance(value, dict):
        raise SecurityViolation("shared configuration must be an object")
    return value


def sign(private_key: Ed25519PrivateKey, value: Any) -> str:
    return base64.b64encode(private_key.sign(canonical_bytes(value))).decode("ascii")


def verify(public_key: Ed25519PublicKey, value: Any, signature: str) -> None:
    try:
        raw = base64.b64decode(signature, validate=True)
        public_key.verify(raw, canonical_bytes(value))
    except (ValueError, InvalidSignature) as exc:
        raise SecurityViolation("invalid Ed25519 signature") from exc


def fresh_nonce(size: int = 32) -> bytes:
    if size < 16:
        raise SecurityViolation("nonce must contain at least 128 bits")
    return secrets.token_bytes(size)


def commitment(payload: Mapping[str, Any], nonce: bytes) -> str:
    if len(nonce) < 16:
        raise SecurityViolation("missing or short nonce")
    framed = b"salareen-stage6-v1\x00" + canonical_bytes(payload) + b"\x00" + nonce
    return hashlib.sha256(framed).hexdigest()


@dataclass
class CommitReveal:
    seen_digests: set[str] = field(default_factory=set)
    phase: str = "new"
    digest: str | None = None
    payload: Mapping[str, Any] | None = None

    def commit(self, digest: str) -> None:
        if self.phase != "new" or len(digest) != 64 or digest in self.seen_digests:
            raise SecurityViolation("invalid or reused commitment")
        try:
            int(digest, 16)
        except ValueError as exc:
            raise SecurityViolation("commitment must be hexadecimal") from exc
        self.seen_digests.add(digest)
        self.digest, self.phase = digest, "committed"

    def acknowledge(self) -> None:
        if self.phase != "committed":
            raise SecurityViolation("acknowledgement out of phase")
        self.phase = "acknowledged"

    def reveal(self, payload: Mapping[str, Any]) -> None:
        if self.phase != "acknowledged":
            raise SecurityViolation("reveal requires acknowledgement")
        self.payload, self.phase = dict(payload), "revealed"

    def audit(self, nonce: bytes) -> None:
        if self.phase != "revealed" or self.payload is None or self.digest is None:
            raise SecurityViolation("audit before completed reveal")
        if not hmac.compare_digest(commitment(self.payload, nonce), self.digest):
            raise SecurityViolation("commitment audit mismatch: technical loss")
        self.phase = "audited"
