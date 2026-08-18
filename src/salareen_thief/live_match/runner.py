"""Independent thief live-match server process entry point."""

import argparse
import asyncio
import os
from contextlib import suppress

from .autoplay import run_autoplay
from .endpoints import validate_endpoint
from .event_log import EventLog
from .gameplay import GameplayAdapter
from .journal import Journal
from .security_runtime import LiveSecurity
from .server import build_live_server
from .session import LiveMatchSession


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8801, type=int)
    parser.add_argument("--game-id", default="local-game")
    parser.add_argument("--session-id", default="local-session")
    parser.add_argument("--config", default="config/game.json")
    parser.add_argument("--opponent")
    parser.add_argument(
        "--scenario",
        choices=(
            "capture",
            "barrier_capture",
            "trapped",
            "capture_priority",
            "survival",
        ),
        default="capture",
    )
    args = parser.parse_args()
    if args.opponent:
        validate_endpoint(
            args.opponent, mode="local", host="127.0.0.1", permitted_port=8802
        )
    path = os.environ.get("SALAREEN_THIEF_JOURNAL", ".runtime/thief-match.sqlite3")
    log_path = os.environ.get("SALAREEN_THIEF_EVENT_LOG", ".runtime/thief-match.jsonl")
    journal = Journal(path)
    events = EventLog(log_path, "thief", args.game_id, args.session_id)
    saved = journal.get_state(args.game_id, args.session_id, "game_state")
    security = LiveSecurity("thief", args.config, args.game_id, journal, args.session_id)
    gameplay = GameplayAdapter(args.config, saved, defer=True)
    session = LiveMatchSession(
        "thief", args.game_id, args.session_id, 1, journal, gameplay, security
    )
    session.events = events
    session.action_delay = float(os.environ.get("SALAREEN_ACTION_DELAY", "0"))
    session.crash_after_send = int(os.environ.get("SALAREEN_CRASH_AFTER_SEND", "-1"))
    session.max_retries = int(os.environ.get("SALAREEN_MAX_RETRIES", "3"))
    session.retry_backoff = float(os.environ.get("SALAREEN_RETRY_BACKOFF", "5"))
    session.watchdog_timeout = float(os.environ.get("SALAREEN_WATCHDOG_TIMEOUT", "60"))
    session.response_timeout = float(os.environ.get("SALAREEN_RESPONSE_TIMEOUT", "30"))
    session.recovery_mismatch = os.environ.get("SALAREEN_RECOVERY_MISMATCH", "")
    events.emit("configured", turn=session.turn_index, phase=session.phase)
    pending = journal.get_state(args.game_id, args.session_id, "pending_action")
    if args.opponent and (saved or pending) and session.phase == "game_initialized":
        session.phase = "paused_recovering"
        session._save("phase", session.phase)
    server = build_live_server(session, events)
    events.emit("server_ready", turn=session.turn_index, phase=session.phase)
    if args.opponent is None:
        try:
            server.run(transport="http", host=args.host, port=args.port)
        finally:
            journal.close()
        return

    async def play() -> None:
        task = asyncio.create_task(
            server.run_async(
                transport="http", host=args.host, port=args.port, show_banner=False
            )
        )
        try:
            await run_autoplay(args.opponent, session, args.scenario)
        finally:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
            journal.close()

    asyncio.run(play())


if __name__ == "__main__":
    main()
