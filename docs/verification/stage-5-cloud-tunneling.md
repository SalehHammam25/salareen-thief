# Stage 5 Cloud Tunneling Verification

**Branch:** `feat/stage-5-cloud-tunneling`

**Specification:** 3.0.0

**Local and single-endpoint public technical gate:** PASS

**Final Stage 5 gate:** FAIL - bidirectional two-machine and complete-match
evidence remains unavailable

## Authority and scope

Chapters 2.4, 8.4 and 10.3.5, Appendix E rules 1-2/10, and Annex F Table 19
were read completely. ADR-007 records Areen's approved ngrok stable-domain,
manual exchange, reconnect, and attribution contracts. A compatible cop
endpoint on a second machine remains the sole external acceptance blocker.

ngrok 3.39.9-msix-stable was already installed and authenticated by Areen. The
authorized public check used test-only port 8802, which is the concrete thief
port in the merged MCP private-configuration fixture. Production still requires
an explicit private `my_port`; no production port was guessed. No account,
firewall, paid plan, or external deployment was changed.

## Implemented evidence

- Provider-neutral start/readiness/health/stop contract and controller.
- Environment-only provider identity, credential, and opponent endpoint; secret
  fields are excluded from representations.
- Shared agreed JSON mapping is authoritative for response timeout, watchdog,
  retry backoff, and retry count. Annex F defaults/minimums are enforced and
  Boolean numeric values reject.
- Remote mode requires public HTTPS and rejects localhost, private IP, userinfo,
  fragments, malformed ports, and unsafe components.
- Endpoint display strips userinfo/fragments and redacts secret query keys.
- Bounded retry/backoff propagates caller cancellation and returns one stable
  exhaustion result. DNS, TLS, disconnect, timeout, process exit, and unknown
  attribution are typed without exception-message leakage.
- Controlled shutdown is idempotent and async context management prevents an
  orphan fake provider. No tunnel layer imports Base Logic, strategy, language,
  scent, belief, or cryptography.
- The operator runbook identifies the exact external prerequisites and redacted
  evidence required for the final gate.
- `NgrokProvider` validates a private stable domain, checks ngrok version and
  authenticated-agent readiness, waits for the local MCP endpoint, starts ngrok
  with safe arguments and no token, accepts only the exact configured URL from
  the local agent API, probes public health, detects exit, and shuts down
  idempotently with terminate/kill fallback.
- Bounded recovery pauses gameplay, reuses the same provider/domain, consults
  the watchdog, and resumes only when game/session/protocol/turn/phase match.
- The public MCP tool call passed; two tunnel restarts returned the identical
  redacted endpoint. Disconnect, watchdog expiry, exact-identity resume, and
  shutdown passed. Post-test process counts were zero for ngrok and the test
  peer. Neither the auth token nor `ngrok.yml` was read or printed.

## Failures and corrections

- Initial focused verification found two Ruff import-order findings, a Python
  `urlencode` generator incompatibility, and an empty-exception test assertion.
  All were corrected; the focused suite then passed 22 tests.
- Adversarial review found raw endpoint values could appear in dataclass reprs,
  private environment variables could override agreed network values, Annex F
  retry/backoff minimums were not enforced, and provider exceptions could
  escape. Secret fields are now repr-hidden, network values come from shared
  configuration, minimums reject deviations, and lifecycle exceptions return
  redacted typed failures. Two regression tests were added.
- The final review found an obsolete test permanently forbidding provider
  adapters after provider approval; it now enforces the durable no-embedded-
  credential/domain boundary. It also found reconnect policy pieces lacked an
  executable coordinator; bounded watchdog/identity recovery and four focused
  tests were added. Direct config construction and missing-command error paths
  were hardened. Ruff import formatting and test-file line count were fixed.

## Final commands and results

- `uv --version` - exit 0; `uv 0.12.5`.
- `python --version` - exit 0; `Python 3.12.10`.
- `uv lock` - exit 0; 88 packages resolved.
- `uv sync --frozen` - exit 0; 86 packages checked.
- Package import - exit 0.
- `uv run ruff check .` - exit 0; all checks passed.
- `uv run pytest -q` - exit 0; 421 passed, one third-party Authlib warning.
- Focused Stage 5 suite - exit 0; 47 passed.
- Boundary/isolation suite - exit 0; 14 passed.
- Line checker - exit 0; 130 Python files, all at or below 150 lines.
- `git diff --check` - exit 0.
- Credential scan - no matches (expected `rg` exit 1).
- Stage 1-4 dependency scan - no matches (expected `rg` exit 1).
- Authorized public test - exit 0; stable domain redacted, restart same, public
  MCP passed, disconnect/watchdog/reconnect/shutdown passed; orphan counts zero.

Independent human reviewer: None

Owner approval: Areen

Review method: Codex-assisted adversarial review and automated verification

## External actions required

A compatible cop endpoint must run on another machine using the same Stage 2
contract. Operators must then record redacted thief-to-cop, cop-to-thief,
complete-match, and remote-restart evidence using the runbook. CLD-025, 046-049,
063, and 065 remain incomplete. No salareen-cop file was modified.

## Delivery evidence

- Reviewed implementation commit: `ea4a053` (`feat: implement Stage 5 cloud
  tunneling`).
- Push: successful; upstream set to
  `origin/feat/stage-5-cloud-tunneling`.
- Pull Request: deliberately not created.
- Final Stage 5 gate remains FAIL pending the documented external actions,
  Pull Request, merge, and synchronization.
