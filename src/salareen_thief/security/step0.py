"""Signed Step-0 declaration validation."""

from collections.abc import Mapping
from typing import Any


def validate_step0(value: Mapping[str, Any]) -> None:
    from .protocol import SecurityViolation

    required = {
        "protocol_version",
        "role",
        "team",
        "model",
        "provider",
        "os",
        "cpu_cores",
        "cpu_frequency_mhz",
        "ram_bytes",
        "gpu",
        "vram_bytes",
        "game_count",
        "git_commit",
        "token_budget",
        "token_usage",
    }
    if set(value) != required:
        raise SecurityViolation("Step 0 fields do not match the contract")
    if value["role"] not in {"cop", "thief"} or value["game_count"] != 6:
        raise SecurityViolation("invalid Step 0 role or game count")
    commit = value["git_commit"]
    if not isinstance(commit, str) or len(commit) != 40:
        raise SecurityViolation("invalid exact Git commit")
