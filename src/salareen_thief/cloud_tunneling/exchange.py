"""Manual/private endpoint injection; no shared runtime state or discovery."""

from collections.abc import Mapping
from dataclasses import dataclass, field

from .endpoints import redact_endpoint, validate_remote_endpoint
from .models import TunnelEndpoint, TunnelFailure


@dataclass(frozen=True, slots=True)
class EndpointExchange:
    opponent: TunnelEndpoint = field(repr=False)

    @property
    def safe_display(self) -> str:
        return redact_endpoint(self.opponent.url)


def load_opponent_endpoint(
    env: Mapping[str, str],
) -> EndpointExchange | TunnelFailure:
    checked = validate_remote_endpoint(env.get("SALAREEN_OPPONENT_URL", ""))
    if isinstance(checked, TunnelFailure):
        return checked
    return EndpointExchange(checked)
