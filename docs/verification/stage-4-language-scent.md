# Stage 4 Language and Scent Verification

**Branch:** `feat/stage-4-language-scent`

**Specification:** 3.0.0

**Technical verification:** PASS

**Final Stage 4 gate:** PASS

## Authority and scope

Chapter 4, Chapter 6.4-6.5, Chapter 10.3.4, Appendix E 25-27, and Annex F
Tables 14, 16, 18 and 21 were read completely. ADR-005 records the original
unblocked boundary. ADR-006 records Areen's six owner-approved engineering
decisions after confirming they do not replace an explicit Annex F fixed value.

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
- Exact-decimal Chebyshev emissions use `0.9`, `0.6`, and `0.3`; old scent
  decays by exactly `0.90`, then new emission combines by cell-wise maximum.
- Center, edge and corner clipping retain in-board strength without wrapping,
  reflection, transfer, or renormalization. Rejections preserve scent identity.
- Exact normalized belief starts uniformly over publicly possible cells, applies
  monotonic scent likelihood before qualitative language, and uses private
  reliability `0.5` through `1.0` with default `0.75`.
- Invalid/zero-weight evidence preserves the previous belief with a typed
  visible result. No belief or provider type contains an objective position,
  action, or mutable Base Logic state.

AC04-01 through AC04-08 all have passing automated evidence.

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
- Finalization first produced 77 focused passes. Ruff then identified one test
  import-order issue, and review found a rounding-sensitive equality assertion;
  both were corrected without weakening behavior.
- Adversarial review added square scent-grid validation, exact integer origins,
  typed invalid-evidence fallback, even-board center regions, validated
  hint-before-belief processing, and prompt coordinate redaction.

## Final commands and results

- `uv --version` - exit 0; `uv 0.12.5`.
- `python --version` - exit 0; `Python 3.12.10`.
- `uv lock` - exit 0; 88 packages resolved.
- `uv sync --frozen` - exit 0; 86 packages checked.
- Stage 1-4 package imports - exit 0.
- `uv run ruff check .` - exit 0; all checks passed.
- `uv run pytest -q` - exit 0; 374 passed, one third-party Authlib warning.
- Focused Stage 4 suite - exit 0; 78 passed.
- Earlier-stage isolation suite - exit 0; 12 passed.
- Line checker - exit 0; 103 Python files, all at or below 150 lines.
- `git diff --check` - exit 0.
- Focused credential scan - no matches (expected `rg` exit 1).
- Earlier-stage import scan - no Stage 4 imports (expected `rg` exit 1).

Independent human reviewer: None

Owner approval: Areen

Review method: Codex-assisted adversarial review and automated verification

## Remaining delivery work

LS-BQ-01 through LS-BQ-06 are resolved by ADR-006 and verified. Only LST-063
(Pull Request) and LST-065 (post-merge synchronization and final gate) remain.

## Delivery evidence

- Reviewed implementation commit: `0c6b2ec` (`feat: implement Stage 4 language
  and scent`).
- Initial push: successful; upstream set to
  `origin/feat/stage-4-language-scent`.
- Finalization commit: `77af8b7` (`feat: finalize Stage 4 language and scent`),
  containing the 29-file reviewed ADR/documentation, scent, belief, language,
  and focused-test update.
- Finalization push: successful to the existing upstream branch.
- At initial branch delivery, the Pull Request was deliberately not created and
  the final gate correctly remained FAIL pending later GitHub events.

## Post-merge closeout

- Pull Request #12 merged into `main` as `48d24e6`.
- `77af8b7` and `c2f8e50` are ancestors of `origin/main`.
- Local `main` fast-forwarded to `48d24e6` with a clean worktree before the
  Stage 5 branch was created.
- LST-063 and LST-065 are complete; final Stage 4 gate: PASS.
