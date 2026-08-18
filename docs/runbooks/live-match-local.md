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

`--scenario` also accepts `barrier_capture`, `trapped`, `capture_priority`, and
`survival`. Private strategy and
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

## Complete local pre-ngrok gate

From the sibling `salareen-cop` repository, run exactly:

```powershell
uv run python tests/support/live_match_gate.py --repeat 2
```

The harness starts both production runners with separate journals and JSONL
logs, requires event-plus-port readiness, performs controlled interruption and
restart cases, and terminates/kills/reaps peers in `finally`. Every run has a
fresh runtime directory and canonical evidence comparison.
On failure, preserve the printed runtime directory. The harness reports each
peer's PID, exit/timeout state, last event, stdout/stderr tail, bound port, and
targeted cleanup action; do not delete that directory before diagnosis.

Tomorrow with Saleh: privately exchange stable HTTPS endpoints; start one peer
on each computer; verify symmetric MCP calls; complete and reconcile one remote
match; retain redacted logs; then run the authorized ngrok checks. Do not begin
Stage 6 or merge until that remote evidence exists.
