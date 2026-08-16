"""Immutable validated Base Logic configuration."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BoardConfig:
    grid_size: int
    num_agents: int
    thief_start: tuple[int, int]
    cop_start: tuple[int, int]
    axis_origin_corner: str
    axis_start_index: int


@dataclass(frozen=True, slots=True)
class MovementConfig:
    move_set: tuple[str, ...]
    max_barriers: int
    max_moves: int
    survival_threshold: int


@dataclass(frozen=True, slots=True)
class ScoringConfig:
    capture_cop: int
    capture_thief: int
    survival_cop: int
    survival_thief: int
    technical_loss: int


@dataclass(frozen=True, slots=True)
class BaseLogicConfig:
    board: BoardConfig
    movement: MovementConfig
    scoring: ScoringConfig
