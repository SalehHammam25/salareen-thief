"""Private provider configuration boundary tests."""

from pathlib import Path

import pytest

from salareen_thief.language.models import ProviderMode
from salareen_thief.language.private_config import load_private_language_config


def test_missing_private_config_uses_zero_token_template(tmp_path: Path) -> None:
    config = load_private_language_config(tmp_path / "game.toml")
    assert config.provider is ProviderMode.TEMPLATE
    assert (config.every_n_steps, config.timeout_seconds) == (1, 10.0)


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
