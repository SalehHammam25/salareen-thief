"""Read-only privacy-safe live status dashboard."""

import json

from .gui_view import load_view


def run_gui(
    role: str, artifact_path: str, config_path: str = "config/game.json"
) -> None:
    import tkinter as tk

    view = load_view(role, artifact_path, config_path)
    root = tk.Tk()
    root.title(f"Salareen {role.title()} — Local View")
    root.geometry("720x740")
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

    canvas = tk.Canvas(root, width=420, height=420, bg="#182630", highlightthickness=0)
    canvas.pack(padx=20, pady=8)
    _draw_heatmap(canvas, view["belief_heatmap"], view["board_size"], 420)

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


def _draw_heatmap(canvas, values, board_size, extent):
    cell_size = extent / board_size
    maximum = max(max(float(value) for value in row) for row in values) or 1.0
    for row_index in range(board_size):
        for column_index in range(board_size):
            value = values[row_index][column_index]
            intensity = max(0.0, min(1.0, float(value) / maximum))
            red = int(35 + 220 * intensity)
            blue = int(175 - 120 * intensity)
            color = f"#{red:02x}4b{blue:02x}"
            x0, y0 = column_index * cell_size, row_index * cell_size
            canvas.create_rectangle(
                x0,
                y0,
                x0 + cell_size,
                y0 + cell_size,
                fill=color,
                outline="#101820",
            )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("role", choices=("cop", "thief"))
    parser.add_argument("artifact")
    parser.add_argument("--config", default="config/game.json")
    arguments = parser.parse_args()
    run_gui(arguments.role, arguments.artifact, arguments.config)


if __name__ == "__main__":
    main()
