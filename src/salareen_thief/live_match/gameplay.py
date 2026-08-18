"""Narrow adapters from live messages to existing deterministic stages."""

from pathlib import Path
from typing import Any

from salareen_thief.base_logic.action_results import ActionAccepted
from salareen_thief.base_logic.actions import (
    BarrierAction,
    MoveAction,
    MoveChoice,
)
from salareen_thief.base_logic.config_loader import load_config
from salareen_thief.base_logic.config_results import ConfigAccepted
from salareen_thief.base_logic.rules import BaseLogicRules
from salareen_thief.base_logic.scoring import ScoreAccepted, score_episode
from salareen_thief.base_logic.state_factory import initial_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import Coordinate
from salareen_thief.scent.field import empty_field, evolve
from salareen_thief.strategy.blind import BlindShortestPath
from salareen_thief.strategy.gateway import StrategyGateway
from salareen_thief.strategy.results import ValidatedDecision

from .gameplay_capture import verify_capture
from .gameplay_snapshot import snapshot
from .gameplay_state import action_for, restore_state
from .persistence import restore_runtime
from .stage4 import Stage4Boundary


class GameplayAdapter:
    def __init__(
        self, config_path: str | Path, saved: str | None = None, *, defer: bool = False
    ) -> None:
        self.config_path, self.saved = Path(config_path), saved
        if not defer:
            self.initialize()

    def initialize(self) -> None:
        if hasattr(self, "state"):
            return
        source = self.config_path
        loaded = load_config(source)
        if not isinstance(loaded, ConfigAccepted):
            raise ValueError("invalid shared configuration")
        self.config = loaded.value
        self.rules = BaseLogicRules(self.config)
        created = (
            initial_state(self.config)
            if self.saved is None
            else self._restore(self.saved)
        )
        if not isinstance(created, StateAccepted):
            raise ValueError("invalid game state")
        self.state = created.value
        self.scent = empty_field(self.state.board)
        self.stage4 = Stage4Boundary(source, self.state.board)
        if self.saved:
            self.scent = restore_runtime(self.saved, self.scent, self.stage4)
        self.gateway = StrategyGateway(self.rules, BlindShortestPath())

    def propose(self, target: Coordinate):
        return self.gateway.decide(self.state, target)

    def apply_payload(self, payload: dict[str, Any]) -> tuple[bool, str]:
        action = self._action(payload)
        result = self.rules.apply(self.state, action)
        if not isinstance(result, ActionAccepted):
            detail = getattr(result, "error", getattr(result, "question", "rejected"))
            return False, str(detail)
        self.state = result.state
        if isinstance(action, MoveAction):
            position = self.state.positions.for_role(action.role)
            self.scent = evolve(self.scent, self.state.board, position)
        return True, "applied"

    def validate_payload(self, payload: dict[str, Any]) -> tuple[str, str] | None:
        result = self.rules.apply(self.state, self._action(payload))
        if isinstance(result, ActionAccepted):
            return None
        detail = getattr(result, "error", getattr(result, "question", "rejected"))
        return "ACTION_REJECTED", str(detail)

    def capture(
        self, payload: dict[str, Any], *, apply: bool
    ) -> tuple[str, str] | None:
        return verify_capture(self, payload, apply=apply)

    def intent_for(self, decision: ValidatedDecision) -> dict[str, Any]:
        action = decision.action
        if isinstance(action, BarrierAction):
            return {
                "action_kind": "barrier",
                "direction": None,
                "x": action.target.row,
                "y": action.target.col,
            }
        kind = "stay" if action.choice is MoveChoice.STAY else "move"
        return {
            "action_kind": kind,
            "direction": action.choice.value,
            "x": None,
            "y": None,
        }

    def snapshot(self) -> str:
        return snapshot(self)

    def score(self) -> tuple[int, int]:
        result = score_episode(self.state, self.config.scoring)
        if not isinstance(result, ScoreAccepted):
            raise ValueError("episode is not scoreable")
        return result.score.cop, result.score.thief

    def _restore(self, saved: str):
        return restore_state(self, saved)

    def _action(self, payload: dict[str, Any]):
        return action_for(self, payload)
