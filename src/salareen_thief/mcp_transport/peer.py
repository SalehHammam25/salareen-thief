"""Independent peer-process command entry point."""

import argparse

from .server import build_server


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--role", choices=("cop", "thief"), required=True)
    result.add_argument("--session-id", required=True)
    result.add_argument("--port", type=int, required=True)
    result.add_argument("--opponent-url")
    return result


def main() -> None:
    args = parser().parse_args()
    if not 1 <= args.port <= 65535:
        raise SystemExit("port must be between 1 and 65535")
    server, _ = build_server(args.role, args.session_id, args.opponent_url)
    server.run(transport="http", host="127.0.0.1", port=args.port, show_banner=False)


if __name__ == "__main__":
    main()
