"""Official wire engine backed by Salareen's existing Thief policy."""

import secrets
from dataclasses import dataclass
from datetime import UTC, datetime

from salareen_thief.base_logic.state_types import Board, Coordinate
from salareen_thief.evasion.fallback import corner_choice
from salareen_thief.evasion.observer import PoliceObserver
from salareen_thief.evasion.policy import EvasionPolicy

from .terms import TERMS, commit_of

DELTAS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1), "STAY": (0, 0)}


@dataclass(frozen=True)
class IncomingOutcome:
    won: bool = False
    caught: bool = False
    opponent_won: bool = False


class ThiefEngine:
    role = "thief"

    def __init__(self, sub_game: int, git_commit: str) -> None:
        self.sub_game = sub_game
        self.git_commit = git_commit
        self.board = Board(7, 0, "top-left")
        self.position = Coordinate(*TERMS["thief_start"])
        self.barriers: set[Coordinate] = set()
        self.step = 0
        self.records: list[dict] = []
        self.pending_response: dict | None = None
        self.caught = False
        self.last_threat = Coordinate(*TERMS["cop_start"])
        self.observer = PoliceObserver(self.board, self.last_threat)
        self.evasion = EvasionPolicy(self.board)
        self.history: list[Coordinate] = [self.position]
        self._record("STAY", "initial", None)

    def _choice(self) -> str:
        barriers = frozenset(self.barriers)
        try:
            return self.evasion.choose(
                self.position, barriers, self.observer.estimate, self.history
            )
        except Exception:
            return corner_choice(
                self.board, self.position, barriers, self.last_threat
            )

    def _apply_move(self, choice: str) -> None:
        row, col = DELTAS.get(choice, (0, 0))
        target = Coordinate(self.position.row + row, self.position.col + col)
        if self.board.contains(target) and target not in self.barriers:
            self.position = target

    def _trapped(self) -> bool:
        for row, col in DELTAS.values():
            if row == col == 0:
                continue
            cell = Coordinate(self.position.row + row, self.position.col + col)
            if self.board.contains(cell) and cell not in self.barriers:
                return False
        return True

    def _scent(self) -> dict[str, float]:
        rings = (0.9, 0.6, 0.3)
        result = {}
        for row in range(7):
            for col in range(7):
                distance = max(abs(row - self.position.row), abs(col - self.position.col))
                if distance < len(rings):
                    result[f"{row},{col}"] = rings[distance]
        return result

    def _record(self, move: str, intent: str, response: dict | None) -> dict:
        payload = {
            "claim_response": response,
            "hint": "",
            "intent": intent,
            "move": move,
            "position": [self.position.row, self.position.col],
            "role": self.role,
            "state": "caught" if self.caught else "ok",
            "step": self.step,
            "sub_game": self.sub_game,
        }
        nonce = secrets.token_hex(16)
        record = {"payload": payload, "nonce": nonce, "commit": commit_of(payload, nonce)}
        self.records.append(record)
        return record

    def receive(self, message: dict) -> IncomingOutcome:
        self.observer.update(message)
        barrier = message.get("barrier_placed")
        if barrier is not None:
            self.barriers.add(Coordinate(*barrier))
        claim = message.get("capture_claim")
        if claim is not None:
            self.last_threat = Coordinate(*claim)
            caught = claim == [self.position.row, self.position.col]
            caught = caught or barrier == [self.position.row, self.position.col]
            caught = caught or self._trapped()
            self.pending_response = {"claim": list(claim), "caught": caught}
            self.caught = caught
        return IncomingOutcome(caught=self.caught, opponent_won=bool(message.get("win_claim")))

    def take_turn(self, incoming: dict | None = None, *, hold: bool = False) -> dict:
        self.step += 1
        choice = "STAY" if hold or self.caught else self._choice()
        self._apply_move(choice)
        self.history.append(self.position)
        response = self.pending_response
        record = self._record(
            "STAY" if choice == "STAY" else f"MOVE:{choice}",
            "hold after capture" if hold or self.caught else "evade threat",
            response,
        )
        self.pending_response = None
        survived = not self.caught and self.step >= TERMS["max_steps"]
        return {
            "step": self.step,
            "sender": self.role,
            "commit": record["commit"],
            "hint": "",
            "smell_grid": self._scent(),
            "timestamp": datetime.now(UTC).isoformat(),
            "barrier_placed": None,
            "capture_claim": None,
            "claim_response": response,
            "win_claim": {"type": "survival"} if survived else None,
        }
