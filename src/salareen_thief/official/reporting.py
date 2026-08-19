"""Full counted-result generation, separate from official_reference_v1 settlement."""

import json
import re
from pathlib import Path

from .report_identity import group_block, opponent_identity
from .report_validation import validate_counted_result
from .settlement import aggregate, consensus_row
from .terms import GROUP_ID

SCHEMA_VERSION = "1.1"
ZEROED_RESULTS = {"timeout", "technical_loss", "tamper_forfeit"}
SAFE_GAME_ID = re.compile(r"^[A-Za-z0-9._-]+$")


def _links(game_id: str, own: dict, peer: dict) -> dict:
    return {
        "config": f"config_{game_id}_g<NN>.json",
        "declaration": f"declaration_{game_id}.json",
        "log": f"log_{game_id}_g<NN>.json",
        "result": f"result_{game_id}.json",
        "github": {own["group_id"]: own["repos"], peer["group_id"]: peer["repos"]},
    }


def _audit(summary: dict) -> dict:
    source = summary.get("audit", {})
    return {
        "log_verified": bool(source.get("log_verified")),
        "tampered": bool(source.get("tampered")),
        "local_result_claim": source.get("local_result_claim", summary.get("result")),
        "peer_result_claim": source.get("peer_result_claim"),
        "result_agreed": bool(source.get("result_agreed")),
    }


def _row(summary: dict, ours: str, theirs: str, game_id: str) -> dict:
    base = consensus_row(summary, ours, theirs)
    scores = base["score"]
    tokens = summary.get("tokens")
    if not isinstance(tokens, dict):
        tokens = {
            ours: int(summary.get("tokens_total", 0) or 0),
            theirs: int(summary.get("peer_tokens_total", 0) or 0),
        }
    log_name = f"log_{game_id}_g{summary['sub_game_number']:02d}.json"
    return {
        **base,
        "started_at": summary.get("started_at", ""),
        "ended_at": summary.get("ended_at", ""),
        "steps": int(summary.get("steps", 0)),
        "tie": summary["result"] not in ZEROED_RESULTS
        and len(set(scores.values())) == 1,
        "tokens": {ours: int(tokens.get(ours, 0)), theirs: int(tokens.get(theirs, 0))},
        "github_commit": {
            ours: summary.get("own_github_commit", ""),
            theirs: summary.get("peer_github_commit", ""),
        },
        "log_files": {ours: log_name, theirs: log_name},
        "audit": _audit(summary),
    }


def build_counted_result(series, opponent_url: str) -> dict:
    """Build rich reporting metadata without feeding it into the consensus digest."""
    ours = GROUP_ID
    theirs = series.peer_identity.get("group_id", "amireman")
    own = dict(series.own_identity)
    peer = opponent_identity(series.peer_identity, theirs, opponent_url)
    rows = [_row(summary, ours, theirs, series.game_id) for summary in series.summaries]
    final = aggregate(rows)
    final["tokens_total_series"] = {
        group: sum(row["tokens"][group] for row in rows) for group in (ours, theirs)
    }
    clean = bool(rows) and all(
        row["audit"]["log_verified"]
        and not row["audit"]["tampered"]
        and row["audit"]["result_agreed"]
        for row in rows
    )
    first_commits = rows[0]["github_commit"] if rows else {ours: "", theirs: ""}
    doc = {
        "schema_version": SCHEMA_VERSION,
        "report_type": "final_game_result",
        "game_id": series.game_id,
        "game_uid": series.game_uid,
        "game_started_at": series.game_started_at,
        "game_ended_at": series.game_ended_at,
        "timezone": "UTC",
        "groups": [ours, theirs],
        "group_details": {
            "group_1": group_block(own, first_commits[ours]),
            "group_2": group_block(peer, first_commits[theirs]),
        },
        "links": _links(series.game_id, own, peer),
        "num_sub_games": len(rows),
        "sub_games": rows,
        "final_result": final,
        "mutual_agreement": {
            "confirmed": clean and bool(series.consensus_agreed),
            "results_agreed": all(row["audit"]["result_agreed"] for row in rows),
            "sha256": series.consensus_sha,
            "peer_sha256": series.peer_consensus_sha,
            "sha_match": series.peer_consensus_sha == series.consensus_sha,
        },
    }
    return validate_counted_result(doc)


def write_counted_result(directory: Path, series, opponent_url: str) -> Path:
    """Write one new result_<game_id>.json and never overwrite an earlier artifact."""
    if SAFE_GAME_ID.fullmatch(series.game_id) is None:
        raise ValueError("unsafe game_id for counted result filename")
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"result_{series.game_id}.json"
    if path.exists():
        raise FileExistsError(f"refusing to overwrite counted result: {path}")
    doc = build_counted_result(series, opponent_url)
    path.write_text(
        json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path
