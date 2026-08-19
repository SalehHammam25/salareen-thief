"""Gmail API delivery for verified JSON series reports."""

import base64
import json
import time
from collections.abc import Callable
from email.message import EmailMessage
from pathlib import Path
from typing import Any

GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"


class DuplicateSendError(RuntimeError):
    """Raised when an idempotency key has already been delivered."""


class SendRateLimitError(RuntimeError):
    """Raised when reports are submitted too quickly."""


def load_gmail_service(client_path: Path, token_path: Path) -> Any:
    """Load Gmail credentials from caller-selected, ignored external paths."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    scopes = [GMAIL_SEND_SCOPE]
    credentials = None
    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(str(token_path), scopes)
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(client_path), scopes)
        credentials = flow.run_local_server(port=0)
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(credentials.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=credentials, cache_discovery=False)


def build_json_message(
    sender: str, recipient: str, artifact: dict[str, Any]
) -> dict[str, str]:
    """Create the base64url MIME payload expected by Gmail messages.send."""
    message = EmailMessage()
    prefix = "TEST — " if artifact.get("report_type") == "TEST" else ""
    message["Subject"] = prefix + "Salareen verified series report"
    message["From"] = sender
    message["To"] = recipient
    message.set_content("Attached is the verified Salareen series report.")
    payload = json.dumps(artifact, sort_keys=True, indent=2).encode("utf-8")
    message.add_attachment(
        payload,
        maintype="application",
        subtype="json",
        filename="verified-series.json",
    )
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode("ascii")
    return {"raw": encoded}


class GmailReportSender:
    """Rate-limited sender with per-process duplicate protection."""

    def __init__(
        self,
        service: Any,
        minimum_interval: float = 1.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._service = service
        self._minimum_interval = minimum_interval
        self._clock = clock
        self._sent: set[str] = set()
        self._last_sent: float | None = None

    def send(
        self,
        sender: str,
        recipient: str,
        artifact: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        if idempotency_key in self._sent:
            raise DuplicateSendError(idempotency_key)
        now = self._clock()
        if self._last_sent is not None:
            elapsed = now - self._last_sent
            if elapsed < self._minimum_interval:
                raise SendRateLimitError("report submission rate limit exceeded")
        request = (
            self._service.users()
            .messages()
            .send(
                userId="me",
                body=build_json_message(sender, recipient, artifact),
            )
        )
        result = request.execute()
        self._sent.add(idempotency_key)
        self._last_sent = now
        return result
