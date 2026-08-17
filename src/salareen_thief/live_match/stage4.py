"""Production Stage 4 scent, template-language, and belief choreography."""

from decimal import Decimal
from pathlib import Path
from typing import Any

from salareen_thief.base_logic.state_types import Board
from salareen_thief.belief.models import BeliefFallback, BeliefUpdated
from salareen_thief.belief.prior import uniform_prior
from salareen_thief.belief.updates import update_from_language, update_from_scent
from salareen_thief.language.accounting import TokenLedger
from salareen_thief.language.hints import HINT_VERSION, HintAccepted, validate_hint
from salareen_thief.language.models import FreeLanguageHint, VerbalRequest
from salareen_thief.language.private_config import load_private_language_config
from salareen_thief.language.providers import TemplateProvider
from salareen_thief.language.service import VerbalService
from salareen_thief.scent.config import load_language_scent_config
from salareen_thief.scent.models import ScentGrid


class Stage4Boundary:
    def __init__(self, shared_path: Path, board: Board,
                 private_path: Path | None = None) -> None:
        shared = load_language_scent_config(shared_path)
        private = load_private_language_config(private_path or Path(".private.toml"))
        self.max_words = shared.hint_max_words
        self.reliability = private.reliability
        self.ledger = TokenLedger(shared.token_budget_per_series)
        self.belief = uniform_prior(board)
        self.service = VerbalService(
            TemplateProvider(), private.every_n_steps, private.timeout_seconds)
        self.last_scent_turn = -1
        self.last_hint_turn = -1

    async def outbound(self, game_id: str, turn: int, scent: ScentGrid) -> tuple[
        dict[str, Any], dict[str, Any] | None
    ]:
        values = [[str(value) for value in row] for row in scent.values]
        scent_payload = {"axis_start_index": scent.axis_start_index,
                         "width": len(values), "height": len(values),
                         "values": values}
        request = VerbalRequest(game_id, turn, "New York", "qualitative movement")
        result = await self.service.generate(request, self.ledger, self.max_words)
        self.ledger = result.ledger
        hint = None if result.hint is None else {
            "text": result.hint.text, "word_count": len(result.hint.text.split())}
        return scent_payload, hint

    def receive_scent(self, turn: int, payload: dict[str, Any]) -> bool:
        try:
            grid = ScentGrid(payload["axis_start_index"], tuple(
                tuple(Decimal(value) for value in row) for row in payload["values"]))
        except (KeyError, TypeError, ValueError):
            return False
        result = update_from_scent(self.belief, grid)
        if isinstance(result, BeliefFallback):
            self.last_scent_turn = turn
            return True
        if not isinstance(result, BeliefUpdated):
            return False
        self.belief, self.last_scent_turn = result.belief, turn
        return True

    def receive_hint(self, turn: int, text: str) -> bool:
        if turn != self.last_scent_turn:
            return False
        checked = validate_hint(
            FreeLanguageHint(HINT_VERSION, "live-match", text), self.max_words)
        if not isinstance(checked, HintAccepted):
            return False
        result = update_from_language(self.belief, text, self.reliability)
        if not isinstance(result, BeliefUpdated):
            return False
        self.belief = result.belief
        self.last_hint_turn = turn
        return True
