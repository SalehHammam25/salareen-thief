"""Private provider configuration boundary tests."""

from decimal import Decimal
from pathlib import Path

import pytest

from salareen_thief.language.models import ProviderMode
from salareen_thief.language.private_config import load_private_language_config


def test_missing_private_config_uses_zero_token_template(tmp_path: Path) -> None:
    config = load_private_language_config(tmp_path / "game.toml")
    assert config.provider is ProviderMode.TEMPLATE
    assert (config.every_n_steps, config.timeout_seconds) == (1, 10.0)
    assert config.reliability == Decimal("0.75")


@pytest.mark.parametrize("mode", list(ProviderMode))
def test_annex_f_provider_modes_are_private(mode: ProviderMode, tmp_path: Path) -> None:
    path = tmp_path / "game.toml"
    path.write_text(
        f'[trash_talk]\nprovider = "{mode.value}"\nevery_n_steps = 3\n',
        encoding="utf-8",
    )
    config = load_private_language_config(path)
    assert (config.provider, config.every_n_steps) == (mode, 3)


@pytest.mark.parametrize(
    "body", [
        '[trash_talk]\nprovider = "remote_value"\n',
        "[trash_talk]\nevery_n_steps = true\n",
        "[trash_talk]\ntimeout_seconds = 0\n",
    ]
)
def test_invalid_private_provider_configuration_is_rejected(
    body: str, tmp_path: Path
) -> None:
    path = tmp_path / "game.toml"
    path.write_text(body, encoding="utf-8")
    with pytest.raises(ValueError):
        load_private_language_config(path)


def test_shared_json_provider_value_has_no_effect(tmp_path: Path) -> None:
    shared = tmp_path / "game.json"
    shared.write_text('{"trash_talk":{"provider":"claude_api"}}', encoding="utf-8")
    private = load_private_language_config(tmp_path / "game.toml")
    assert private.provider is ProviderMode.TEMPLATE


@pytest.mark.parametrize("value", (0.5, 0.75, 1.0))
def test_private_reliability_accepts_approved_range(value: float, tmp_path: Path) -> None:
    path = tmp_path / "game.toml"
    path.write_text(f"[trash_talk]\nreliability = {value}\n", encoding="utf-8")
    assert load_private_language_config(path).reliability == Decimal(str(value))


@pytest.mark.parametrize("value", (0.49, 1.01, True))
def test_private_reliability_rejects_out_of_range_and_bool(value, tmp_path: Path) -> None:
    literal = str(value).lower()
    path = tmp_path / "game.toml"
    path.write_text(f"[trash_talk]\nreliability = {literal}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_private_language_config(path)
