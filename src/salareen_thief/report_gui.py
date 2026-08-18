"""Executable privacy-safe Tk report viewer."""

import json
from pathlib import Path

from .security.series import privacy_safe_view


def run_gui(role: str, artifact_path: str | Path) -> None:
    import tkinter as tk

    artifact = json.loads(Path(artifact_path).read_text(encoding="utf-8"))
    view = privacy_safe_view(
        role,
        artifact.get("local_position", [0, 0]),
        artifact.get("public_events", []),
    )
    root = tk.Tk()
    root.title(f"Salareen {role} verified report")
    text = tk.Text(root, width=80, height=30)
    text.insert("1.0", json.dumps(view, sort_keys=True, indent=2))
    text.configure(state="disabled")
    text.pack()
    root.mainloop()
