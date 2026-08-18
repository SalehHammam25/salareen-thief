"""Executable privacy-safe GUI and opt-in Gmail SMTP report sender."""

import json
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from .security.series import privacy_safe_view


def send_gmail_report(recipient: str, artifact: dict[str, Any]) -> None:
    username = os.environ.get("SALAREEN_GMAIL_ADDRESS")
    password = os.environ.get("SALAREEN_GMAIL_APP_PASSWORD")
    if not username or not password:
        raise RuntimeError("Gmail credentials must be supplied through the environment")
    message = EmailMessage()
    message["Subject"] = "Salareen verified series report"
    message["From"], message["To"] = username, recipient
    message.set_content(json.dumps(artifact, sort_keys=True, indent=2))
    with smtplib.SMTP_SSL(
        "smtp.gmail.com", 465, context=ssl.create_default_context()
    ) as smtp:
        smtp.login(username, password)
        smtp.send_message(message)


def run_gui(role: str, artifact_path: str | Path) -> None:
    import tkinter as tk

    artifact = json.loads(Path(artifact_path).read_text(encoding="utf-8"))
    view = privacy_safe_view(
        role, artifact.get("local_position", [0, 0]), artifact.get("public_events", [])
    )
    root = tk.Tk()
    root.title(f"Salareen {role} verified report")
    text = tk.Text(root, width=80, height=30)
    text.insert("1.0", json.dumps(view, sort_keys=True, indent=2))
    text.configure(state="disabled")
    text.pack()
    root.mainloop()
