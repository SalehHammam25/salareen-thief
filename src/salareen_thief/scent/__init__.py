"""Opponent-scent values; spatial evolution awaits approved rules."""

from .config import LanguageScentConfig, load_language_scent_config
from .models import OpponentScent, ScentGrid

__all__ = [
    "LanguageScentConfig",
    "OpponentScent",
    "ScentGrid",
    "load_language_scent_config",
]
