"""Semantic validation and construction of Base Logic configuration."""

from typing import Any, cast

from .config_errors import ConfigErrorCategory as Category
from .config_errors import ConfigIssue
from .config_extract import Path, extract_values
from .config_results import ConfigAccepted, ConfigRejected, ConfigResult
from .config_schema import FIXED_VALUES, MINIMUM_VALUES
from .config_types import (
    BaseLogicConfig,
    BoardConfig,
    MovementConfig,
    ScoringConfig,
)


def _issue(category: Category, path: Path, message: str) -> ConfigIssue:
    return ConfigIssue(category, path, message)


def _constraints(
    values: dict[Path, Any], issues: list[ConfigIssue]
) -> None:
    for path, minimum in MINIMUM_VALUES:
        if path in values and values[path] < minimum:
            issues.append(
                _issue(Category.BELOW_MINIMUM, path, f"minimum is {minimum}")
            )
    for path, expected in FIXED_VALUES:
        if path in values and values[path] != expected:
            issues.append(
                _issue(
                    Category.FIXED_VALUE_DEVIATION,
                    path,
                    f"fixed value is {expected!r}",
                )
            )
    ceiling_path = ("movement_and_barriers", "max_moves")
    survival_path = ("movement_and_barriers", "survival_threshold")
    if (
        ceiling_path in values
        and survival_path in values
        and values[ceiling_path] != values[survival_path]
    ):
        issues.append(
            _issue(
                Category.RELATIONSHIP_MISMATCH,
                survival_path,
                "survival threshold must equal move ceiling",
            )
        )
    grid = values.get(("board_and_agents", "grid_size"))
    start = values.get(("board_and_agents", "axis_start_index"))
    if type(grid) is int and type(start) is int and grid >= 7:
        upper = start + grid - 1
        for field in ("thief_start", "cop_start"):
            path = ("board_and_agents", field)
            coordinate = values.get(path)
            outside = coordinate and not all(
                start <= part <= upper for part in coordinate
            )
            if outside:
                issues.append(
                    _issue(
                        Category.OUT_OF_BOUNDS,
                        path,
                        f"coordinates must be in [{start}, {upper}]",
                    )
                )


def _build(values: dict[Path, Any]) -> BaseLogicConfig:
    board = BoardConfig(
        cast(int, values[("board_and_agents", "grid_size")]),
        cast(int, values[("board_and_agents", "num_agents")]),
        cast(tuple[int, int], values[("board_and_agents", "thief_start")]),
        cast(tuple[int, int], values[("board_and_agents", "cop_start")]),
        cast(str, values[("board_and_agents", "axis_origin_corner")]),
        cast(int, values[("board_and_agents", "axis_start_index")]),
    )
    movement = MovementConfig(
        cast(tuple[str, ...], values[("movement_and_barriers", "move_set")]),
        cast(int, values[("movement_and_barriers", "max_barriers")]),
        cast(int, values[("movement_and_barriers", "max_moves")]),
        cast(int, values[("movement_and_barriers", "survival_threshold")]),
    )
    scoring = ScoringConfig(
        cast(int, values[("scoring", "capture_cop")]),
        cast(int, values[("scoring", "capture_thief")]),
        cast(int, values[("scoring", "survival_cop")]),
        cast(int, values[("scoring", "survival_thief")]),
        cast(int, values[("scoring", "technical_loss")]),
    )
    return BaseLogicConfig(board, movement, scoring)


def validate_config(data: Any) -> ConfigResult:
    """Return a complete immutable configuration or ordered issues."""
    values, issues = extract_values(data)
    _constraints(values, issues)
    if issues:
        return ConfigRejected(tuple(issues))
    return ConfigAccepted(_build(values))
