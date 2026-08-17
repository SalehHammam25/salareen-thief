"""Credential-safe Stage 5 configuration and endpoint tests."""

from salareen_thief.cloud_tunneling.config import load_tunnel_config
from salareen_thief.cloud_tunneling.endpoints import (
    redact_endpoint,
    validate_remote_endpoint,
)
from salareen_thief.cloud_tunneling.exchange import (
    EndpointExchange,
    load_opponent_endpoint,
)
from salareen_thief.cloud_tunneling.models import (
    FailureKind,
    TunnelEndpoint,
    TunnelFailure,
)


def test_defaults_match_annex_f_and_hide_credential() -> None:
    config = load_tunnel_config(
        {
            "SALAREEN_TUNNEL_TOKEN": "private-value",
            "SALAREEN_OPPONENT_URL": "https://peer.example.test/?token=hidden",
        }
    )
    assert config.response_timeout_sec == 30
    assert config.watchdog_timeout_sec == 60
    assert config.retry_backoff_sec == 5
    assert config.max_retries == 3
    assert "private-value" not in repr(config)
    assert "hidden" not in repr(config)


def test_private_environment_overrides_are_typed() -> None:
    config = load_tunnel_config(
        {
            "SALAREEN_OPPONENT_URL": "https://cop.example.test/mcp",
        },
        {
            "network_and_league": {
                "response_timeout_sec": 45,
                "watchdog_timeout_sec": 90,
            },
            "rate_limiter_gatekeeper": {
                "retry_backoff_sec": 6,
                "max_retries": 4,
            },
        },
    )
    assert config.opponent_url == "https://cop.example.test/mcp"
    assert (config.response_timeout_sec, config.watchdog_timeout_sec) == (45, 90)
    assert (config.retry_backoff_sec, config.max_retries) == (6, 4)


def test_shared_minimums_and_bool_values_are_enforced() -> None:
    invalid_sections = (
        {"rate_limiter_gatekeeper": {"retry_backoff_sec": 4, "max_retries": 3}},
        {"rate_limiter_gatekeeper": {"retry_backoff_sec": 5, "max_retries": 2}},
        {"network_and_league": {"response_timeout_sec": True}},
    )
    for shared in invalid_sections:
        try:
            load_tunnel_config({}, shared)
        except ValueError:
            continue
        raise AssertionError("invalid shared network value was accepted")


def test_remote_endpoint_requires_safe_public_https() -> None:
    assert validate_remote_endpoint("https://peer.example.test/mcp") == TunnelEndpoint(
        "https://peer.example.test/mcp"
    )
    rejected = (
        "http://peer.example.test",
        "https://localhost:8000/mcp",
        "https://127.0.0.1/mcp",
        "https://user:pass@peer.example.test/mcp",
        "https://peer.example.test/mcp#secret",
    )
    assert all(isinstance(validate_remote_endpoint(value), TunnelFailure) for value in rejected)


def test_endpoint_redaction_removes_userinfo_fragment_and_secret_query() -> None:
    value = "https://user:pass@peer.example.test/mcp?token=hidden&mode=test#fragment"
    redacted = redact_endpoint(value)
    assert redacted == "https://peer.example.test/mcp?token=REDACTED&mode=test"
    assert all(secret not in redacted for secret in ("user", "pass", "hidden", "fragment"))


def test_endpoint_exchange_is_environment_only_and_repeatable() -> None:
    env = {"SALAREEN_OPPONENT_URL": "https://cop.example.test/mcp"}
    first = load_opponent_endpoint(env)
    second = load_opponent_endpoint(env)
    assert first == second
    assert isinstance(first, EndpointExchange)
    assert first.safe_display == env["SALAREEN_OPPONENT_URL"]
    secret = load_opponent_endpoint(
        {"SALAREEN_OPPONENT_URL": "https://cop.example.test/mcp?token=hidden"}
    )
    assert isinstance(secret, TunnelFailure)
    assert secret.kind is FailureKind.CONFIGURATION
