"""Per-game scoring, audit verification, and official_reference_v1 consensus."""

import hashlib
from typing import Any

from .terms import canonical, commit_of

SCORES = {
    "capture": {"police": 20, "thief": 5},
    "survival": {"police": 5, "thief": 10},
    "timeout": {"police": 0, "thief": 0},
    "technical_loss": {"police": 0, "thief": 0},
    "tamper_forfeit": {"police": 0, "thief": 0},
}
ROW_KEYS = ("sub_game_number", "result", "roles", "score", "winner_group")


def verify_records(records: list[dict], played: dict[int, str]) -> bool:
    revealed: dict[int, str] = {}
    for record in records:
        try:
            payload, nonce, digest = record["payload"], record["nonce"], record["commit"]
            step = payload["step"]
        except (KeyError, TypeError):
            return False
        if type(step) is not int or not isinstance(nonce, str) or not isinstance(digest, str):
            return False
        if commit_of(payload, nonce) != digest:
            return False
        revealed[step] = digest
    return all(revealed.get(step) == digest for step, digest in played.items())


def consensus_row(summary: dict, ours: str, theirs: str) -> dict:
    our_role = summary["role"]
    their_role = "thief" if our_role == "police" else "police"
    result = summary["result"]
    our_score = SCORES[result][our_role]
    their_score = SCORES[result][their_role]
    winner = ours if our_score > their_score else theirs if their_score > our_score else None
    return {
        "sub_game_number": summary["sub_game_number"],
        "result": result,
        "roles": {ours: our_role, theirs: their_role},
        "score": {ours: our_score, theirs: their_score},
        "winner_group": winner,
    }


def aggregate(rows: list[dict]) -> dict:
    groups = sorted({group for row in rows for group in row["score"]})
    total = {group: sum(row["score"].get(group, 0) for row in rows) for group in groups}
    won = dict.fromkeys(groups, 0)
    ties = 0
    for row in rows:
        top = max(row["score"].values())
        winners = [group for group, score in row["score"].items() if score == top]
        if len(winners) == 1:
            won[winners[0]] += 1
        else:
            ties += 1
    series_tie = len(groups) == 2 and total[groups[0]] == total[groups[1]]
    if series_tie:
        total = {group: score + 2 for group, score in total.items()}
    winner = None if series_tie or not total else max(total, key=total.get)
    return {
        "total_score": total,
        "sub_games_won": won,
        "ties": ties,
        "winner_group": winner,
        "series_tie": series_tie,
    }


def consensus_preimage(game_id: str, rows: list[dict]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda row: row["sub_game_number"])
    exact = [{key: row[key] for key in ROW_KEYS} for row in ordered]
    return {"game_id": game_id, "aggregate": aggregate(exact), "sub_games": exact}


def consensus_sha(game_id: str, rows: list[dict]) -> str:
    data = canonical(consensus_preimage(game_id, rows), spaced=True).encode("utf-8")
    return hashlib.sha256(data).hexdigest()
