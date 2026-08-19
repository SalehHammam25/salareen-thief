"""Focused Gmail OAuth delivery compliance tests."""

import base64
import json
from email import policy
from email.parser import BytesParser
from pathlib import Path

import pytest

from salareen_thief.gmail_reporting import (
    GMAIL_SEND_SCOPE,
    DuplicateSendError,
    GmailReportSender,
    SendRateLimitError,
    build_json_message,
)


class FakeRequest:
    def execute(self):
        return {"id": "message-1"}


class FakeMessages:
    def __init__(self):
        self.calls = []

    def send(self, **kwargs):
        self.calls.append(kwargs)
        return FakeRequest()


class FakeUsers:
    def __init__(self, messages):
        self._messages = messages

    def messages(self):
        return self._messages


class FakeService:
    def __init__(self):
        self.messages_api = FakeMessages()

    def users(self):
        return FakeUsers(self.messages_api)


def test_oauth_uses_only_gmail_send_scope():
    assert GMAIL_SEND_SCOPE == "https://www.googleapis.com/auth/gmail.send"


def test_report_is_a_json_attachment():
    body = build_json_message(
        "sender@example.test",
        "recipient@example.test",
        {"series_id": "series-1", "verified": True},
    )
    raw = base64.urlsafe_b64decode(body["raw"])
    message = BytesParser(policy=policy.default).parsebytes(raw)
    attachment = next(message.iter_attachments())
    assert attachment.get_content_type() == "application/json"
    assert json.loads(attachment.get_content()) == {
        "series_id": "series-1",
        "verified": True,
    }


def test_test_report_is_clearly_labeled():
    body = build_json_message(
        "sender@example.test",
        "sender@example.test",
        {"report_type": "TEST"},
    )
    raw = base64.urlsafe_b64decode(body["raw"])
    message = BytesParser(policy=policy.default).parsebytes(raw)
    assert message["Subject"].startswith("TEST")


def test_duplicate_send_is_rejected():
    service = FakeService()
    sender = GmailReportSender(service, clock=lambda: 10.0)
    sender.send("a@example.test", "b@example.test", {}, "series-1")
    with pytest.raises(DuplicateSendError):
        sender.send("a@example.test", "b@example.test", {}, "series-1")
    assert len(service.messages_api.calls) == 1


def test_send_rate_limit_is_enforced():
    service = FakeService()
    times = iter([10.0, 10.5, 11.1])
    sender = GmailReportSender(service, minimum_interval=1.0, clock=lambda: next(times))
    sender.send("a@example.test", "b@example.test", {}, "series-1")
    with pytest.raises(SendRateLimitError):
        sender.send("a@example.test", "b@example.test", {}, "series-2")
    sender.send("a@example.test", "b@example.test", {}, "series-2")
    assert len(service.messages_api.calls) == 2


def test_oauth_secrets_are_excluded_from_source_and_git_patterns():
    repository = Path(__file__).resolve().parents[1]
    source = (repository / "src" / "salareen_thief" / "reporting.py").read_text()
    gmail_source = (
        repository / "src" / "salareen_thief" / "gmail_reporting.py"
    ).read_text()
    ignore = (repository / ".gitignore").read_text()
    assert "SALAREEN_GMAIL_APP_PASSWORD" not in source + gmail_source
    assert "smtplib" not in source + gmail_source
    for pattern in (".secrets/", "credentials*.json", "oauth*.json", "token*.json"):
        assert pattern in ignore
