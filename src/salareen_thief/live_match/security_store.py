import base64
import json
from typing import Any

from salareen_thief.security.protocol import CommitReveal


def restore_incoming(runtime: Any) -> None:
    if not runtime.journal:
        return
    raw = runtime.journal.get_state(
        runtime.game_id, runtime.session_id, "security_incoming"
    )
    for correlation, item in json.loads(raw or "{}").items():
        machine = CommitReveal()
        machine.commit(item["digest"])
        machine.acknowledge()
        if item.get("action") is not None:
            machine.reveal(item["action"])
        runtime.incoming[correlation] = machine


def persist_incoming(runtime: Any) -> None:
    if not runtime.journal:
        return
    data = {
        key: {"digest": value.digest, "action": value.payload}
        for key, value in runtime.incoming.items()
    }
    _save(runtime, "security_incoming", data)


def restore_outgoing(runtime: Any) -> None:
    if not runtime.journal:
        return
    raw = runtime.journal.get_state(
        runtime.game_id, runtime.session_id, "security_outgoing"
    )
    for correlation, item in json.loads(raw or "{}").items():
        machine = CommitReveal()
        machine.commit(item["digest"])
        if item["phase"] == "revealed":
            machine.acknowledge()
            machine.reveal(item["action"])
        nonce = base64.b64decode(item["nonce"])
        runtime.outgoing[correlation] = (machine, nonce)


def persist_outgoing(runtime: Any) -> None:
    if not runtime.journal:
        return
    data = {
        key: {
            "digest": machine.digest,
            "phase": machine.phase,
            "action": machine.payload,
            "nonce": base64.b64encode(nonce).decode("ascii"),
        }
        for key, (machine, nonce) in runtime.outgoing.items()
    }
    _save(runtime, "security_outgoing", data)


def _save(runtime: Any, name: str, data: dict[str, Any]) -> None:
    runtime.journal.set_state(
        runtime.game_id,
        runtime.session_id,
        name,
        json.dumps(data, sort_keys=True, separators=(",", ":")),
    )
