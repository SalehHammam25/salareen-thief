import base64
import json
from pathlib import Path
from typing import Any

from salareen_thief.security.protocol import (
    AppendOnlyAuditLog,
    CommitReveal,
    SecurityViolation,
    canonical_bytes,
    commitment,
    fresh_nonce,
    validate_step0,
)

from .security_identity import accept_bundle, build_bundle, build_step0
from .security_keys import load_expected_peer_key, load_private_key
from .security_store import (
    persist_incoming,
    persist_outgoing,
    restore_incoming,
    restore_outgoing,
)


class LiveSecurity:
    def __init__(
        self,
        role: str,
        config_path: str | Path,
        game_id: str,
        journal: Any = None,
        session_id: str = "",
    ) -> None:
        self.role = role
        self.game_id = game_id
        raw = Path(config_path).read_text(encoding="utf-8")
        self.config = canonical_bytes(json.loads(raw))
        self.key = load_private_key()
        self.public = self.key.public_key()
        self.expected_peer_public = load_expected_peer_key()
        self.step0 = build_step0(role)
        validate_step0(self.step0)
        self.peer_verified = False
        self.incoming: dict[str, CommitReveal] = {}
        self.outgoing: dict[str, tuple[CommitReveal, bytes]] = {}
        self.audit = AppendOnlyAuditLog()
        self.journal = journal
        self.session_id = session_id
        restore_outgoing(self)
        restore_incoming(self)

    def bundle(self) -> dict[str, Any]:
        return build_bundle(self)

    def accept_bundle(self, value: dict[str, Any]) -> None:
        accept_bundle(self, value)

    def prepare(self, correlation: str, action: dict[str, Any]) -> str:
        if correlation in self.outgoing:
            machine, _ = self.outgoing[correlation]
            return str(machine.digest)
        nonce = fresh_nonce()
        digest = commitment(action, nonce)
        machine = CommitReveal()
        machine.commit(digest)
        self.outgoing[correlation] = (machine, nonce)
        persist_outgoing(self)
        self.audit.append("commit", {"correlation_id": correlation, "digest": digest})
        return digest

    def acknowledge_outgoing(self, correlation: str, action: dict[str, Any]) -> None:
        machine, _ = self.outgoing[correlation]
        if machine.phase == "revealed":
            return
        machine.acknowledge()
        machine.reveal(action)
        persist_outgoing(self)
        self.audit.append("reveal", {"correlation_id": correlation, "payload": action})

    def accept_commit(self, correlation: str, digest: str) -> None:
        machine = CommitReveal()
        machine.commit(digest)
        machine.acknowledge()
        self.incoming[correlation] = machine
        persist_incoming(self)
        self.audit.append(
            "commit_acknowledged",
            {"correlation_id": correlation, "digest": digest},
        )

    def accept_reveal(self, correlation: str, action: dict[str, Any]) -> None:
        self.incoming[correlation].reveal(action)
        persist_incoming(self)
        self.audit.append("reveal", {"correlation_id": correlation, "payload": action})

    def nonce_audit(self) -> dict[str, str]:
        result = {}
        for correlation, (machine, nonce) in self.outgoing.items():
            machine.audit(nonce)
            result[correlation] = base64.b64encode(nonce).decode("ascii")
        self.audit.verify()
        return result

    def accept_nonce_audit(self, values: dict[str, str]) -> None:
        if set(values) != set(self.incoming):
            raise SecurityViolation("incomplete final nonce audit")
        for correlation, encoded in values.items():
            nonce = base64.b64decode(encoded, validate=True)
            self.incoming[correlation].audit(nonce)
        self.audit.verify()
