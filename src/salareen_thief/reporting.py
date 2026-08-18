"""Public report GUI and Gmail API interfaces."""

import os
from pathlib import Path
from typing import Any

from .gmail_reporting import GmailReportSender, load_gmail_service
from .report_gui import run_gui


def send_gmail_report(
    recipient: str,
    artifact: dict[str, Any],
    idempotency_key: str,
) -> dict[str, Any]:
    """Send with OAuth material supplied only through explicit path variables."""
    sender = os.environ.get("SALAREEN_GMAIL_ADDRESS")
    client_value = os.environ.get("SALAREEN_GOOGLE_OAUTH_CLIENT_PATH")
    token_value = os.environ.get("SALAREEN_GOOGLE_OAUTH_TOKEN_PATH")
    if not sender or not client_value or not token_value:
        raise RuntimeError("Gmail address and OAuth paths must be supplied")
    service = load_gmail_service(Path(client_value), Path(token_value))
    return GmailReportSender(service).send(
        sender,
        recipient,
        artifact,
        idempotency_key,
    )


__all__ = ["run_gui", "send_gmail_report"]
