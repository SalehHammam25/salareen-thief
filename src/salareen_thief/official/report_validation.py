"""Fail-closed validation for the full counted result artifact."""

import re

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
TOP_FIELDS = {
    "schema_version",
    "report_type",
    "game_id",
    "game_uid",
    "game_started_at",
    "game_ended_at",
    "timezone",
    "groups",
    "group_details",
    "links",
    "num_sub_games",
    "sub_games",
    "final_result",
    "mutual_agreement",
}
ROW_FIELDS = {
    "sub_game_number",
    "started_at",
    "ended_at",
    "roles",
    "result",
    "winner_group",
    "score",
    "steps",
    "tie",
    "tokens",
    "github_commit",
    "log_files",
    "audit",
}
AUDIT_FIELDS = {
    "log_verified",
    "tampered",
    "local_result_claim",
    "peer_result_claim",
    "result_agreed",
}
FINAL_FIELDS = {
    "total_score",
    "sub_games_won",
    "ties",
    "series_tie",
    "winner_group",
    "tokens_total_series",
}
AGREEMENT_FIELDS = {"confirmed", "results_agreed", "sha256", "peer_sha256", "sha_match"}


def validate_counted_result(doc: dict) -> dict:
    """Reject incomplete or ambiguously keyed counted reports before writing them."""
    if not isinstance(doc, dict) or not TOP_FIELDS <= set(doc):
        raise ValueError("counted result is missing required top-level fields")
    groups = doc["groups"]
    group_set = set(groups) if isinstance(groups, list) else set()
    if len(group_set) != 2 or doc["num_sub_games"] != 6 or len(doc["sub_games"]) != 6:
        raise ValueError("counted result must describe two groups and six sub-games")
    details = doc["group_details"]
    if set(details) != {"group_1", "group_2"}:
        raise ValueError("group_details must contain group_1 and group_2")
    if {block.get("group_id") for block in details.values()} != group_set:
        raise ValueError("group_details do not match groups")
    github = doc["links"].get("github", {})
    urls = [
        github.get(group, {}).get(role) for group in groups for role in ("cop", "thief")
    ]
    if any(not url for url in urls) or len(set(urls)) != 4:
        raise ValueError("all four distinct repository URLs are required")
    for row in doc["sub_games"]:
        if not ROW_FIELDS <= set(row) or not AUDIT_FIELDS <= set(row["audit"]):
            raise ValueError("sub-game row is incomplete")
        for key in ("roles", "score", "tokens", "github_commit", "log_files"):
            if set(row[key]) != group_set:
                raise ValueError(f"sub-game {key} must be keyed by group id")
        if any(
            HEX40.fullmatch(value) is None for value in row["github_commit"].values()
        ):
            raise ValueError("sub-game commits must be full lowercase SHAs")
    final = doc["final_result"]
    if not FINAL_FIELDS <= set(final):
        raise ValueError("final_result is incomplete")
    for key in ("total_score", "sub_games_won", "tokens_total_series"):
        if set(final[key]) != group_set:
            raise ValueError(f"final_result.{key} must be keyed by group id")
    agreement = doc["mutual_agreement"]
    if not AGREEMENT_FIELDS <= set(agreement):
        raise ValueError("mutual_agreement is incomplete")
    if HEX64.fullmatch(agreement["sha256"]) is None:
        raise ValueError("mutual agreement SHA is invalid")
    return doc
