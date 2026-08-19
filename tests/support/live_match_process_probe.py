"""Deterministic client probe for two independent localhost peers."""

import asyncio
import json
from typing import Any

from fastmcp import Client

BASE = {
    "protocol_version": "1.0-provisional",
    "game_id": "local-game",
    "session_id": "local-session",
    "game_number": 1,
}
URLS = {"thief": "http://127.0.0.1:8801/mcp", "cop": "http://127.0.0.1:8802/mcp"}


async def call(role: str, tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    async with Client(URLS[role]) as client:
        result = await client.call_tool(tool, {"payload": payload})
    assert isinstance(result.structured_content, dict)
    return result.structured_content


def message(sender: str, correlation: str, **fields: Any) -> dict[str, Any]:
    return {**BASE, "sender_role": sender, "correlation_id": correlation, **fields}


async def run() -> None:
    for receiver, sender in (("cop", "thief"), ("thief", "cop")):
        result = await call(
            receiver,
            "initialize_game_v1",
            message(
                sender,
                f"init-{sender}",
                config_schema_version="3.0.0",
                starting_role="thief",
            ),
        )
        assert result["accepted"]
    applied = {"cop": 0, "thief": 0}
    for turn in range(4):
        sender = "thief" if turn % 2 == 0 else "cop"
        receiver = "cop" if sender == "thief" else "thief"
        intent = message(
            sender,
            f"action-{turn}",
            turn_index=turn,
            action_kind="stay",
            direction="STAY",
            x=None,
            y=None,
        )
        first = await call(receiver, "submit_action_v1", intent)
        assert first == await call(receiver, "submit_action_v1", intent)
        applied[receiver] += 1
        acknowledgement = message(
            receiver,
            f"ack-{turn}",
            turn_index=turn,
            action_correlation_id=f"action-{turn}",
            result="applied",
            result_code="OK",
            next_turn_index=turn + 1,
            next_role=receiver,
        )
        assert (await call(sender, "acknowledge_action_v1", acknowledgement))[
            "accepted"
        ]
    for receiver, sender in (("cop", "thief"), ("thief", "cop")):
        terminal = message(
            sender,
            f"terminal-{sender}",
            turn_index=4,
            outcome="cop_capture",
            winner_role="cop",
            loser_role="thief",
            attribution="none",
            reason_code="cooccupancy",
        )
        assert (await call(receiver, "reconcile_terminal_v1", terminal))["accepted"]
        score = message(
            sender,
            f"score-{sender}",
            turn_index=4,
            outcome="cop_capture",
            cop_score=20,
            thief_score=5,
        )
        assert (await call(receiver, "reconcile_score_v1", score))["accepted"]
        stop = message(
            sender,
            f"stop-{sender}",
            turn_index=4,
            mode="terminal",
            reason_code="complete",
        )
        assert (await call(receiver, "shutdown_match_v1", stop))["accepted"]
    print(
        json.dumps(
            {
                "turns": 4,
                "applied": applied,
                "outcome": "cop_capture",
                "scores": {"cop": 20, "thief": 5},
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    asyncio.run(run())
