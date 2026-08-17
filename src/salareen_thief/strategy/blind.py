"""Blind shortest-route thief policy with injected tie-breaking."""

from collections.abc import Callable

from salareen_thief.base_logic.actions import MoveAction, MoveChoice
from salareen_thief.base_logic.state_types import EpisodeStatus, Role

from .models import StrategySnapshot
from .results import DecisionError, DecisionFailure, ProposalResult, ProposedAction
from .search import distance_map, shortest_first_choices

TiePolicy = Callable[[tuple[MoveChoice, ...]], MoveChoice]


class BlindShortestPath:
    def __init__(self, tie_policy: TiePolicy) -> None:
        self._tie_policy = tie_policy

    def propose(self, snapshot: StrategySnapshot) -> ProposalResult:
        if snapshot.status is EpisodeStatus.TERMINAL:
            return DecisionFailure(DecisionError.TERMINAL_STATE)
        if not snapshot.board.contains(snapshot.target):
            return DecisionFailure(DecisionError.INVALID_TARGET)
        if snapshot.thief == snapshot.target:
            return ProposedAction(
                MoveAction(Role.THIEF, MoveChoice.STAY, snapshot.thief), 1
            )
        distances = distance_map(snapshot)
        choices = shortest_first_choices(snapshot, distances)
        if not choices:
            return DecisionFailure(
                DecisionError.UNREACHABLE_TARGET, str(snapshot.target)
            )
        chosen = self._tie_policy(choices)
        if chosen not in choices:
            return DecisionFailure(DecisionError.INVALID_TIE_CHOICE, str(chosen))
        action = MoveAction(Role.THIEF, chosen)
        return ProposedAction(action, len(distances))
