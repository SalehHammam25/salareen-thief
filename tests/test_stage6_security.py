import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from salareen_thief.security.protocol import (
    AppendOnlyAuditLog,
    CommitReveal,
    SecurityViolation,
    canonical_bytes,
    commitment,
    fresh_nonce,
    parse_canonical,
    require_identical_config,
    sign,
    verify,
    verify_capture_claim,
)


def test_canonical_vector_and_config_mismatch():
    fixture = json.loads(
        (Path(__file__).parent / "fixtures/stage6/canonical-vector.json").read_text()
    )
    assert canonical_bytes(fixture["payload"]).hex() == fixture["expected_hex"]
    data = canonical_bytes(fixture["payload"])
    assert require_identical_config(data, data) == fixture["payload"]
    with pytest.raises(SecurityViolation):
        require_identical_config(data, data + b" ")
    with pytest.raises(SecurityViolation):
        parse_canonical(b'{"x":1,"x":2}')


def test_ed25519_preserves_base64_case_and_rejects_tamper():
    private = Ed25519PrivateKey.generate()
    payload = {"team": "Salareen", "game_count": 6}
    signature = sign(private, payload)
    verify(private.public_key(), payload, signature)
    with pytest.raises(SecurityViolation):
        verify(private.public_key(), {**payload, "game_count": 5}, signature)
    swapped = signature.swapcase()
    if swapped != signature:
        with pytest.raises(SecurityViolation):
            verify(private.public_key(), payload, swapped)


def test_commit_ack_reveal_final_nonce_audit_and_secrecy():
    payload = {"game_id": "g1", "turn": 1, "role": "cop", "move": "N"}
    nonce = fresh_nonce()
    digest = commitment(payload, nonce)
    machine = CommitReveal()
    machine.commit(digest)
    with pytest.raises(SecurityViolation):
        machine.reveal(payload)
    machine.acknowledge()
    machine.reveal(payload)
    assert nonce.hex() not in repr(machine)
    machine.audit(nonce)
    assert machine.phase == "audited"
    assert commitment(payload, fresh_nonce()) != digest


def test_capture_claim_and_append_only_tamper_rejection():
    claim = {
        "game_id": "g1",
        "turn": 2,
        "claimant_role": "cop",
        "kind": "overlap",
        "cop": [2, 2],
        "thief": [2, 2],
        "barriers": [],
    }
    verify_capture_claim(claim)
    with pytest.raises(SecurityViolation):
        verify_capture_claim({**claim, "thief": [3, 2]})
    log = AppendOnlyAuditLog()
    log.append("commit", {"digest": "a" * 64})
    log.append("acknowledgement", {"turn": 2})
    log.verify()
    log.entries[0]["payload"]["digest"] = "b" * 64
    with pytest.raises(SecurityViolation):
        log.verify()
