"""Load provider selection only from trusted local TOML."""

import tomllib
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from .models import ProviderMode


@dataclass(frozen=True, slots=True)
class PrivateLanguageConfig:
    provider: ProviderMode = ProviderMode.TEMPLATE
    every_n_steps: int = 1
    timeout_seconds: float = 10.0
    reliability: Decimal = Decimal("0.75")


def load_private_language_config(path: Path) -> PrivateLanguageConfig:
    if not path.exists():
        return PrivateLanguageConfig()
    root = tomllib.loads(path.read_text(encoding="utf-8"))
    section = root.get("trash_talk", {})
    if not isinstance(section, dict):
        raise ValueError("trash_talk must be a table")
    mode = ProviderMode(section.get("provider", ProviderMode.TEMPLATE))
    every = section.get("every_n_steps", 1)
    timeout = section.get("timeout_seconds", 10.0)
    reliability = section.get("reliability", 0.75)
    if isinstance(every, bool) or not isinstance(every, int) or every < 1:
        raise ValueError("every_n_steps must be a positive integer")
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or timeout <= 0
    ):
        raise ValueError("timeout_seconds must be positive")
    if isinstance(reliability, bool) or not isinstance(reliability, (int, float)):
        raise ValueError("reliability must be numeric")
    exact_reliability = Decimal(str(reliability))
    if not Decimal("0.5") <= exact_reliability <= Decimal("1"):
        raise ValueError("reliability must be between 0.5 and 1.0")
    return PrivateLanguageConfig(mode, every, float(timeout), exact_reliability)
