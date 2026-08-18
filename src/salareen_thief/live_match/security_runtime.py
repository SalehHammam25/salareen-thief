import base64
import binascii
import json
import os
import platform
import subprocess
from pathlib import Path
from typing import Any
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from salareen_thief.security.protocol import (
    AppendOnlyAuditLog,
    CommitReveal,
    SecurityViolation,
    canonical_bytes,
    commitment,
    fresh_nonce,
    require_identical_config,
    sign,
    validate_step0,
    verify,
)
class LiveSecurity:
    def __init__(self, role: str, config_path: str | Path, game_id: str, journal: Any = None, session_id: str = "") -> None:
        self.role, self.game_id = role, game_id; raw = Path(config_path).read_text(encoding="utf-8")
        self.config = canonical_bytes(json.loads(raw))
        self.key = Ed25519PrivateKey.generate()
        self.public = self.key.public_key()
        self.step0 = self._step0()
        validate_step0(self.step0)
        self.peer_verified = False
        self.incoming: dict[str, CommitReveal] = {}
        self.outgoing: dict[str, tuple[CommitReveal, bytes]] = {}
        self.audit = AppendOnlyAuditLog()
        self.journal, self.session_id = journal, session_id
        self._restore_outgoing()
        self._restore_incoming()
    def _restore_incoming(self) -> None:
        if not self.journal: return
        raw = self.journal.get_state(self.game_id, self.session_id, "security_incoming")
        for correlation, item in json.loads(raw or "{}").items():
            machine = CommitReveal(); machine.commit(item["digest"]); machine.acknowledge()
            if item.get("action") is not None: machine.reveal(item["action"])
            self.incoming[correlation] = machine
    def _persist_incoming(self) -> None:
        if not self.journal: return
        data = {key: {"digest": value.digest, "action": value.payload}
                for key, value in self.incoming.items()}
        self.journal.set_state(self.game_id, self.session_id, "security_incoming",
            json.dumps(data, sort_keys=True, separators=(",", ":")))
    def _restore_outgoing(self) -> None:
        if not self.journal: return
        raw = self.journal.get_state(self.game_id, self.session_id, "security_outgoing")
        for correlation, item in json.loads(raw or "{}").items():
            machine = CommitReveal(); machine.commit(item["digest"])
            if item["phase"] == "revealed":
                machine.acknowledge(); machine.reveal(item["action"])
            self.outgoing[correlation] = (machine, base64.b64decode(item["nonce"]))
    def _persist_outgoing(self) -> None:
        if not self.journal: return
        data = {key: {"digest": machine.digest, "phase": machine.phase,
            "action": machine.payload, "nonce": base64.b64encode(nonce).decode("ascii")}
            for key, (machine, nonce) in self.outgoing.items()}
        self.journal.set_state(self.game_id, self.session_id, "security_outgoing",
                               json.dumps(data, sort_keys=True, separators=(",", ":")))
    def _step0(self) -> dict[str, Any]:
        commit = os.environ.get("SALAREEN_GIT_COMMIT") or subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True).strip()
        return {"protocol_version": "1.0", "role": self.role, "team": "salareen",
            "model": os.environ.get("SALAREEN_MODEL", "deterministic"),
            "provider": os.environ.get("SALAREEN_PROVIDER", "local"),
            "os": platform.system(), "cpu_cores": os.cpu_count() or 1,
            "cpu_frequency_mhz": 0, "ram_bytes": 0, "gpu": "undisclosed",
            "vram_bytes": 0, "game_count": 6, "git_commit": commit,
            "token_budget": 0, "token_usage": 0}
    def bundle(self) -> dict[str, Any]:
        public = self.public.public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )
        body = {
            "config": base64.b64encode(self.config).decode("ascii"),
            "step0": self.step0,
            "public_key": base64.b64encode(public).decode("ascii"),
        }
        return {
            **body,
            "config_signature": sign(self.key, {"config": body["config"]}),
            "step0_signature": sign(self.key, self.step0),
        }
    def accept_bundle(self, bundle: dict[str, Any]) -> None:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        try:
            public_raw = base64.b64decode(bundle["public_key"], validate=True)
            peer_config = base64.b64decode(bundle["config"], validate=True)
            public = Ed25519PublicKey.from_public_bytes(public_raw)
        except (KeyError, ValueError, binascii.Error) as exc:
            raise SecurityViolation("malformed security bootstrap") from exc
        require_identical_config(self.config, peer_config)
        validate_step0(bundle["step0"])
        if bundle["step0"]["role"] == self.role:
            raise SecurityViolation("peer role must differ")
        verify(public, {"config": bundle["config"]}, bundle["config_signature"])
        verify(public, bundle["step0"], bundle["step0_signature"])
        self.peer_verified = True
        self.audit.append("bootstrap", {"peer_role": bundle["step0"]["role"]})
    def prepare(self, correlation: str, action: dict[str, Any]) -> str:
        if correlation in self.outgoing:
            machine, _ = self.outgoing[correlation]
            return str(machine.digest)
        nonce = fresh_nonce()
        digest = commitment(action, nonce)
        machine = CommitReveal()
        machine.commit(digest)
        self.outgoing[correlation] = (machine, nonce)
        self._persist_outgoing()
        self.audit.append("commit", {"correlation_id": correlation, "digest": digest})
        return digest
    def acknowledge_outgoing(self, correlation: str, action: dict[str, Any]) -> None:
        machine, _ = self.outgoing[correlation]
        if machine.phase == "revealed": return
        machine.acknowledge()
        machine.reveal(action)
        self._persist_outgoing()
        self.audit.append("reveal", {"correlation_id": correlation, "payload": action})
    def accept_commit(self, correlation: str, digest: str) -> None:
        machine = CommitReveal()
        machine.commit(digest)
        machine.acknowledge()
        self.incoming[correlation] = machine
        self._persist_incoming()
        self.audit.append(
            "commit_acknowledged", {"correlation_id": correlation, "digest": digest}
        )
    def accept_reveal(self, correlation: str, action: dict[str, Any]) -> None:
        self.incoming[correlation].reveal(action)
        self._persist_incoming()
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
            self.incoming[correlation].audit(base64.b64decode(encoded, validate=True))
        self.audit.verify()
