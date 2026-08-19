"""The exact closed agreement and byte-level reference constructions."""

import hashlib
import json
import secrets
import uuid
from typing import Any

GROUP_ID = "salareen"
GROUP_NAME = "Salareen"
MEMBERS = ["Areen Tarabeh", "Saleh Hammam"]
TERM_KEYS = (
    "board_size",
    "smell_grid_size",
    "decay_per_step",
    "emit_intensity",
    "min_center_intensity",
    "max_steps",
    "barriers_max",
    "setting",
    "hint_max_words",
    "axis_origin_corner",
    "axis_start_index",
    "thief_start",
    "cop_start",
    "num_games",
)
TERMS: dict[str, Any] = {
    "board_size": 7,
    "smell_grid_size": 5,
    "decay_per_step": 0.1,
    "emit_intensity": 0.9,
    "min_center_intensity": 0.5,
    "max_steps": 35,
    "barriers_max": 14,
    "setting": "Haifa",
    "hint_max_words": 15,
    "axis_origin_corner": "top-left",
    "axis_start_index": 0,
    "thief_start": [3, 3],
    "cop_start": [0, 0],
    "num_games": 6,
}


def canonical(value: Any, *, spaced: bool = False) -> str:
    kwargs = {"sort_keys": True, "ensure_ascii": False}
    if not spaced:
        kwargs["separators"] = (",", ":")
    return json.dumps(value, **kwargs)


def terms_sha256(terms: dict[str, Any] = TERMS) -> str:
    return hashlib.sha256(canonical(terms).encode("utf-8")).hexdigest()


def commit_of(payload: dict[str, Any], nonce: str) -> str:
    material = f"{canonical(payload)}|{nonce}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def derive_game_ids(
    group_a: str, group_b: str, terms: dict[str, Any] = TERMS
) -> tuple[str, str]:
    pair = sorted([group_a, group_b])
    seed = f"{canonical(terms)}|{'|'.join(pair)}"
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return "-vs-".join(pair), str(uuid.UUID(bytes=digest[:16]))


def greeting(
    role: str,
    sub_game: int,
    git_commit: str,
    opponent: str,
    identity: dict | None = None,
) -> dict:
    nonce = secrets.token_hex(16)
    _, game_uid = derive_game_ids(GROUP_ID, opponent)
    declared = dict(identity or {})
    declared.update(
        {
            "group_id": GROUP_ID,
            "group_name": GROUP_NAME,
            "members": list(MEMBERS),
            "github_commit": git_commit,
            "git_commit_hash": git_commit,
        }
    )
    return {
        "terms": dict(TERMS),
        "nonce": nonce,
        "signature": commit_of(TERMS, nonce),
        "group_id": GROUP_ID,
        "role": role,
        "sub_game_number": sub_game,
        "identity": declared,
        "game_uid": game_uid,
    }
