# Live-match orchestration verification

Branch: `feat/live-match-orchestration`

- `uv lock`: exit 0; 88 packages resolved.
- `uv sync --frozen`: exit 0.
- `uv run ruff check .`: exit 0.
- `uv run pytest -q`: exit 0; 427 passed, one dependency deprecation warning.
- `uv run python scripts/check_python_line_lengths.py`: exit 0; 144 files,
  maximum 150 lines.
- Local process probe: exit 0; thief-first, four turns, two applications at
  each receiver, duplicate response replayed, outcome `cop_capture`, Annex F
  scores cop 20/thief 5.
- Shutdown check: ports 8801 and 8802 closed.

The explicit acknowledged-action recovery regression proves restart replay does
not apply the same action twice. No ngrok, credential or Stage 6 primitive was
used.

Production composition follow-up ran the independent autonomous capture scenario
to coordinate overlap at turn 12 and the survival scenario to exactly 35 accepted
Base Logic actions. Both reconciled Annex F scores and shutdown with separate
JSONL logs and SQLite journals. The accepted shared contract blob is
`81bea39ce3516117541b5b2a471bf211d6303df6`; the earlier expected hash was stale.
