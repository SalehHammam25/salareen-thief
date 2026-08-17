"""Narrow adapters from live messages to existing deterministic stages."""

import json
from pathlib import Path
from typing import Any

from salareen_thief.base_logic.action_results import ActionAccepted
from salareen_thief.base_logic.actions import (
    BarrierAction,
    CaptureClaim,
    MoveAction,
    MoveChoice,
)
from salareen_thief.base_logic.config_loader import load_config
from salareen_thief.base_logic.config_results import ConfigAccepted
from salareen_thief.base_logic.rules import BaseLogicRules
from salareen_thief.base_logic.scoring import ScoreAccepted, score_episode
from salareen_thief.base_logic.state_factory import build_state, initial_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import (
    CaptureCause,
    Coordinate,
    EpisodeStatus,
    Outcome,
    OutcomeKind,
    Role,
)
from salareen_thief.scent.field import empty_field, evolve
from salareen_thief.strategy.blind import BlindShortestPath
from salareen_thief.strategy.gateway import StrategyGateway
from salareen_thief.strategy.results import ValidatedDecision


class GameplayAdapter:
    def __init__(self, config_path: str | Path, saved: str | None = None) -> None:
        loaded = load_config(config_path)
        if not isinstance(loaded, ConfigAccepted):
            raise ValueError("invalid shared configuration")
        self.config = loaded.value
        self.rules = BaseLogicRules(self.config)
        created = initial_state(self.config) if saved is None else self._restore(saved)
        if not isinstance(created, StateAccepted):
            raise ValueError("invalid game state")
        self.state = created.value
        self.scent = empty_field(self.state.board)
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

    def capture(self, payload: dict[str, Any], *, apply: bool) -> tuple[str, str] | None:
        causes = {"cooccupancy": CaptureCause.COORDINATE_OVERLAP,
                  "trapped": CaptureCause.TRAPPED_THIEF}
        cause = causes.get(payload["capture_kind"])
        if payload["claimant_role"] != "cop" or cause is None:
            return "CAPTURE_REJECTED", "capture_kind"
        expected = (self.state.positions.cop.row, self.state.positions.cop.col,
                    self.state.positions.thief.row, self.state.positions.thief.col)
        claimed = tuple(payload[key] for key in ("cop_x", "cop_y", "thief_x", "thief_y"))
        if claimed != expected:
            return "CAPTURE_REJECTED", "coordinates"
        if self.state.status is EpisodeStatus.TERMINAL:
            return None if self.state.outcome and self.state.outcome.capture_cause else (
                "CAPTURE_REJECTED", "local_consistency")
        result = self.rules.apply(self.state, CaptureClaim(Role.COP, cause))
        if not isinstance(result, ActionAccepted):
            return "CAPTURE_REJECTED", "local_consistency"
        if apply:
            self.state = result.state
        return None

    def intent_for(self, decision: ValidatedDecision) -> dict[str, Any]:
        action = decision.action
        if isinstance(action, BarrierAction):
            return {"action_kind": "barrier", "direction": None,
                    "x": action.target.row, "y": action.target.col}
        kind = "stay" if action.choice is MoveChoice.STAY else "move"
        return {"action_kind": kind, "direction": action.choice.value,
                "x": None, "y": None}

    def snapshot(self) -> str:
        outcome = self.state.outcome
        data = {"thief": self._point(self.state.positions.thief),
                "cop": self._point(self.state.positions.cop),
                "barriers": [self._point(item) for item in sorted(self.state.barriers)],
                "barrier_usage": self.state.barrier_usage,
                "valid_steps": self.state.valid_steps,
                "status": self.state.status.value,
                "outcome": None if outcome is None else outcome.kind.value,
                "capture_cause": None if outcome is None or outcome.capture_cause is None
                else outcome.capture_cause.value}
        return json.dumps(data, sort_keys=True, separators=(",", ":"))

    def score(self) -> tuple[int, int]:
        result = score_episode(self.state, self.config.scoring)
        if not isinstance(result, ScoreAccepted):
            raise ValueError("episode is not scoreable")
        return result.score.cop, result.score.thief

    def _restore(self, saved: str):
        data = json.loads(saved)
        outcome = None
        if data["outcome"] is not None:
            cause = data["capture_cause"]
            outcome = Outcome(OutcomeKind(data["outcome"]),
                              None if cause is None else CaptureCause(cause))
        return build_state(self.config, thief=Coordinate(*data["thief"]),
            cop=Coordinate(*data["cop"]),
            barriers=(Coordinate(*item) for item in data["barriers"]),
            barrier_usage=data["barrier_usage"], valid_steps=data["valid_steps"],
            status=EpisodeStatus(data["status"]), outcome=outcome)

    @staticmethod
    def _point(value: Coordinate) -> list[int]:
        return [value.row, value.col]

    def _action(self, payload: dict[str, Any]):
        role = Role(payload["sender_role"])
        if payload["action_kind"] == "barrier":
            target = Coordinate(payload["x"], payload["y"])
            claim = (CaptureClaim(Role.COP, CaptureCause.BARRIER_ON_THIEF)
                     if target == self.state.positions.thief else None)
            return BarrierAction(role, target, claim)
        return MoveAction(role, MoveChoice(payload["direction"]))
