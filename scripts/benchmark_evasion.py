"""Local thief benchmark: legacy corner-seeking versus deterministic evasion."""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from bench_police import POLICE  # noqa: E402

from salareen_thief.evasion.fallback import corner_choice  # noqa: E402
from salareen_thief.official.engine import ThiefEngine  # noqa: E402
from salareen_thief.official.terms import TERMS  # noqa: E402
from salareen_thief.official.wire import clean_turn  # noqa: E402

STEPS = TERMS["max_steps"]
VARIANTS = (0, 1, 2, 3)
SEEDS = tuple(range(20))
MODES = ((True, "claim+scent"), (False, "scent only"))


class LegacyThief(ThiefEngine):
    """Reproduce the pre-change corner-seeking decision rule exactly."""

    def _choice(self) -> str:
        return corner_choice(
            self.board, self.position, frozenset(self.barriers), self.last_threat
        )


def rings(pos):
    """Build the agreed 5x5 ring emission centred on one cell."""
    grid = {}
    for row in range(7):
        for col in range(7):
            ring = max(abs(row - pos[0]), abs(col - pos[1]))
            if ring < 3:
                grid[f"{row},{col}"] = (0.9, 0.6, 0.3)[ring]
    return grid


def message(step, police, claim):
    """Build one cleaned police turn message in the requested information mode."""
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


def play(factory, police_move, seed, variant, claim):
    """Run one episode; return (capture step or None, transcript)."""
    engine = factory(1, "1" * 40)
    rng = random.Random(seed)
    police = tuple(TERMS["cop_start"])
    incoming, trail = None, []
    for step in range(1, STEPS + 1):
        engine.take_turn(incoming)
        thief = (engine.position.row, engine.position.col)
        trail.append((thief, police))
        if thief == police:
            return step, tuple(trail)
        police = police_move(police, thief, rng, variant)
        trail.append((thief, police))
        if police == thief:
            return step, tuple(trail)
        incoming = message(step, police, claim)
        if engine.receive(incoming).caught:
            return step, tuple(trail)
    return None, tuple(trail)


def scenarios(name):
    """Return the (seed, variant) grid appropriate for one police profile."""
    if name == "random_legal":
        return [(seed, 0) for seed in SEEDS]
    return [(0, variant) for variant in VARIANTS]


def summarise(factory, move, grid, claim):
    """Return survival rate, mean capture step, and distinct-game count."""
    runs = [play(factory, move, s, v, claim) for s, v in grid]
    distinct = {trail for _, trail in runs}
    caught = [step for step, _ in runs if step is not None]
    rate = 100 * (len(runs) - len(caught)) / len(runs)
    mean = f"{sum(caught) / len(caught):.0f}" if caught else "-"
    return rate, mean, len(distinct)


def main() -> int:
    header = f"{'police / peer info':<38}{'distinct':>9}{'legacy':>17}{'evasion':>17}"
    print(header)
    totals = {label: [0.0, 0.0, 0] for _, label in MODES}
    for name, move in POLICE.items():
        grid = scenarios(name)
        for claim, label in MODES:
            legacy = summarise(LegacyThief, move, grid, claim)
            new = summarise(ThiefEngine, move, grid, claim)
            distinct = max(legacy[2], new[2])
            cells = [
                f"{legacy[0]:5.0f}% surv cap={legacy[1]}".rjust(17),
                f"{new[0]:5.0f}% surv cap={new[1]}".rjust(17),
            ]
            print(f"{name + ' / ' + label:<38}{distinct:>9}" + "".join(cells))
            bucket = totals[label]
            bucket[0] += legacy[0]
            bucket[1] += new[0]
            bucket[2] += distinct
    count = len(POLICE)
    for _, label in MODES:
        bucket = totals[label]
        print(
            f"{'AGGREGATE / ' + label:<38}{bucket[2]:>9}"
            f"{bucket[0] / count:16.0f}%{bucket[1] / count:16.0f}%"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
