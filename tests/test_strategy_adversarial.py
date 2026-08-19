"""Strategy isolation and malicious-policy tests."""

from dataclasses import FrozenInstanceError

import pytest

from salareen_thief.base_logic.actions import MoveAction, MoveChoice
from salareen_thief.base_logic.state_types import Coordinate, Role
from salareen_thief.strategy.blind import BlindShortestPath
from salareen_thief.strategy.gateway import StrategyGateway
from salareen_thief.strategy.models import snapshot_for
from salareen_thief.strategy.results import (
    DecisionError,
    DecisionFailure,
    ProposedAction,
)


def first(choices):
    return choices[0]


def test_snapshot_is_frozen_and_hides_opponent_and_stage4_inputs(initial_game) -> None:
    snapshot = snapshot_for(initial_game, Coordinate(6, 6))
    assert not hasattr(snapshot, "cop")
    assert not hasattr(snapshot, "scent")
    assert not hasattr(snapshot, "language")
    with pytest.raises(FrozenInstanceError):
        snapshot.target = Coordinate(0, 0)  # type: ignore[misc]


def test_invalid_tie_choice_is_typed_failure(initial_game) -> None:
    policy = BlindShortestPath(lambda _: MoveChoice.STAY)
    result = policy.propose(snapshot_for(initial_game, Coordinate(4, 4)))
    assert isinstance(result, DecisionFailure)
    assert result.error is DecisionError.INVALID_TIE_CHOICE


def test_terminal_state_is_typed_failure(rules, initial_game) -> None:
    terminal = rules.technical_loss(initial_game).state
    result = BlindShortestPath(first).propose(snapshot_for(terminal, Coordinate(6, 6)))
    assert result == DecisionFailure(DecisionError.TERMINAL_STATE)


class DiagonalPolicy:
    def propose(self, snapshot):
        return ProposedAction(
            MoveAction(Role.THIEF, MoveChoice.NORTH, Coordinate(2, 4)), 0
        )


def test_illegal_policy_cannot_bypass_base_logic(rules, initial_game) -> None:
    before = initial_game
    result = StrategyGateway(rules, DiagonalPolicy()).decide(
        initial_game, Coordinate(6, 6)
    )
    assert isinstance(result, DecisionFailure)
    assert result.error is DecisionError.ILLEGAL_PROPOSAL
    assert initial_game is before


class ExplodingPolicy:
    def propose(self, snapshot):
        raise RuntimeError("untrusted policy")


def test_policy_exception_becomes_typed_failure(rules, initial_game) -> None:
    result = StrategyGateway(rules, ExplodingPolicy()).decide(
        initial_game, Coordinate(6, 6)
    )
    assert result == DecisionFailure(DecisionError.POLICY_EXCEPTION, "RuntimeError")


class WrongRolePolicy:
    def propose(self, snapshot):
        return ProposedAction(MoveAction(Role.COP, MoveChoice.STAY), 0)


def test_wrong_role_proposal_rejected_before_base_logic(rules, initial_game) -> None:
    result = StrategyGateway(rules, WrongRolePolicy()).decide(
        initial_game, Coordinate(6, 6)
    )
    assert result == DecisionFailure(DecisionError.INVALID_PROPOSAL)
