"""Read-only privacy-safe live status dashboard."""

import json
from pathlib import Path

from .security.series import privacy_safe_view


def load_view(role: str, artifact_path: str | Path):
    artifact = json.loads(Path(artifact_path).read_text(encoding="utf-8"))
    return privacy_safe_view(
        role,
        artifact.get("local_position", [0, 0]),
        artifact.get("public_events", []),
        artifact.get("belief_heatmap", []),
        artifact.get("turn_status", "LOCKED"),
    )


def run_gui(role: str, artifact_path: str | Path) -> None:
    import tkinter as tk

    view = load_view(role, artifact_path)
    root = tk.Tk()
    root.title(f"Salareen {role.title()} — Local View")
    root.geometry("720x620")
    root.configure(bg="#101820")

    header = tk.Frame(root, bg="#101820")
    header.pack(fill="x", padx=20, pady=(18, 8))
    tk.Label(
        header,
        text=f"{role.upper()} · LOCAL VIEW",
        bg="#101820",
        fg="#f2f5f7",
        font=("Segoe UI", 18, "bold"),
    ).pack(side="left")
    status = view["turn_status"]
    tk.Label(
        header,
        text=status,
        bg="#167d4a" if status == "YOUR TURN" else "#7a2832",
        fg="white",
        padx=14,
        pady=6,
        font=("Segoe UI", 12, "bold"),
    ).pack(side="right")

    local = view["local_position"]
    tk.Label(
        root,
        text=f"Your position: row {local[0]}, column {local[1]}",
        bg="#101820",
        fg="#b9c7d0",
        font=("Segoe UI", 12),
    ).pack(anchor="w", padx=20, pady=(0, 12))
    tk.Label(
        root,
        text="Opponent-belief heatmap · probability only",
        bg="#101820",
        fg="#f2f5f7",
        font=("Segoe UI", 13, "bold"),
    ).pack(anchor="w", padx=20)

    canvas = tk.Canvas(root, width=480, height=320, bg="#182630", highlightthickness=0)
    canvas.pack(padx=20, pady=8)
    _draw_heatmap(canvas, view["belief_heatmap"], 480, 320)

    tk.Label(
        root,
        text="Public events",
        bg="#101820",
        fg="#f2f5f7",
        font=("Segoe UI", 12, "bold"),
    ).pack(anchor="w", padx=20)
    events = tk.Text(root, width=84, height=7, bg="#182630", fg="#d7e0e5")
    events.insert("1.0", json.dumps(view["public_events"], sort_keys=True, indent=2))
    events.configure(state="disabled")
    events.pack(padx=20, pady=(4, 18))
    root.mainloop()


def _draw_heatmap(canvas, values, width, height):
    if not values or not values[0]:
        canvas.create_text(
            width / 2,
            height / 2,
            text="No belief data",
            fill="#b9c7d0",
            font=("Segoe UI", 12),
        )
        return
    rows, columns = len(values), len(values[0])
    cell_width, cell_height = width / columns, height / rows
    maximum = max(max(float(value) for value in row) for row in values) or 1.0
    for row_index, row in enumerate(values):
        for column_index, value in enumerate(row):
            intensity = max(0.0, min(1.0, float(value) / maximum))
            red = int(35 + 220 * intensity)
            blue = int(175 - 120 * intensity)
            color = f"#{red:02x}4b{blue:02x}"
            x0, y0 = column_index * cell_width, row_index * cell_height
            canvas.create_rectangle(
                x0,
                y0,
                x0 + cell_width,
                y0 + cell_height,
                fill=color,
                outline="#101820",
            )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("role", choices=("cop", "thief"))
    parser.add_argument("artifact")
    arguments = parser.parse_args()
    run_gui(arguments.role, arguments.artifact)


if __name__ == "__main__":
    main()
