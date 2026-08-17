"""Independent thief live-match server process entry point."""

import argparse
import os

from .journal import Journal
from .server import build_live_server
from .session import LiveMatchSession


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8801, type=int)
    parser.add_argument("--game-id", default="local-game")
    parser.add_argument("--session-id", default="local-session")
    args = parser.parse_args()
    path = os.environ.get("SALAREEN_THIEF_JOURNAL", ".runtime/thief-match.sqlite3")
    journal = Journal(path)
    session = LiveMatchSession("thief", args.game_id, args.session_id, 1, journal)
    try:
        build_live_server(session).run(transport="http", host=args.host, port=args.port)
    finally:
        journal.close()


if __name__ == "__main__":
    main()
