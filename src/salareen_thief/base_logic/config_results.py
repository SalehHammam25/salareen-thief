"""Explicit accepted and rejected configuration results."""

from dataclasses import dataclass

from .config_errors import ConfigIssue
from .config_types import BaseLogicConfig


@dataclass(frozen=True, slots=True)
class ConfigAccepted:
    value: BaseLogicConfig


@dataclass(frozen=True, slots=True)
class ConfigRejected:
    issues: tuple[ConfigIssue, ...]


ConfigResult = ConfigAccepted | ConfigRejected
