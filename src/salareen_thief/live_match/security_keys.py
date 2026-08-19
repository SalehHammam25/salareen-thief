"""Operator-managed Ed25519 identity loading."""

import base64
import binascii
import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ENVIRONMENT_VARIABLE = "SALAREEN_THIEF_ED25519_PRIVATE_KEY_PATH"
EXPECTED_PEER_VARIABLE = "SALAREEN_THIEF_EXPECTED_PEER_PUBLIC_KEY"


def load_private_key() -> Ed25519PrivateKey:
    value = os.environ.get(ENVIRONMENT_VARIABLE)
    if not value:
        return Ed25519PrivateKey.generate()
    path = Path(value).expanduser()
    loaded = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(loaded, Ed25519PrivateKey):
        raise TypeError(f"{ENVIRONMENT_VARIABLE} must identify an Ed25519 private key")
    return loaded


def load_expected_peer_key() -> bytes | None:
    value = os.environ.get(EXPECTED_PEER_VARIABLE)
    if not value:
        return None
    try:
        raw = base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError(f"{EXPECTED_PEER_VARIABLE} must be Base64") from exc
    if len(raw) != 32:
        raise ValueError(f"{EXPECTED_PEER_VARIABLE} must encode 32 bytes")
    return raw
