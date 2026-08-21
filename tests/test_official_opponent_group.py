"""Thief-side symmetry: no opponent group is baked into reporting or ids."""

import pytest

from salareen_thief.official.reporting import build_counted_result
from salareen_thief.official.terms import GROUP_ID, derive_game_ids
from tests.test_counted_reporting import PEER, _series

GROUPS = ["GRP00001", "amireman", "zeta.group-9", "a"]


@pytest.mark.parametrize("group", GROUPS)
def test_derived_ids_are_unique_per_opponent_group(group):
    game_id, game_uid = derive_game_ids(GROUP_ID, group)
    assert game_id == "-vs-".join(sorted([GROUP_ID, group]))
    others = {derive_game_ids(GROUP_ID, other)[1] for other in GROUPS if other != group}
    assert game_uid not in others


@pytest.mark.parametrize("group", GROUPS)
def test_counted_result_follows_the_declared_peer_group(group):
    series = _series()
    series.peer_identity = {**series.peer_identity, "group_id": group}
    series.game_id = f"NC-{group}"
    doc = build_counted_result(series, PEER)
    assert set(doc["groups"]) == {GROUP_ID, group}
    assert doc["group_details"]["group_2"]["group_id"] == group
    for row in doc["sub_games"]:
        assert set(row["score"]) == {GROUP_ID, group}


@pytest.mark.parametrize("missing", [None, "", GROUP_ID])
def test_counted_result_refuses_a_missing_or_self_peer_group(missing):
    series = _series()
    peer = dict(series.peer_identity)
    if missing is None:
        peer.pop("group_id", None)
    else:
        peer["group_id"] = missing
    series.peer_identity = peer
    with pytest.raises(ValueError, match="distinct peer group_id"):
        build_counted_result(series, PEER)
