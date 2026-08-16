"""JSON decoding with duplicate-key rejection."""

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class DuplicateKeyError(ValueError):
    key: str


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def decode_json(text: str) -> Any:
    """Decode JSON while rejecting the first deterministic duplicate key."""
    return json.loads(text, object_pairs_hook=_unique_object)
