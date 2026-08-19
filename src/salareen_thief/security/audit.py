"""Capture evidence and append-only audit chain."""

from __future__ import annotations

import hashlib
import hmac
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


def verify_capture_claim(claim: Mapping[str, Any]) -> None:
    from .protocol import SecurityViolation

    required = {"game_id", "turn", "claimant_role", "kind", "cop", "thief", "barriers"}
    if set(claim) != required or claim["claimant_role"] not in {"cop", "thief"}:
        raise SecurityViolation("invalid capture claim envelope")
    cop, thief = tuple(claim["cop"]), tuple(claim["thief"])
    barriers = {tuple(cell) for cell in claim["barriers"]}
    neighbors = {
        (thief[0] + dx, thief[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
    }
    valid = {
        "overlap": cop == thief,
        "barrier": thief in barriers,
        "trapped": neighbors <= (barriers | {cop}),
    }
    if not valid.get(claim["kind"], False):
        raise SecurityViolation("false capture claim: technical loss")


@dataclass
class AppendOnlyAuditLog:
    entries: list[dict[str, Any]] = field(default_factory=list)

    def append(self, event: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        from .protocol import canonical_bytes

        previous = self.entries[-1]["entry_hash"] if self.entries else "0" * 64
        core = {
            "index": len(self.entries),
            "event": event,
            "payload": dict(payload),
            "previous_hash": previous,
        }
        entry = {
            **core,
            "entry_hash": hashlib.sha256(canonical_bytes(core)).hexdigest(),
        }
        self.entries.append(entry)
        return dict(entry)

    def verify(self) -> None:
        from .protocol import SecurityViolation, canonical_bytes

        previous = "0" * 64
        for index, entry in enumerate(self.entries):
            core = {
                key: entry[key]
                for key in ("index", "event", "payload", "previous_hash")
            }
            expected = hashlib.sha256(canonical_bytes(core)).hexdigest()
            valid = entry["index"] == index and entry["previous_hash"] == previous
            if not valid or not hmac.compare_digest(entry["entry_hash"], expected):
                raise SecurityViolation("audit log tamper or reorder detected")
            previous = entry["entry_hash"]
