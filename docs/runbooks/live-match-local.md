# Local live-match runner

From this repository, start the thief peer with a private journal:

```powershell
$env:SALAREEN_THIEF_JOURNAL='.runtime/thief-match.sqlite3'
uv run python -m salareen_thief.live_match.runner --host 127.0.0.1 --port 8801
```

The peer exposes `/mcp`. Local mode uses loopback HTTP only. Remote mode requires
the exact configured public HTTPS host, permitted port and `/mcp` path. Never put
credentials in an endpoint, journal, command line or log.

Start the cop independently on port 8802, then run
`uv run python tests/support/live_match_process_probe.py`. Stop both peer
processes after the probe. This runbook does not start ngrok.
