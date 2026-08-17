# Stage 5 Cloud Tunneling Verification

**Branch:** `feat/stage-5-cloud-tunneling`

**Specification:** 3.0.0

**Safe local technical gate:** PASS

**Final Stage 5 gate:** FAIL - authorized public tunnel and two-machine evidence
is unavailable

## Authority and scope

Chapters 2.4, 8.4 and 10.3.5, Appendix E rules 1-2/10, and Annex F Table 19
were read completely. ADR-007 records the safe local boundary and retains all
provider, URL-exchange, reconnect, attribution, credential, firewall, and
two-machine actions as explicit blockers.

No provider was selected or invoked. No account was created, no public tunnel
was opened, no firewall was changed, and no external deployment or paid action
occurred.

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

## Final commands and results

- `uv --version` - exit 0; `uv 0.12.5`.
- `python --version` - exit 0; `Python 3.12.10`.
- `uv lock` - exit 0; 88 packages resolved.
- `uv sync --frozen` - exit 0; 86 packages checked.
- Package import - exit 0.
- `uv run ruff check .` - exit 0; all checks passed.
- `uv run pytest -q` - exit 0; 398 passed, one third-party Authlib warning.
- Focused Stage 5 suite - exit 0; 24 passed.
- Boundary/repeatability suite - exit 0; 14 passed.
- Line checker - exit 0; 117 Python files, all at or below 150 lines.
- `git diff --check` - exit 0.
- Credential scan - no matches (expected `rg` exit 1).
- Stage 1-4 isolation scan - no matches (expected `rg` exit 1).

Independent human reviewer: None

Owner approval: Areen

Review method: Codex-assisted adversarial review and automated verification

## External actions required

Areen and the cop team must select and authorize a provider/account/plan,
approve the URL exchange and reconnect/outage policies, privately provision the
provider client/token and firewall on two machines, implement/approve the
provider-specific adapter, and run the redacted bidirectional/public match,
restart, disconnect, latency, watchdog, and shutdown acceptance procedure in the
runbook. Until that happens, CLD-003/005-007, 021, 023, 025, 029, 036, 040,
044, 046-049, and 065 remain blocked or incomplete.

## Delivery evidence

- Reviewed implementation commit: `ea4a053` (`feat: implement Stage 5 cloud
  tunneling`).
- Push: successful; upstream set to
  `origin/feat/stage-5-cloud-tunneling`.
- Pull Request: deliberately not created.
- Final Stage 5 gate remains FAIL pending the documented external actions,
  Pull Request, merge, and synchronization.
