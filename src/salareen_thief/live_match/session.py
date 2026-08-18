import json
from typing import Any

from . import protocol
from .journal import Journal
from .outbound import prepare


class LiveMatchSession:
    def __init__(self, local_role: str, game_id: str, session_id: str,
                 game_number: int, journal: Journal, gameplay: Any = None) -> None:
        if local_role not in protocol.ROLES:
            raise ValueError("invalid local role")
        self.local_role = local_role
        self.remote_role = "thief" if local_role == "cop" else "cop"
        self.game_id, self.session_id = game_id, session_id
        self.game_number, self.journal = game_number, journal
        self.gameplay = gameplay
        self.phase = journal.get_state(game_id, session_id, "phase") or "configured"
        self.turn_index = int(journal.get_state(game_id, session_id, "turn") or 0)
        self.applied_actions = int(journal.get_state(game_id, session_id, "applied") or 0)
        self.recovery_epoch = 0
    def prepare_local(self, payload: dict[str, Any]) -> dict[str, Any]:
        return prepare(self, payload)
    def handle(self, tool: str, payload: Any) -> dict[str, Any]:
        correlation = payload.get("correlation_id") if type(payload) is dict else None
        issue = protocol.validate_shape(tool, payload)
        if issue:
            return self._reject(correlation, *issue)
        assert isinstance(payload, dict)
        issue = self._validate_identity(tool, payload)
        if issue:
            if tool == "resume_match_v1":
                self.phase = "aborted"
                self._save("phase", self.phase)
            return self._reject(correlation, *issue)
        key = (self.game_id, self.session_id, tool, correlation)
        request = protocol.canonical(payload)
        cached = self.journal.lookup(key)
        if cached:
            return json.loads(cached[1]) if cached[0] == request else self._reject(
                correlation, "DUPLICATE_MISMATCH", "correlation_id")
        issue = self._validate_semantics(tool, payload)
        if issue:
            return self._reject(correlation, *issue)
        response = {"accepted": True, "correlation_id": correlation,
                    "status": protocol.STATUSES[tool]}
        self._mutate(tool, payload)
        self.journal.record(key, self._boundary(tool), request,
                            protocol.canonical(response))
        return response
    def _validate_identity(self, tool: str, payload: dict[str, Any]):
        if payload["protocol_version"] != protocol.VERSION:
            return "UNSUPPORTED_VERSION", "protocol_version"
        if not protocol.ID_PATTERN.fullmatch(payload["correlation_id"]):
            return "INVALID_CORRELATION_ID", "correlation_id"
        role = payload["sender_role"]
        if role not in protocol.ROLES:
            return "INVALID_ROLE", "sender_role"
        if role != self.remote_role:
            return "WRONG_EXPECTED_ROLE", "sender_role"
        if payload["game_id"] != self.game_id or payload["session_id"] != self.session_id:
            return "IDENTITY_MISMATCH", "match"
        if tool != "resume_match_v1" and payload["game_number"] != self.game_number:
            return "INVALID_GAME_NUMBER", "game_number"
        return None
    def _validate_semantics(self, tool: str, payload: dict[str, Any]):
        if tool == "initialize_game_v1":
            if self.phase not in {"configured", "game_initialized"}:
                return "ILLEGAL_PHASE", "phase"
            if payload["starting_role"] != "thief":
                return "INVALID_ROLE", "starting_role"
            return None
        if tool == "resume_match_v1":
            received = self.journal.get_state(self.game_id, self.session_id,
                                              "last_received_turn")
            pending_ack = received is not None and payload["turn_index"] == int(received)
            exact = payload["turn_index"] == self.turn_index
            if (not exact and not pending_ack) or payload["phase"] != self.phase:
                self._save("phase", "aborted")
                self.phase = "aborted"
                return "IDENTITY_MISMATCH", "recovery_identity"
            return None
        if payload["turn_index"] != self.turn_index:
            return "INVALID_TURN", "turn_index"
        allowed = {"reconcile_terminal_v1", "reconcile_score_v1", "shutdown_match_v1"}
        if self.phase in {"terminal", "shutdown"} and tool not in allowed:
            return "EPISODE_TERMINAL", "phase"
        if tool == "submit_action_v1":
            issue = protocol.validate_action(payload, self.turn_index)
            return issue or (self.gameplay and self.gameplay.validate_payload(payload))
        if tool == "submit_capture_claim_v1" and self.gameplay:
            return self.gameplay.capture(payload, apply=False)
        if tool == "reconcile_score_v1":
            scores = {"cop_capture": (20, 5), "thief_survival": (5, 10),
                      "tie": (2, 2), "technical_loss": (0, 0)}
            if scores.get(payload["outcome"]) != (payload["cop_score"], payload["thief_score"]):
                return "SCORE_MISMATCH", "scores"
        return None
    def _mutate(self, tool: str, payload: dict[str, Any]) -> None:
        if tool == "initialize_game_v1":
            self.phase = "game_initialized"
            self._save("phase", self.phase)
        elif tool == "submit_action_v1":
            if self.gameplay:
                accepted, _ = self.gameplay.apply_payload(payload)
                assert accepted
                self._save("game_state", self.gameplay.snapshot())
            self.applied_actions += 1
            self._save("applied", str(self.applied_actions))
            self.turn_index += 1
            self._save("turn", str(self.turn_index))
            self._save("last_received_turn", str(payload["turn_index"]))
        elif tool == "acknowledge_action_v1" and payload["result"] != "rejected":
            pending = self.journal.get_state(self.game_id, self.session_id,
                                             "pending_action")
            if pending and self.gameplay:
                action = json.loads(pending)
                assert action["correlation_id"] == payload["action_correlation_id"]
                assert self.gameplay.apply_payload(action)[0]
                self._save("game_state", self.gameplay.snapshot())
                self._save("pending_action", "")
            self.turn_index = payload["next_turn_index"]
            self._save("turn", str(self.turn_index))
        elif tool == "reconcile_terminal_v1":
            self.phase = "terminal"
            self._save("phase", self.phase)
        elif tool == "resume_match_v1":
            self.recovery_epoch += 1
            self.phase = "game_initialized"
            self._save("phase", self.phase)
        elif tool == "submit_capture_claim_v1" and self.gameplay:
            assert self.gameplay.capture(payload, apply=True) is None
            self._save("game_state", self.gameplay.snapshot())
        elif tool == "shutdown_match_v1":
            self.phase = "shutdown"
            self._save("phase", self.phase)
    def _save(self, name: str, value: str) -> None:
        self.journal.set_state(self.game_id, self.session_id, name, value)
    @staticmethod
    def _boundary(tool: str) -> str:
        return "received" if tool != "acknowledge_action_v1" else "acknowledged"
    @staticmethod
    def _reject(correlation: Any, code: str, detail: str) -> dict[str, Any]:
        return {"accepted": False, "correlation_id": correlation,
                "code": code, "detail": detail}
