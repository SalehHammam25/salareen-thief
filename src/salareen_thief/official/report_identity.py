"""Runtime-sourced identity blocks for counted official reports."""

import os
import platform

from .terms import GROUP_ID, GROUP_NAME, MEMBERS

SALAREEN_REPOS = {
    "cop": "https://github.com/SalehHammam25/salareen-cop",
    "thief": "https://github.com/SalehHammam25/salareen-thief",
}
AMIREMAN_REPOS = {
    "cop": "https://github.com/AMIR13BD/Game-P2P-Cop-Chase-Police",
    "thief": "https://github.com/AMIR13BD/Game-P2P-Cop-Chase-Thief",
}
AMIREMAN_MEMBERS = ["Amir Fadila", "Eman Sarhan"]


def hardware_spec() -> dict:
    """Return truthful, standard-library-only runtime hardware metadata."""
    return {
        "cpu_cores": os.cpu_count(),
        "cpu_type": platform.machine(),
        "operating_system": platform.platform(),
        "python_version": platform.python_version(),
    }


def salareen_identity(commits: dict[str, str], public_mcp_url: str, model: str) -> dict:
    """Build the identity Salareen advertises and serializes for a counted run."""
    return {
        "group_id": GROUP_ID,
        "group_name": GROUP_NAME,
        "members": list(MEMBERS),
        "repos": dict(SALAREEN_REPOS),
        "github_commit": commits["police"],
        "git_commit_hash": commits["police"],
        "role_commits": dict(commits),
        "mcp_servers": {"cop": public_mcp_url, "thief": public_mcp_url},
        "llm_model": model,
        "hardware_spec": hardware_spec(),
    }


def opponent_identity(source: dict, group: str, endpoint: str) -> dict:
    """Complete only peer fields known from its greeting or pairing configuration."""
    value = dict(source) if isinstance(source, dict) else {}
    value.setdefault("group_id", group)
    value.setdefault("group_name", group)
    value.setdefault("members", list(AMIREMAN_MEMBERS) if group == "amireman" else [])
    declared_repos = value.get("repos") if isinstance(value.get("repos"), dict) else {}
    defaults = AMIREMAN_REPOS if group == "amireman" else {}
    value["repos"] = {**defaults, **declared_repos}
    declared_mcp = value.get("mcp_servers")
    if not isinstance(declared_mcp, dict) or not declared_mcp:
        value["mcp_servers"] = {"cop": endpoint, "thief": endpoint}
    value.setdefault("llm_model", "peer-declared")
    spec = value.get("hardware_spec", value.get("spec", {}))
    value["hardware_spec"] = spec if isinstance(spec, dict) else {}
    return value


def group_block(identity: dict, commit: str) -> dict:
    """Shape one identity into the shared full-result group block."""
    return {
        "group_id": identity.get("group_id", ""),
        "group_name": identity.get("group_name", ""),
        "members": list(identity.get("members", [])),
        "repos": dict(identity.get("repos", {})),
        "git_commit_hash": commit,
        "github_commit": commit,
        "mcp_servers": dict(identity.get("mcp_servers", {})),
        "llm_model": identity.get("llm_model", ""),
        "hardware_spec": dict(identity.get("hardware_spec", {})),
    }
