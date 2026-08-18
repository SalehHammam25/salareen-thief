"""Private ngrok stable-domain configuration tests."""

import pytest

from salareen_thief.cloud_tunneling.ngrok_config import NgrokConfig, load_ngrok_config


def test_config_requires_explicit_port_and_bare_stable_domain() -> None:
    config = load_ngrok_config({"NGROK_DOMAIN": "Stable.Example.Test"}, 8802)
    assert config.public_url == "https://stable.example.test"
    assert "stable.example.test" not in repr(config)
    for domain in ("", "https://random.example.test", "localhost", "bad domain"):
        with pytest.raises(ValueError):
            load_ngrok_config({"NGROK_DOMAIN": domain}, 8802)


@pytest.mark.parametrize(
    "values",
    [
        {"local_port": True, "domain": "stable.example.test"},
        {
            "local_port": 8802,
            "domain": "stable.example.test",
            "readiness_attempts": 0,
        },
        {
            "local_port": 8802,
            "domain": "stable.example.test",
            "readiness_interval": False,
        },
    ],
)
def test_direct_construction_cannot_bypass_validation(values) -> None:
    with pytest.raises(ValueError):
        NgrokConfig(**values)
