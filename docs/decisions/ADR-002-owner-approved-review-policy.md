# ADR-002 - Owner-Approved Review Policy

**Status:** Approved by Areen
**Date:** 2026-08-17
**AI interface:** Codex

## Context

Specification 3.0.0 requires disciplined staged delivery, repository history,
verification and submission evidence, but does not explicitly require an
independent human reviewer. The independent-review condition was added by the
project PLAN/TODO as a safety practice.

PR #8 and PR #9 were merged before any independent review. GitHub contains no
formal review, review comment or independent-review evidence for either PR.
This fact must not be rewritten or described as an independent review.

## Decision

Pull Requests and automated verification remain mandatory. Independent human
review is recommended when available, but Areen may approve an exception when
none is available. The exception requires a strict Codex-assisted adversarial
self-review, truthful tool/command evidence, explicit disclosure that no human
reviewer participated, and Areen's explicit owner approval.

## Stage 1 Corrective Closeout

Areen explicitly approved this exception. Stage 1 commit `d6ddf3f` was merged
by PR #8 as merge commit `25dee6c` before review. Its recorded technical gate
passed 199 tests, Ruff, ten dependency-isolation tests, the 150-line check and
credential scans. Codex performed the documented adversarial review before the
commit, but no independent human reviewer participated. PR #9 later merged the
Stage 2-7 documentation without an independent reviewer.

The merge-before-review order is a process deviation. The corrective action is
this transparent owner-approved exception and retained verification evidence,
not a claim that review occurred earlier or independently.

## Required Disclosure

`Independent human reviewer: None`

`Owner approval: Areen`

`Review method: Codex-assisted adversarial review and automated verification`
