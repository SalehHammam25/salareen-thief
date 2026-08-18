# Local live-match gate evidence

Date: 2026-08-18. Scope: localhost only; no ngrok, public domain, PR, merge, or
Stage 6 activity.

Command from sibling `salareen-cop`:
`uv run python tests/support/live_match_gate.py --repeat 2`

Result: PASS. Both canonical runs matched for every scenario. Coordinate and
barrier captures applied 12 actions; trapped capture applied 32; boundary
capture applied 36; survival applied exactly 35. Capture scores were `(20, 5)`
and survival scores were `(5, 10)` on both peers. Acknowledged restart and
terminal restart completed with 12 applications per peer. Lost acknowledgement
replayed `action-0` from the journal and still applied 12 unique actions.

Mismatch ended without outcome/score after two already accepted actions. Retry
exhaustion and watchdog expiry ended without outcome/score after one accepted
action. Attribution remained `unknown`. Every scenario used separate journals
and logs; `finally` reaped both child processes and verified ports 8801/8802
closed. Canonical comparison excluded OS-specific evidence.

Adversarial review found and corrected a survival shutdown race: terminal
reconciliation could begin before the final scent/language boundary completed.
The cop now waits for both final Stage 4 messages before reconciliation.

Remaining: authorized ngrok/public endpoint checks, two-computer symmetric MCP
calls with Saleh, one reconciled remote match, redacted remote evidence, PR
review/merge, and Stage 6. These remain unchecked.

## Windows manual-failure correction

Areen reported a manual failure on 2026-08-18 at the old combined restart
assertion, with runtime `live-gate-j9l3y4fs`. That directory was unavailable
when diagnosis began and the old harness discarded stdout/stderr, so the
original failing peer is not recoverable. The failure remains recorded.

Independent reproduction found both peers timed out after terminal agreement:
cop was stuck before score/shutdown in an unbounded FastMCP call and thief was
waiting for shutdown. Further retained runs exposed Windows connection reset
during peer-close observation, aborted-phase overwrite, restart before the
receiver's `paused` signal, and schedule-dependent recovery evidence.

The correction adds application-level RPC timeouts, bounded identical-message
retries for capture/terminal/score/shutdown, abort preservation, structured
paused-before-restart coordination, confirmed port release, Windows-safe peer
closure, deterministic resume event turns, and per-generation stdout/stderr.
Future failures report role, PID, exit code, timeout, last event, output tails,
bound port, and targeted cleanup action.

Final corrected evidence: acknowledged restart passed 5 consecutive runs; all
other recovery scenarios passed twice. Two complete fresh-root gates passed at
`live-gate-yswgq_ns` (790.6 s) and `live-gate-37n6x7n3` (789.6 s). Ports
8801/8802 and exact peer-runner process counts were zero afterward. The local
Windows gate is PASS again.
