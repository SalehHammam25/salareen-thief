"""Test-only deterministic replay helper."""

from collections.abc import Iterable

from salareen_thief.base_logic.action_results import ActionAccepted, ActionResult
from salareen_thief.base_logic.actions import Action
from salareen_thief.base_logic.rules import BaseLogicRules
from salareen_thief.base_logic.state_types import GameState


def replay_actions(
    rules: BaseLogicRules,
    initial: GameState,
    actions: Iterable[Action],
) -> tuple[ActionResult, ...]:
    """Apply actions in order, stopping at the first non-accepted result."""
    state = initial
    results: list[ActionResult] = []
    for action in actions:
        result = rules.apply(state, action)
        results.append(result)
        if not isinstance(result, ActionAccepted):
            break
        state = result.state
    return tuple(results)
