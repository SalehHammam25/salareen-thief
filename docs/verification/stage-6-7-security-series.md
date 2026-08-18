# Stage 6-7 execution evidence

- Branch: `feat/stage-6-7-security-series`
- Focused Stage 6/7 tests: 6 passed.
- Full suite after integration: 444 passed, one third-party deprecation warning.
- Established cop-driven live gate: 11/11 scenarios passed with `--repeat 1` in 480.1s.
- Shared Stage 6 schema, Stage 7 schema, and canonical fixture are byte-identical.
- No production key, credential, token, domain, or opponent endpoint is included.

The local implementation gate passes. Push, merge, tag, production key exchange,
and an authorized remote-peer run remain intentionally external/deferred.

## Production integration continuation (2026-08-19)

- Signed Step-0/config exchange now precedes `GameplayAdapter.initialize()` and
  therefore precedes initial match-state construction.
- Production actions use commitment submission/acknowledgement before action
  reveal; capture claims use the common verifier; both audit ledgers and secret
  outbound nonces survive peer-local recovery for final audit.
- Focused production security tests: 9 passed.
- Full suite: 446 passed, one third-party deprecation warning.
- Complete cop-driven live/security gate: 11/11 scenarios passed in 549.6 seconds.
- Executable Tk reporting GUI added.

## Final compliance cleanup (2026-08-19)

- Gmail delivery uses the Gmail API OAuth flow with only the `gmail.send` scope;
  SMTP and app-password handling were removed.
- OAuth client and token locations are caller-supplied paths, and credential,
  token, secret-directory, and runtime-database patterns are ignored by Git.
- Focused OAuth and Stage 6/7 tests: 13 passed.
- Ruff: passed. Python 150-line gate: 179 files checked, passed.
- Full suite: 451 passed, one third-party deprecation warning.
- The nine-minute live gate was not rerun because cleanup changed no live-match
  behavior; the preceding 11/11 cop-driven live/security result remains the
  live evidence.

## Persistent operator identity gate (2026-08-19)

- Production loads the thief Ed25519 identity from
  `SALAREEN_THIEF_ED25519_PRIVATE_KEY_PATH` and pins the peer supplied through
  `SALAREEN_THIEF_EXPECTED_PEER_PUBLIC_KEY`.
- A journal-replayed bootstrap re-verifies its signed bundle and pinned peer;
  commitment submission tolerates only the bounded `SECURITY_REQUIRED` race
  while a restarted peer completes that verification.
- Actual-key restart comparison preserved the same thief public identity and
  `SHA256:d9iHCmAbFJjhG2aQdKzYx4nzT3XlmQcPXgoRdk/gvV4` fingerprint.
- Full suite: 453 passed, one third-party deprecation warning.
- Cop-driven persistent-identity live/security gate: 11/11 scenarios passed
  once in 555.3 seconds, including acknowledgement restart, lost
  acknowledgement, mismatch, retry exhaustion, watchdog, and terminal restart.
