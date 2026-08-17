# Stage 4 Language and Scent Verification

**Branch:** `feat/stage-4-language-scent`

**Specification:** 3.0.0

**Unblocked technical subset:** PASS

**Final Stage 4 gate:** FAIL - six approved specification blockers and delivery
events remain

## Authority and scope

Chapter 4, Chapter 6.4-6.5, Chapter 10.3.4, Appendix E 25-27, and Annex F
Tables 14, 16, 18 and 21 were read completely. ADR-005 records the boundary
between fixed/negotiable values, optional provider modes, and the six unresolved
engineering decisions. No scent evolution or Bayesian belief behavior was
invented.

## Implemented evidence

- Shared Stage 4 configuration validates fixed `0.9`, `0.10`, and `5`, rejects
  Boolean numeric values and duplicate JSON keys, and loads the negotiated map,
  hint limit, and token budget without enforcing later-stage sections.
- Frozen scent-grid and opponent-observation types enforce a finite `[0, 0.9]`
  value domain and expose no objective opponent position or own-scent field.
- The versioned free-language contract treats input as untrusted, enforces the
  word limit, and rejects unmistakable direct numeric-coordinate forms.
- Provider configuration is private TOML only. The four Annex F modes are typed;
  missing configuration selects deterministic zero-token template fallback.
- Provider results contain text and actual token counts, not actions or state.
  Cadence, timeout, cancellation, actual usage, exhausted-budget behavior,
  visible fallback reasons, and prompt-injection isolation have focused tests.
- Fresh-process and repeated-input tests produce identical template results.

AC04-04 through AC04-08 pass for the executable subset. AC04-01 through
AC04-03 remain blocked where they require scent arithmetic or belief updates.

## Failures and corrections

- The first in-sandbox `uv` command was denied by Windows access controls. The
  same commands ran successfully with the approved `uv` execution permission.
- Ruff initially found no violations and the first full suite passed 332 tests.
- Review found that 5x5 was being treated as merely positive instead of fixed;
  fixed-value rejection and a regression test were added.
- Review found actual provider tokens were discarded on invalid or over-budget
  replies. Accounting now preserves real usage and prevents calls after budget
  exhaustion; focused tests prove both paths.
- Review added the PDF intensity upper bound, explicit caller-cancellation
  propagation, fresh-process repeatability, missing game identity, and an
  additional unmistakable coordinate form.

## Final commands and results

- `uv --version` - exit 0; `uv 0.12.5`.
- `python --version` - exit 0; `Python 3.12.10`.
- `uv lock` - exit 0; 88 packages resolved.
- `uv sync --frozen` - exit 0; 86 packages checked.
- Stage 1-4 package imports - exit 0.
- `uv run ruff check .` - exit 0; all checks passed.
- `uv run pytest -q` - exit 0; 339 passed, one third-party Authlib warning.
- Focused Stage 4 suite - exit 0; 43 passed.
- Earlier-stage isolation suite - exit 0; 12 passed.
- Line checker - exit 0; 91 Python files, all at or below 150 lines.
- `git diff --check` - exit 0.
- Focused credential scan - no matches (expected `rg` exit 1).
- Earlier-stage import scan - no Stage 4 imports (expected `rg` exit 1).

Independent human reviewer: None

Owner approval: Areen

Review method: Codex-assisted adversarial review and automated verification

## Deferred work

LS-BQ-01 through LS-BQ-04 block scent emission, decay, overlap, boundaries, and
their repeatability fixtures. LS-BQ-06 blocks belief construction and updates.
LS-BQ-05 blocks a claim of comprehensive numeric-language smuggling coverage.
The Pull Request, merge, synchronization, and final PASS gate have not occurred.

## Delivery evidence

- Reviewed implementation commit: `0c6b2ec` (`feat: implement Stage 4 language
  and scent`).
- Initial push: successful; upstream set to
  `origin/feat/stage-4-language-scent`.
- Pull Request: deliberately not created.
- Final Stage 4 gate remains FAIL because the retained blockers and merge gate
  are incomplete.
