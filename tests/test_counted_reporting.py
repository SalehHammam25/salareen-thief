from types import SimpleNamespace

import pytest

from salareen_thief.official.report_identity import (
    AMIREMAN_REPOS,
    SALAREEN_REPOS,
    salareen_identity,
)
from salareen_thief.official.reporting import build_counted_result, write_counted_result
from salareen_thief.official.settlement import consensus_row, consensus_sha

POLICE_SHA = "1" * 40
THIEF_SHA = "2" * 40
PEER_POLICE_SHA = "3" * 40
PEER_THIEF_SHA = "4" * 40
CONSENSUS = "a" * 64
PUBLIC = "https://salareen.example/mcp"
PEER = "https://amireman.example/mcp"


def _series():
    summaries = []
    for number in range(1, 7):
        role = "police" if number % 2 else "thief"
        summaries.append(
            {
                "sub_game_number": number,
                "role": role,
                "result": "survival",
                "started_at": f"2026-09-01T10:0{number}:00+00:00",
                "ended_at": f"2026-09-01T10:0{number}:30+00:00",
                "steps": 35,
                "tokens_total": 0,
                "peer_tokens_total": 0,
                "own_github_commit": POLICE_SHA if role == "police" else THIEF_SHA,
                "peer_github_commit": PEER_THIEF_SHA
                if role == "police"
                else PEER_POLICE_SHA,
                "audit": {
                    "log_verified": True,
                    "tampered": False,
                    "local_result_claim": "survival",
                    "peer_result_claim": "survival",
                    "result_agreed": True,
                },
            }
        )
    own = salareen_identity(
        {"police": POLICE_SHA, "thief": THIEF_SHA}, PUBLIC, "Codex GPT-5"
    )
    peer = {
        "group_id": "amireman",
        "group_name": "amireman",
        "members": ["Amir Fadila", "Eman Sarhan"],
        "repos": AMIREMAN_REPOS,
        "mcp_servers": {"cop": PEER, "thief": PEER},
        "llm_model": "peer-model",
        "hardware_spec": {"cpu_cores": 4},
    }
    return SimpleNamespace(
        game_id="amireman-vs-salareen",
        game_uid="dc96f6d1-fc31-e0d9-3be2-05ddef48ed73",
        game_started_at="2026-09-01T10:01:00+00:00",
        game_ended_at="2026-09-01T10:06:30+00:00",
        own_identity=own,
        peer_identity=peer,
        summaries=summaries,
        consensus_sha=CONSENSUS,
        peer_consensus_sha=CONSENSUS,
        consensus_agreed=True,
    )


def test_full_counted_result_shape_and_repository_links():
    doc = build_counted_result(_series(), PEER)
    assert doc["num_sub_games"] == 6 and len(doc["sub_games"]) == 6
    assert doc["report_type"] == "final_game_result"
    assert doc["links"]["github"] == {
        "salareen": SALAREEN_REPOS,
        "amireman": AMIREMAN_REPOS,
    }
    assert set(doc["group_details"]) == {"group_1", "group_2"}
    assert doc["game_started_at"] and doc["game_ended_at"] and doc["timezone"] == "UTC"


def test_per_role_commits_and_group_keyed_rows_are_exact():
    rows = build_counted_result(_series(), PEER)["sub_games"]
    assert [row["github_commit"]["salareen"] for row in rows] == [
        POLICE_SHA,
        THIEF_SHA,
        POLICE_SHA,
        THIEF_SHA,
        POLICE_SHA,
        THIEF_SHA,
    ]
    assert [row["github_commit"]["amireman"] for row in rows] == [
        PEER_THIEF_SHA,
        PEER_POLICE_SHA,
        PEER_THIEF_SHA,
        PEER_POLICE_SHA,
        PEER_THIEF_SHA,
        PEER_POLICE_SHA,
    ]
    for row in rows:
        assert set(row["roles"]) == {"salareen", "amireman"}
        assert set(row["score"]) == {"salareen", "amireman"}
        assert row["audit"] == {
            "log_verified": True,
            "tampered": False,
            "local_result_claim": "survival",
            "peer_result_claim": "survival",
            "result_agreed": True,
        }


def test_final_result_mutual_agreement_and_digest_isolation():
    series = _series()
    canonical = [consensus_row(row, "salareen", "amireman") for row in series.summaries]
    before = consensus_sha(series.game_id, canonical)
    doc = build_counted_result(series, PEER)
    assert doc["final_result"] == {
        "total_score": {"amireman": 47, "salareen": 47},
        "sub_games_won": {"amireman": 3, "salareen": 3},
        "ties": 0,
        "winner_group": None,
        "series_tie": True,
        "tokens_total_series": {"salareen": 0, "amireman": 0},
    }
    assert doc["mutual_agreement"] == {
        "confirmed": True,
        "results_agreed": True,
        "sha256": CONSENSUS,
        "peer_sha256": CONSENSUS,
        "sha_match": True,
    }
    doc["links"]["config"] = "changed-reporting-only"
    assert consensus_sha(series.game_id, canonical) == before


def test_writer_uses_required_name_and_never_overwrites(tmp_path):
    path = write_counted_result(tmp_path, _series(), PEER)
    assert path.name == "result_amireman-vs-salareen.json"
    with pytest.raises(FileExistsError):
        write_counted_result(tmp_path, _series(), PEER)
