"""Stage 4 shared-configuration validation."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from salareen_thief.base_logic.config_decode import DuplicateKeyError, decode_json


@dataclass(frozen=True, slots=True)
class LanguageScentConfig:
    center_intensity: float
    decay_rate: float
    field_size: int
    map_area: str
    hint_max_words: int
    token_budget_per_series: int


@dataclass(frozen=True, slots=True)
class Stage4ConfigError(ValueError):
    category: str
    path: str


def _object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise Stage4ConfigError("incorrect_type", path)
    return value


def _required(section: dict[str, Any], key: str, parent: str) -> Any:
    if key not in section:
        raise Stage4ConfigError("missing_key", f"{parent}.{key}")
    return section[key]


def _fixed_number(value: Any, expected: float, path: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise Stage4ConfigError("incorrect_type", path)
    if value != expected:
        raise Stage4ConfigError("fixed_value_deviation", path)
    return float(value)


def _positive_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise Stage4ConfigError("incorrect_type", path)
    if value < 1:
        raise Stage4ConfigError("below_minimum", path)
    return value


def parse_language_scent_config(root: Any) -> LanguageScentConfig:
    data = _object(root, "$" )
    pheromones = _object(_required(data, "pheromones", "$"), "pheromones")
    world = _object(_required(data, "world", "$"), "world")
    league = _object(
        _required(data, "network_and_league", "$"), "network_and_league"
    )
    area = _required(world, "map_area", "world")
    if not isinstance(area, str):
        raise Stage4ConfigError("incorrect_type", "world.map_area")
    return LanguageScentConfig(
        _fixed_number(
            _required(pheromones, "pheromone_center_intensity", "pheromones"),
            0.9,
            "pheromones.pheromone_center_intensity",
        ),
        _fixed_number(
            _required(pheromones, "pheromone_decay", "pheromones"),
            0.10,
            "pheromones.pheromone_decay",
        ),
        int(
            _fixed_number(
                _required(pheromones, "pheromone_grid_size", "pheromones"),
                5,
                "pheromones.pheromone_grid_size",
            )
        ),
        area,
        _positive_int(_required(world, "hint_max_words", "world"), "world.hint_max_words"),
        _positive_int(
            _required(league, "token_budget_per_series", "network_and_league"),
            "network_and_league.token_budget_per_series",
        ),
    )


def load_language_scent_config(path: Path) -> LanguageScentConfig:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise Stage4ConfigError("file_not_found", str(path)) from error
    except OSError as error:
        raise Stage4ConfigError("file_read_error", str(path)) from error
    try:
        return parse_language_scent_config(decode_json(text))
    except DuplicateKeyError as error:
        raise Stage4ConfigError("duplicate_key", error.key) from error
    except ValueError as error:
        if isinstance(error, Stage4ConfigError):
            raise
        raise Stage4ConfigError("malformed_json", "$" ) from error
