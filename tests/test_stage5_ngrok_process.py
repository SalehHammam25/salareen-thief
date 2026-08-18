"""Safe ngrok subprocess argument tests."""

from salareen_thief.cloud_tunneling import ngrok_process


class Process:
    def poll(self):
        return None


def test_start_uses_explicit_domain_and_no_credential_argument(monkeypatch) -> None:
    captured = {}

    def popen(arguments, **options):
        captured["arguments"] = arguments
        captured["options"] = options
        return Process()

    monkeypatch.setattr(ngrok_process.subprocess, "Popen", popen)
    result = ngrok_process.start_ngrok(8802, "https://stable.example.test")
    assert result.running() is True
    assert captured["arguments"] == [
        "ngrok",
        "http",
        "8802",
        "--url",
        "https://stable.example.test",
    ]
    assert all("token" not in value.casefold() for value in captured["arguments"])
    assert captured["options"]["stdout"] is ngrok_process.subprocess.DEVNULL
    assert captured["options"]["stderr"] is ngrok_process.subprocess.DEVNULL
