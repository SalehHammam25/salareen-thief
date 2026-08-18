"""Bounded waiting for the mandatory Stage 4 turn boundary."""

import asyncio
import time

from .recovery import abort
from .session import LiveMatchSession


def ready(session: LiveMatchSession) -> bool:
    stage4 = session.gameplay.stage4
    turn = session.turn_index
    return stage4.last_scent_turn == turn and (
        not stage4.requires_hint(turn) or stage4.last_hint_turn == turn
    )


async def wait_boundary(session: LiveMatchSession) -> None:
    started = time.monotonic()
    epoch = session.recovery_epoch
    paused = False
    while session.turn_index and not ready(session):
        elapsed = time.monotonic() - started
        if (
            elapsed >= session.response_timeout
            and session.phase == "game_initialized"
            and session.recovery_epoch == epoch
        ):
            session.phase = "paused_recovering"
            session._save("phase", session.phase)
            session.events.emit("paused", turn=session.turn_index, phase=session.phase)
            paused = True
        if elapsed >= max(session.watchdog_timeout, session.response_timeout):
            abort(
                session, "stage4_boundary_expired", f"action-{session.turn_index - 1}"
            )
            raise RuntimeError("Stage 4 boundary watchdog expired")
        await asyncio.sleep(0.02)
    if (
        paused
        and session.phase == "paused_recovering"
        and session.recovery_epoch == epoch
    ):
        session.phase = "game_initialized"
        session._save("phase", session.phase)
