"""Private stable-domain configuration for the ngrok adapter."""

import re
from collections.abc import Mapping
from dataclasses import dataclass, field

DOMAIN = re.compile(
    r"(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?\Z"
)


@dataclass(frozen=True, slots=True)
class NgrokConfig:
    local_port: int
    domain: str = field(repr=False)
    api_url: str = "http://127.0.0.1:4040/api/tunnels"
    readiness_attempts: int = 30
    readiness_interval: float = 0.2

    def __post_init__(self) -> None:
        domain = self.domain.strip().casefold()
        if type(self.local_port) is not int or not 1 <= self.local_port <= 65535:
            raise ValueError("local_port must be an explicit valid port")
        if not DOMAIN.fullmatch(domain):
            raise ValueError("NGROK_DOMAIN must be a bare stable DNS domain")
        if type(self.readiness_attempts) is not int or self.readiness_attempts < 1:
            raise ValueError("readiness_attempts must be a positive exact integer")
        if type(self.readiness_interval) not in {int, float}:
            raise ValueError("readiness_interval must be an exact number")
        if self.readiness_interval < 0:
            raise ValueError("readiness_interval cannot be negative")
        object.__setattr__(self, "domain", domain)

    @property
    def public_url(self) -> str:
        return f"https://{self.domain}"


def load_ngrok_config(env: Mapping[str, str], local_port: int) -> NgrokConfig:
    return NgrokConfig(local_port, env.get("NGROK_DOMAIN", ""))
