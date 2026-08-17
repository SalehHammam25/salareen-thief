# Local live-match runner

From this repository, start the thief peer with a private journal:

```powershell
$env:SALAREEN_THIEF_JOURNAL='.runtime/thief-match.sqlite3'
$env:SALAREEN_THIEF_EVENT_LOG='.runtime/thief-match.jsonl'
$env:SALAREEN_PRIVATE_CONFIG='C:\private\thief.toml'
uv run python -m salareen_thief.live_match.runner --host 127.0.0.1 --port 8801 `
  --opponent http://127.0.0.1:8802/mcp --game-id local-game `
  --session-id local-session --scenario capture
```

`--scenario` also accepts `barrier_capture` and `survival`. Private strategy and
provider files remain local; automated verification always uses the template
provider. End the match through `shutdown_match_v1`; an operator may stop the
process only after the local journal and JSONL log have flushed.

## Tomorrow: two-computer placeholders

Set the opponent URL to `https://<COP-STABLE-HOST>/mcp`, retain a private
journal/log path, and use the agreed game/session IDs. Replace only the
placeholder host after private exchange. Do not put tunnel credentials in the
URL or command. This connectivity has not yet been tested.

The peer exposes `/mcp`. Local mode uses loopback HTTP only. Remote mode requires
the exact configured public HTTPS host, permitted port and `/mcp` path. Never put
credentials in an endpoint, journal, command line or log.

Start the cop independently on port 8802, then run
`uv run python tests/support/live_match_process_probe.py`. Stop both peer
processes after the probe. This runbook does not start ngrok.
