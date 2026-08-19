import base64
import binascii
import os
import platform
import subprocess
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from salareen_thief.security.protocol import (
    SecurityViolation,
    require_identical_config,
    sign,
    validate_step0,
    verify,
)


def build_step0(role: str) -> dict[str, Any]:
    commit = (
        os.environ.get("SALAREEN_GIT_COMMIT")
        or subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    )
    return {
        "protocol_version": "1.0",
        "role": role,
        "team": "salareen",
        "model": os.environ.get("SALAREEN_MODEL", "deterministic"),
        "provider": os.environ.get("SALAREEN_PROVIDER", "local"),
        "os": platform.system(),
        "cpu_cores": os.cpu_count() or 1,
        "cpu_frequency_mhz": 0,
        "ram_bytes": 0,
        "gpu": "undisclosed",
        "vram_bytes": 0,
        "game_count": 6,
        "git_commit": commit,
        "token_budget": 0,
        "token_usage": 0,
    }


def build_bundle(runtime: Any) -> dict[str, Any]:
    public = runtime.public.public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    body = {
        "config": base64.b64encode(runtime.config).decode("ascii"),
        "step0": runtime.step0,
        "public_key": base64.b64encode(public).decode("ascii"),
    }
    return {
        **body,
        "config_signature": sign(runtime.key, {"config": body["config"]}),
        "step0_signature": sign(runtime.key, runtime.step0),
    }


def accept_bundle(runtime: Any, bundle: dict[str, Any]) -> None:
    try:
        public_raw = base64.b64decode(bundle["public_key"], validate=True)
        peer_config = base64.b64decode(bundle["config"], validate=True)
        public = Ed25519PublicKey.from_public_bytes(public_raw)
    except (KeyError, ValueError, binascii.Error) as exc:
        raise SecurityViolation("malformed security bootstrap") from exc
    require_identical_config(runtime.config, peer_config)
    if runtime.expected_peer_public and public_raw != runtime.expected_peer_public:
        raise SecurityViolation("unexpected peer public key")
    validate_step0(bundle["step0"])
    if bundle["step0"]["role"] == runtime.role:
        raise SecurityViolation("peer role must differ")
    verify(public, {"config": bundle["config"]}, bundle["config_signature"])
    verify(public, bundle["step0"], bundle["step0_signature"])
    runtime.peer_verified = True
    runtime.audit.append("bootstrap", {"peer_role": bundle["step0"]["role"]})
