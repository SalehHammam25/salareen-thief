"""Proof that gameplay rules consume validated configuration values."""

from dataclasses import replace

from salareen_thief.base_logic.action_results import ActionAccepted
from salareen_thief.base_logic.actions import BarrierAction, MoveAction, MoveChoice
from salareen_thief.base_logic.rules import BaseLogicRules
from salareen_thief.base_logic.state_factory import build_state, initial_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import Coordinate, OutcomeKind, Role


def test_rules_use_increased_barrier_quota(accepted_config) -> None:
    movement = replace(accepted_config.movement, max_barriers=15)
    config = replace(accepted_config, movement=movement)
    built = build_state(
        config,
        thief=Coordinate(3, 3),
        cop=Coordinate(0, 0),
        barrier_usage=14,
    )
    assert isinstance(built, StateAccepted)
    result = BaseLogicRules(config).apply(
        built.value, BarrierAction(Role.COP, Coordinate(0, 1))
    )
    assert isinstance(result, ActionAccepted)
    assert result.state.barrier_usage == 15


def test_rules_use_increased_equal_survival_values(accepted_config) -> None:
    movement = replace(accepted_config.movement, max_moves=36, survival_threshold=36)
    config = replace(accepted_config, movement=movement)
    initial = initial_state(config)
    assert isinstance(initial, StateAccepted)
    built = build_state(
        config,
        thief=initial.value.positions.thief,
        cop=initial.value.positions.cop,
        valid_steps=34,
    )
    assert isinstance(built, StateAccepted)
    rules = BaseLogicRules(config)
    step_35 = rules.apply(built.value, MoveAction(Role.THIEF, MoveChoice.STAY))
    assert isinstance(step_35, ActionAccepted)
    assert step_35.state.outcome is None
    step_36 = rules.apply(step_35.state, MoveAction(Role.THIEF, MoveChoice.STAY))
    assert isinstance(step_36, ActionAccepted)
    assert step_36.state.outcome.kind is OutcomeKind.SURVIVAL
