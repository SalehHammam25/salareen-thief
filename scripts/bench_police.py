"""Generic deterministic benchmark polices for the local thief benchmark."""

from __future__ import annotations

DELTAS = ((-1, 0), (1, 0), (0, 1), (0, -1))


def legal(cell):
    """Return in-board orthogonal destinations for one cell."""
    return [
        (cell[0] + dr, cell[1] + dc)
        for dr, dc in DELTAS
        if 0 <= cell[0] + dr < 7 and 0 <= cell[1] + dc < 7
    ]


def distance(left, right):
    """Return the orthogonal grid distance between two cells."""
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def _breaker(variant):
    """Return a deterministic secondary ordering for equal-value cells."""
    return (
        (lambda c: (c[0], c[1])),
        (lambda c: (-c[0], -c[1])),
        (lambda c: (c[1], c[0])),
        (lambda c: (-c[1], -c[0])),
    )[variant % 4]


def stationary(pos, foe, rng, variant):
    """Never move."""
    return pos


def distance_min(pos, foe, rng, variant):
    """Greedily minimise distance with a variant tie-break."""
    key = _breaker(variant)
    return min([pos, *legal(pos)], key=lambda c: (distance(c, foe), key(c)))


def predictive_interceptor(pos, foe, rng, variant):
    """Minimise worst-case distance to the thief's next reachable set."""
    key = _breaker(variant)
    ahead = [foe, *legal(foe)]
    return min(
        [pos, *legal(pos)],
        key=lambda c: (max(distance(c, n) for n in ahead), sum(distance(c, n) for n in ahead), key(c)),
    )


def cutoff_chaser(pos, foe, rng, variant):
    """Maximise how many thief options sit within one step of the police."""
    key = _breaker(variant)
    ahead = [foe, *legal(foe)]
    return min(
        [pos, *legal(pos)],
        key=lambda c: (
            -sum(1 for n in ahead if distance(c, n) <= 1),
            distance(c, foe),
            key(c),
        ),
    )


def mobility_reducing(pos, foe, rng, variant):
    """Close in while steering the thief toward low-mobility escape cells."""
    key = _breaker(variant)
    ahead = [foe, *legal(foe)]
    return min(
        [pos, *legal(pos)],
        key=lambda c: (
            distance(c, foe),
            sum(len(legal(n)) for n in ahead if distance(c, n) >= 2),
            key(c),
        ),
    )


def random_legal(pos, foe, rng, variant):
    """Take a uniformly random legal action from a seeded generator."""
    return rng.choice([pos, *legal(pos)])


POLICE = {
    "stationary": stationary,
    "distance_min": distance_min,
    "predictive_interceptor": predictive_interceptor,
    "cutoff_chaser": cutoff_chaser,
    "mobility_reducing": mobility_reducing,
    "random_legal": random_legal,
}
