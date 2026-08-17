"""Local/public readiness and ngrok-agent API probes."""

import json
from typing import Any
from urllib.error import HTTPError
from urllib.request import urlopen


def endpoint_reachable(url: str, timeout: float = 2) -> bool:
    try:
        with urlopen(url, timeout=timeout) as response:
            return response.status < 500
    except HTTPError as error:
        return error.code < 500
    except OSError:
        return False


def assigned_urls(api_url: str) -> tuple[str, ...]:
    try:
        with urlopen(api_url, timeout=2) as response:
            payload: Any = json.loads(response.read())
    except (OSError, ValueError, TypeError):
        return ()
    tunnels = payload.get("tunnels", []) if isinstance(payload, dict) else []
    if not isinstance(tunnels, list):
        return ()
    urls = [item.get("public_url") for item in tunnels if isinstance(item, dict)]
    return tuple(sorted(url for url in urls if isinstance(url, str)))
