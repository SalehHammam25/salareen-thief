import pytest

from salareen_thief.security.protocol import AppendOnlyAuditLog, SecurityViolation
from salareen_thief.security.series import (
    SixGameSeries,
    privacy_safe_view,
    verified_replay,
)


def _series():
    series = SixGameSeries("series-1")
    for index in range(1, 7):
        series.add(
            {
                "game_id": f"g{index}",
                "index": index,
                "outcome": "survival",
                "cop_score": 0,
                "thief_score": 1,
                "audit_root": "a" * 64,
                "private_nonce": "forbidden",
            }
        )
    return series


def test_six_games_peer_agreement_and_privacy():
    series = _series()
    artifact = series.artifact()
    series.agree(artifact)
    assert "private_nonce" not in repr(artifact)
    with pytest.raises(SecurityViolation):
        series.agree({**artifact, "series_id": "tampered"})
    view = privacy_safe_view(
        "cop",
        [1, 2],
        [{"event": "turn", "index": 1, "thief_position": [4, 4]}],
        [[0.25, 0.75]],
        "YOUR TURN",
    )
    assert set(view) == {
        "role",
        "local_position",
        "belief_heatmap",
        "turn_status",
        "public_events",
    }
    assert "thief_position" not in repr(view)


def test_verified_replay_rejects_mutation():
    log = AppendOnlyAuditLog()
    log.append("terminal", {"outcome": "survival"})
    assert verified_replay(log.entries) == log.entries[-1]["entry_hash"]
    log.entries[0]["payload"]["outcome"] = "capture"
    with pytest.raises(SecurityViolation):
        verified_replay(log.entries)
