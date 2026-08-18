import asyncio

from .handshake import connect
from .lifecycle import wait_peer_closed
from .reconciliation import capture, finish
from .session import LiveMatchSession
from .stage4_wait import wait_boundary
from .turn_security import local_turn


async def run_autoplay(url: str, session: LiveMatchSession, scenario: str) -> None:
    await connect(url, session)
    while (
        session.gameplay.state.status.value == "active" and session.phase != "aborted"
    ):
        positions = session.gameplay.state.positions
        if positions.cop == positions.thief:
            break
        active = "thief" if session.turn_index % 2 == 0 else "cop"
        if active == session.local_role:
            await wait_boundary(session)
            await asyncio.sleep(getattr(session, "action_delay", 0.0))
            if session.phase == "aborted":
                break
            await local_turn(url, session, scenario)
        else:
            await asyncio.sleep(0.02)
    if session.phase == "aborted":
        return
    if session.local_role == "cop":
        if scenario == "survival":
            await wait_boundary(session)
        if scenario in {"capture", "barrier_capture", "trapped", "capture_priority"}:
            await capture(url, session)
        outcome = "cop_capture" if scenario != "survival" else "thief_survival"
        await finish(url, session, outcome, session.gameplay.score())
    else:
        while session.phase != "shutdown":
            await asyncio.sleep(0.02)
        await wait_peer_closed(url)
