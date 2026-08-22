"""Deterministic lightweight thief evasion over legally visible geometry."""

from .observer import PoliceObserver
from .policy import EvasionPolicy

__all__ = ["EvasionPolicy", "PoliceObserver"]
