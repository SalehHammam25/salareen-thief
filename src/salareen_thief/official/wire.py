"""Strict official turn, agreement, and audit validation."""

import json
import math
import re
from typing import Any

from .terms import GROUP_ID, TERMS, commit_of, derive_game_ids

MAX_MESSAGE_BYTES = 262_144
HEX32 = re.compile(r"^[0-9a-f]{32}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _sized(value: Any) -> bool:
    try:
        return len(json.dumps(value, ensure_ascii=False).encode("utf-8")) <= MAX_MESSAGE_BYTES
    except (TypeError, ValueError):
        return False


def cell(value: Any, board_size: int = 7) -> list[int] | None:
    if type(value) is not list or len(value) != 2:
        return None
    if not all(type(part) is int and 0 <= part < board_size for part in value):
        return None
    return list(value)


def clean_scent(value: Any, board_size: int = 7) -> dict[str, float]:
    if not isinstance(value, dict) or len(value) > board_size * board_size:
        return {}
    result: dict[str, float] = {}
    for key, intensity in value.items():
        if not isinstance(key, str) or not isinstance(intensity, (int, float)):
            continue
        if isinstance(intensity, bool) or not math.isfinite(float(intensity)):
            continue
        try:
            row, col = (int(part) for part in key.split(","))
        except (ValueError, TypeError):
            continue
        if key != f"{row},{col}" or not (0 <= row < board_size and 0 <= col < board_size):
            continue
        if 0.0 <= float(intensity) <= 1.0:
            result[key] = float(intensity)
    return result


def clean_turn(value: Any, board_size: int = 7) -> dict | None:
    if type(value) is not dict or not _sized(value):
        return None
    step, sender, digest = value.get("step"), value.get("sender"), value.get("commit")
    if type(step) is not int or step < 0:
        return None
    if not isinstance(sender, str) or not sender or not isinstance(digest, str):
        return None
    if HEX64.fullmatch(digest) is None:
        return None
    response = value.get("claim_response")
    if not isinstance(response, dict) or type(response.get("caught")) is not bool:
        response = None
    else:
        claim = cell(response.get("claim"), board_size)
        response = None if claim is None else {"claim": claim, "caught": response["caught"]}
    win = value.get("win_claim")
    win = win if isinstance(win, dict) and isinstance(win.get("type"), str) else None
    return {
        "step": step,
        "sender": sender,
        "commit": digest,
        "hint": value.get("hint") if isinstance(value.get("hint"), str) else "",
        "smell_grid": clean_scent(value.get("smell_grid"), board_size),
        "timestamp": value.get("timestamp") if isinstance(value.get("timestamp"), str) else "",
        "barrier_placed": cell(value.get("barrier_placed"), board_size),
        "capture_claim": cell(value.get("capture_claim"), board_size),
        "claim_response": response,
        "win_claim": win,
    }


def verify_greeting(value: Any, expected_role: str, sub_game: int) -> str:
    if type(value) is not dict or value.get("terms") != TERMS:
        raise ValueError("agreement terms differ")
    nonce, signature = value.get("nonce"), value.get("signature")
    if not isinstance(nonce, str) or HEX32.fullmatch(nonce) is None:
        raise ValueError("invalid agreement nonce")
    if not isinstance(signature, str) or signature != commit_of(TERMS, nonce):
        raise ValueError("invalid agreement signature")
    identity = value.get("identity") if isinstance(value.get("identity"), dict) else {}
    group = value.get("group_id") or identity.get("group_id")
    if not isinstance(group, str) or not group or group == GROUP_ID:
        raise ValueError("invalid peer group")
    if value.get("role") != expected_role or value.get("sub_game_number") != sub_game:
        raise ValueError("wrong peer role or sub-game")
    _, expected_uid = derive_game_ids(GROUP_ID, group)
    if value.get("game_uid") not in (None, expected_uid):
        raise ValueError("wrong game_uid")
    return group


def clean_audit(value: Any, max_records: int = 72) -> dict | None:
    if type(value) is not dict or not _sized(value):
        return None
    records = value.get("records")
    if not isinstance(records, list) or len(records) > max_records:
        return None
    sender, claim = value.get("sender"), value.get("result_claim")
    if not isinstance(sender, str) or not sender or not isinstance(claim, str):
        return None
    digest = value.get("consensus_sha")
    if digest is not None and (not isinstance(digest, str) or HEX64.fullmatch(digest) is None):
        return None
    result = {"sender": sender, "records": [r for r in records if isinstance(r, dict)], "result_claim": claim}
    if digest is not None:
        result["consensus_sha"] = digest
    for key in ("sub_game", "sub_game_number"):
        if type(value.get(key)) is int:
            result[key] = value[key]
    return result
