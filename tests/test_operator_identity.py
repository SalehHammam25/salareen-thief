"""Operator-managed production identity tests."""

import base64

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from salareen_thief.live_match.security_runtime import LiveSecurity
from salareen_thief.security.protocol import SecurityViolation

CONFIG = "config/game.json"
PRIVATE_ENV = "SALAREEN_THIEF_ED25519_PRIVATE_KEY_PATH"
PEER_ENV = "SALAREEN_THIEF_EXPECTED_PEER_PUBLIC_KEY"


def write_key(path):
    key = Ed25519PrivateKey.generate()
    path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    return key


def raw_public(key):
    return key.public_key().public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    )


def test_restart_preserves_operator_identity(tmp_path, monkeypatch):
    path = tmp_path / "identity.pem"
    key = write_key(path)
    monkeypatch.setenv(PRIVATE_ENV, str(path))
    first = LiveSecurity("thief", CONFIG, "game")
    restarted = LiveSecurity("thief", CONFIG, "game")
    assert raw_public(first.key) == raw_public(key)
    assert raw_public(restarted.key) == raw_public(key)


def test_unexpected_peer_identity_is_rejected(tmp_path, monkeypatch):
    path = tmp_path / "identity.pem"
    write_key(path)
    expected = raw_public(Ed25519PrivateKey.generate())
    monkeypatch.setenv(PRIVATE_ENV, str(path))
    monkeypatch.setenv(PEER_ENV, base64.b64encode(expected).decode("ascii"))
    local = LiveSecurity("thief", CONFIG, "game")
    peer = LiveSecurity("cop", CONFIG, "game")
    with pytest.raises(SecurityViolation, match="unexpected peer public key"):
        local.accept_bundle(peer.bundle())

