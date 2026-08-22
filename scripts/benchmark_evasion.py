"""Small deterministic thief benchmark: legacy corner-seeking versus evasion."""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from salareen_thief.evasion.fallback import corner_choice  # noqa: E402
from salareen_thief.official.engine import ThiefEngine  # noqa: E402
from salareen_thief.official.terms import TERMS  # noqa: E402
from salareen_thief.official.wire import clean_turn  # noqa: E402

DELTAS = ((-1, 0), (1, 0), (0, 1), (0, -1))
STEPS = TERMS["max_steps"]


class LegacyThief(ThiefEngine):
    """Reproduce the pre-change corner-seeking decision rule exactly."""

    def _choice(self) -> str:
        return corner_choice(
            self.board, self.position, frozenset(self.barriers), self.last_threat
        )


def legal(cell):
    return [
        (cell[0] + dr, cell[1] + dc)
        for dr, dc in DELTAS
        if 0 <= cell[0] + dr < 7 and 0 <= cell[1] + dc < 7
    ]


def distance(left, right):
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def stationary(pos, foe, rng):
    return pos


def chase(pos, foe, rng):
    return min([pos, *legal(pos)], key=lambda c: (distance(c, foe), c[0], c[1]))


def random_legal(pos, foe, rng):
    return rng.choice([pos, *legal(pos)])


def mobility(pos, foe, rng):
    options = [pos, *legal(pos)]
    return min(options, key=lambda c: (distance(c, foe), -len(legal(c)), c[0], c[1]))


POLICE = {
    "stationary": stationary,
    "direct_chase": chase,
    "random_legal": random_legal,
    "mobility_max": mobility,
}


def rings(pos):
    grid = {}
    for row in range(7):
        for col in range(7):
            ring = max(abs(row - pos[0]), abs(col - pos[1]))
            if ring < 3:
                grid[f"{row},{col}"] = (0.9, 0.6, 0.3)[ring]
    return grid


def message(step, police, claim=True):
    return clean_turn(
        {
            "step": step,
            "sender": "police",
            "commit": f"{step:064x}",
            "hint": "",
            "smell_grid": rings(police),
            "timestamp": "",
            "barrier_placed": None,
            "capture_claim": list(police) if claim else None,
            "claim_response": None,
            "win_claim": None,
        }
    )


def play(factory, police_move, seed, claim=True):
    """Run one deterministic episode; return the capture step or None."""
    engine = factory(1, "1" * 40)
    rng = random.Random(seed)
    police = tuple(TERMS["cop_start"])
    incoming = None
    for step in range(1, STEPS + 1):
        engine.take_turn(incoming)
        thief = (engine.position.row, engine.position.col)
        if thief == police:
            return step
        police = police_move(police, thief, rng)
        if police == thief:
            return step
        incoming = message(step, police, claim)
        if engine.receive(incoming).caught:
            return step
    return None


def main() -> int:
    seeds = tuple(range(20))
    print(f"{'police / peer info':<30}{'legacy':>20}{'evasion':>20}")
    modes = ((True, "claim+scent"), (False, "scent only"))
    for name, move in POLICE.items():
        for claim, label in modes:
            print("".join(_row(name, label, move, claim, seeds)))
    return 0


def _row(name, label, move, claim, seeds):
    row = [f"{name} / {label}".ljust(30)]
    for factory in (LegacyThief, ThiefEngine):
        results = [play(factory, move, seed, claim) for seed in seeds]
        caught = [value for value in results if value is not None]
        rate = 100 * (len(results) - len(caught)) / len(results)
        mean = sum(caught) / len(caught) if caught else None
        shown = "-" if mean is None else f"{mean:.1f}"
        row.append(f"{rate:5.0f}% surv  cap={shown}".rjust(20))
    return row


if __name__ == "__main__":
    raise SystemExit(main())
