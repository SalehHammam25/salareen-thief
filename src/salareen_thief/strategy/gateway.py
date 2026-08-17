"""Validate every strategy proposal through deterministic Base Logic."""

from typing import Protocol

from salareen_thief.base_logic.action_results import ActionAccepted
from salareen_thief.base_logic.actions import MoveAction
from salareen_thief.base_logic.rules import BaseLogicRules
from salareen_thief.base_logic.state_types import Coordinate, GameState, Role

from .models import StrategySnapshot, snapshot_for
from .results import (
    DecisionError,
    DecisionFailure,
    DecisionResult,
    ProposalResult,
    ProposedAction,
    ValidatedDecision,
)


class ThiefPolicy(Protocol):
    def propose(self, snapshot: StrategySnapshot) -> ProposalResult: ...


class StrategyGateway:
    def __init__(self, rules: BaseLogicRules, policy: ThiefPolicy) -> None:
        self._rules = rules
        self._policy = policy

    def decide(self, state: GameState, target: Coordinate) -> DecisionResult:
        try:
            proposal = self._policy.propose(snapshot_for(state, target))
        except Exception as error:
            return DecisionFailure(DecisionError.POLICY_EXCEPTION, type(error).__name__)
        if isinstance(proposal, DecisionFailure):
            return proposal
        if not isinstance(proposal, ProposedAction):
            return DecisionFailure(DecisionError.INVALID_PROPOSAL)
        action = proposal.action
        if not isinstance(action, MoveAction) or action.role is not Role.THIEF:
            return DecisionFailure(DecisionError.INVALID_PROPOSAL)
        validated = self._rules.apply(state, action)
        if not isinstance(validated, ActionAccepted):
            detail = getattr(validated, "error", getattr(validated, "question", ""))
            return DecisionFailure(DecisionError.ILLEGAL_PROPOSAL, str(detail))
        return ValidatedDecision(action, validated.state)
