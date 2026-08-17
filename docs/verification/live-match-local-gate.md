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
