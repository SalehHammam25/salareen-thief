"""Stage 4 configuration and opponent-scent value tests."""

import json
from dataclasses import FrozenInstanceError
from decimal import Decimal
from pathlib import Path

import pytest

from salareen_thief.scent.config import (
    Stage4ConfigError,
    load_language_scent_config,
    parse_language_scent_config,
)
from salareen_thief.scent.models import OpponentScent, ScentGrid


def valid_config() -> dict[str, object]:
    return {
        "pheromones": {
            "pheromone_center_intensity": 0.9,
            "pheromone_decay": 0.10,
            "pheromone_grid_size": 5,
        },
        "world": {"map_area": "New York", "hint_max_words": 15},
        "network_and_league": {"token_budget_per_series": 200000},
    }


def test_committed_shared_config_loads_stage4_subset() -> None:
    config = load_language_scent_config(Path("config/game.json"))
    assert config.center_intensity == Decimal("0.9")
    assert config.decay_rate == Decimal("0.10")
    assert config.field_size == 5
    assert (config.map_area, config.hint_max_words) == ("New York", 15)
    assert config.token_budget_per_series == 200000


@pytest.mark.parametrize(
    "key,value,category",
    [
        ("pheromone_center_intensity", 0.8, "fixed_value_deviation"),
        ("pheromone_decay", True, "incorrect_type"),
        ("pheromone_grid_size", False, "incorrect_type"),
        ("pheromone_grid_size", 7, "fixed_value_deviation"),
    ],
)
def test_fixed_scent_values_reject_deviations_and_bools(
    key: str, value: object, category: str
) -> None:
    root = valid_config()
    root["pheromones"][key] = value  # type: ignore[index]
    with pytest.raises(Stage4ConfigError) as caught:
        parse_language_scent_config(root)
    assert caught.value.category == category


def test_missing_malformed_and_duplicate_config(tmp_path: Path) -> None:
    with pytest.raises(Stage4ConfigError, match="file_not_found"):
        load_language_scent_config(tmp_path / "missing.json")
    malformed = tmp_path / "bad.json"
    malformed.write_text("{", encoding="utf-8")
    with pytest.raises(Stage4ConfigError, match="malformed_json"):
        load_language_scent_config(malformed)
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"world":{},"world":{}}', encoding="utf-8")
    with pytest.raises(Stage4ConfigError, match="duplicate_key"):
        load_language_scent_config(duplicate)


def test_scent_values_are_frozen_and_validated() -> None:
    grid = ScentGrid(0, ((Decimal("0.0"), Decimal("0.9")),) * 2)
    observation = OpponentScent(2, grid)
    assert observation.grid.values[0][1] == Decimal("0.9")
    with pytest.raises(FrozenInstanceError):
        observation.turn = 3  # type: ignore[misc]
    for invalid in (
        ((Decimal("-0.1"),),),
        ((Decimal("0.91"),),),
        ((Decimal("NaN"),),),
        ((True,),),
        ((),),
    ):
        with pytest.raises(ValueError):
            ScentGrid(0, invalid)


def test_stage4_parser_ignores_unowned_later_sections() -> None:
    root = valid_config()
    root["rate_limiter_gatekeeper"] = {"invalid_later_value": True}
    assert parse_language_scent_config(root).field_size == 5


def test_shared_config_round_trip_is_repeatable() -> None:
    text = json.dumps(valid_config(), sort_keys=True)
    first = parse_language_scent_config(json.loads(text))
    second = parse_language_scent_config(json.loads(text))
    assert first == second
