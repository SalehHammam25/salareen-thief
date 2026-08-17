"""Immutable state reconstruction and terminal transition helpers."""

from .action_results import ActionAccepted
from .config_types import BaseLogicConfig
from .state_factory import build_state
from .state_results import StateAccepted
from .state_types import (
    AgentPositions,
    EpisodeStatus,
    GameState,
    Outcome,
    OutcomeKind,
)


def rebuild(
    config: BaseLogicConfig,
    state: GameState,
    **changes,
) -> GameState:
    """Revalidate a controlled immutable state replacement."""
    positions = changes.get("positions", state.positions)
    values = {
        "thief": positions.thief,
        "cop": positions.cop,
        "barriers": changes.get("barriers", state.barriers),
        "barrier_usage": changes.get("barrier_usage", state.barrier_usage),
        "valid_steps": changes.get("valid_steps", state.valid_steps),
        "status": changes.get("status", state.status),
        "outcome": changes.get("outcome", state.outcome),
    }
    result = build_state(config, **values)
    assert isinstance(result, StateAccepted)
    return result.value


def finish_step(
    config: BaseLogicConfig,
    state: GameState,
    *,
    positions: AgentPositions | None = None,
    barriers=None,
    barrier_usage: int | None = None,
    capture: Outcome | None = None,
) -> ActionAccepted:
    """Count one valid action, giving capture priority over survival."""
    changes = {"valid_steps": state.valid_steps + 1}
    if positions is not None:
        changes["positions"] = positions
    if barriers is not None:
        changes["barriers"] = barriers
    if barrier_usage is not None:
        changes["barrier_usage"] = barrier_usage
    if capture is not None:
        changes.update(status=EpisodeStatus.TERMINAL, outcome=capture)
    elif changes["valid_steps"] >= config.movement.survival_threshold:
        changes.update(
            status=EpisodeStatus.TERMINAL,
            outcome=Outcome(OutcomeKind.SURVIVAL),
        )
    return ActionAccepted(rebuild(config, state, **changes))
