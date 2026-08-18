"""Operator-managed Ed25519 identity loading."""

import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ENVIRONMENT_VARIABLE = "SALAREEN_THIEF_ED25519_PRIVATE_KEY_PATH"


def load_private_key() -> Ed25519PrivateKey:
    value = os.environ.get(ENVIRONMENT_VARIABLE)
    if not value:
        return Ed25519PrivateKey.generate()
    path = Path(value).expanduser()
    loaded = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(loaded, Ed25519PrivateKey):
        raise TypeError(f"{ENVIRONMENT_VARIABLE} must identify an Ed25519 private key")
    return loaded

