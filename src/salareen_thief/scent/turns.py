"""Couple accepted movement to scent without changing Base Logic."""

from dataclasses import dataclass

from salareen_thief.base_logic.action_results import ActionAccepted, ActionResult
from salareen_thief.base_logic.actions import Action, MoveAction
from salareen_thief.base_logic.rules import BaseLogicRules
from salareen_thief.base_logic.state_types import GameState

from .field import evolve
from .models import ScentGrid


@dataclass(frozen=True, slots=True)
class ScentTurn:
    action_result: ActionResult
    scent: ScentGrid


def apply_scent_turn(
    rules: BaseLogicRules,
    state: GameState,
    action: Action,
    scent: ScentGrid,
) -> ScentTurn:
    result = rules.apply(state, action)
    if not isinstance(result, ActionAccepted) or not isinstance(action, MoveAction):
        return ScentTurn(result, scent)
    position = result.state.positions.for_role(action.role)
    return ScentTurn(result, evolve(scent, result.state.board, position))
