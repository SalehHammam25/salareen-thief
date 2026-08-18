"""Privacy-safe Stage 7 series artifacts and verified replay."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from .protocol import AppendOnlyAuditLog, SecurityViolation, canonical_bytes

PUBLIC_GAME_FIELDS = frozenset(
    {"game_id", "index", "outcome", "cop_score", "thief_score", "audit_root"}
)


def public_game_result(result: Mapping[str, Any]) -> dict[str, Any]:
    public = {key: result[key] for key in PUBLIC_GAME_FIELDS}
    if set(public) != PUBLIC_GAME_FIELDS:
        raise SecurityViolation("incomplete public result")
    return public


@dataclass
class SixGameSeries:
    series_id: str
    games: list[dict[str, Any]] = field(default_factory=list)

    def add(self, result: Mapping[str, Any]) -> None:
        if len(self.games) >= 6 or result.get("index") != len(self.games) + 1:
            raise SecurityViolation("series requires games 1 through 6 in order")
        self.games.append(public_game_result(result))

    def artifact(self) -> dict[str, Any]:
        if len(self.games) != 6:
            raise SecurityViolation("series is incomplete")
        return {
            "protocol_version": "1.0",
            "series_id": self.series_id,
            "games": self.games,
        }

    def agree(self, peer_artifact: Mapping[str, Any]) -> None:
        if canonical_bytes(self.artifact()) != canonical_bytes(peer_artifact):
            raise SecurityViolation("peer series result disagreement")


def verified_replay(entries: Sequence[Mapping[str, Any]]) -> str:
    log = AppendOnlyAuditLog(entries=[dict(entry) for entry in entries])
    log.verify()
    return log.entries[-1]["entry_hash"] if log.entries else "0" * 64


def privacy_safe_view(
    role: str,
    local_position: Sequence[int],
    public_events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    if role not in {"cop", "thief"}:
        raise SecurityViolation("invalid viewer role")
    return {
        "role": role,
        "local_position": list(local_position),
        "public_events": [dict(event) for event in public_events],
    }
