import hashlib
import json

import pytest

from salareen_thief.official.delivery import DeliveryInbox, EquivocationError
from salareen_thief.official.engine import ThiefEngine
from salareen_thief.official.settlement import consensus_preimage, consensus_sha
from salareen_thief.official.terms import (
    TERMS,
    commit_of,
    derive_game_ids,
    terms_sha256,
)
from salareen_thief.official.wire import clean_turn

COMMIT = "2" * 40
VECTOR_PAYLOAD = {
    "hint": "",
    "intent": "probe east",
    "move": "MOVE:E",
    "position": [3, 4],
    "role": "thief",
    "state": "ok",
    "step": 1,
    "sub_game": 1,
}


def turn(**changes):
    value = {"step": 1, "sender": "police", "commit": "a" * 64, "hint": ""}
    value.update(changes)
    return value


def test_official_terms_vectors_and_ids():
    assert TERMS["setting"] == "Haifa" and len(TERMS) == 14
    assert terms_sha256() == "ad9e1bfd724e9debcde523833381cb7982a5d619d693d3738b59e0da61f4d81a"
    assert commit_of(VECTOR_PAYLOAD, "a" * 32) == (
        "4047830b8108320cbf48c1c1e1f09c6c0d47da51c225ce2cf40c7857cefc3030"
    )
    assert derive_game_ids("amireman", "salareen") == (
        "amireman-vs-salareen",
        "dc96f6d1-fc31-e0d9-3be2-05ddef48ed73",
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"step": 1.0},
        {"step": True},
        {"step": -1},
        {"sender": ""},
        {"commit": "A" * 64},
        {"commit": "a" * 63},
    ],
)
def test_turn_hard_requirements(changes):
    assert clean_turn(turn(**changes)) is None


def test_exactly_once_delivery_and_equivocation_detection():
    inbox = DeliveryInbox()
    message = clean_turn(turn())
    assert inbox.offer(message) == [message]
    assert inbox.offer(dict(message)) == []
    with pytest.raises(EquivocationError):
        inbox.offer(clean_turn(turn(commit="b" * 64)))


def test_thief_truthfully_answers_capture_and_holds():
    engine = ThiefEngine(1, COMMIT)
    before = engine.position
    incoming = clean_turn(turn(capture_claim=[3, 3]))
    outcome = engine.receive(incoming)
    assert outcome.caught
    message = engine.take_turn(incoming, hold=True)
    assert message["claim_response"] == {"claim": [3, 3], "caught": True}
    assert engine.records[-1]["payload"]["move"] == "STAY"
    assert engine.position == before


def test_barrier_on_thief_and_trapped_thief_are_captures():
    direct = ThiefEngine(1, COMMIT)
    hit = clean_turn(turn(capture_claim=[0, 0], barrier_placed=[3, 3]))
    assert direct.receive(hit).caught
    trapped = ThiefEngine(1, COMMIT)
    for step, barrier in enumerate(([2, 3], [4, 3], [3, 2], [3, 4]), 1):
        message = clean_turn(turn(step=step, commit=f"{step:x}" * 64, barrier_placed=barrier, capture_claim=[0, 0]))
        outcome = trapped.receive(message)
    assert outcome.caught


def test_official_reference_consensus_shape_and_serialization():
    rows = [
        {
            "sub_game_number": 1,
            "result": "survival",
            "roles": {"amireman": "police", "salareen": "thief"},
            "score": {"amireman": 5, "salareen": 10},
            "winner_group": "salareen",
        }
    ]
    value = consensus_preimage("amireman-vs-salareen", rows)
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False)
    assert consensus_sha("amireman-vs-salareen", rows) == hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()
