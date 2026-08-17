"""Approved Stage 5 failure attribution inputs and outcomes."""

from enum import StrEnum


class FailureAttribution(StrEnum):
    LOCAL_TECHNICAL_LOSS = "local_technical_loss"
    REMOTE_TECHNICAL_LOSS = "remote_technical_loss"
    UNKNOWN = "unknown_pending_stage_6_audit"


def attribute_failure(
    *,
    local_server_healthy: bool,
    local_tunnel_healthy: bool,
    remote_application_failure_verified: bool,
    network_or_provider_ambiguous: bool,
) -> FailureAttribution:
    if network_or_provider_ambiguous:
        return FailureAttribution.UNKNOWN
    if not local_server_healthy or not local_tunnel_healthy:
        return FailureAttribution.LOCAL_TECHNICAL_LOSS
    if remote_application_failure_verified:
        return FailureAttribution.REMOTE_TECHNICAL_LOSS
    return FailureAttribution.UNKNOWN
