# TODO 06 - Security and Cryptography

**Status:** Ready for review
**Related PRD:** `../prd/PRD-06-security-and-cryptography.md`
**Implementation:** Not started
**Task ID range:** SEC-001 through SEC-065

All tasks are unchecked. A task may be checked only when its evidence exists. Items that depend on a PRD blocked question remain non-executable until the decision is approved.

**Trace legend:** protocol/Step-0 -> PDF Ch5; shared config -> Appendix B; mandatory rules -> Appendix E 11-24/46-48; values -> Annex F; milestone -> Ch10.3.6; acceptance -> PRD-06 AC06.

## Authority and cryptographic design

- [ ] **SEC-001** Reconfirm PRD-06 against Chapter 5, Appendix B, Appendix E 11-24/46-48 and Annex F. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-002** [BLOCKED: SEC-BQ-01..06] Resolve or retain every security blocker. {Trace: PRD-06; PLAN:Stage 6; PDF:Ch5/Appendix B}
- [ ] **SEC-003** [BLOCKED: SEC-BQ-02] Approve canonical JSON byte profile. {Trace: PRD-06; PLAN:Stage 6; PDF:Ch5.3/Appendix B}
- [ ] **SEC-004** [BLOCKED: SEC-BQ-01] Approve digital-signature algorithm and key format. {Trace: PRD-06; PLAN:Stage 6; PDF:Appendix B}
- [ ] **SEC-005** [BLOCKED: SEC-BQ-01] Approve public-key exchange/trust procedure. {Trace: PRD-06; PLAN:Stage 6; PDF:Appendix B}
- [ ] **SEC-006** [BLOCKED: SEC-BQ-02] Approve complete commitment payload schema. {Trace: PRD-06; PLAN:Stage 6; PDF:Ch5.3}
- [ ] **SEC-007** [BLOCKED: SEC-BQ-03] Approve Capture Claim protocol. {Trace: PRD-06; PLAN:Stage 6; PDF:E21-22/46-47}
- [ ] **SEC-008** [BLOCKED: SEC-BQ-05..06] Approve partial-audit/crash disposition. {Trace: PRD-06; PLAN:Stage 6; PDF:Ch5.4}
- [ ] **SEC-009** Document security threat model. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-010** Map every acceptance criterion to tests. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}

## Configuration and Step-0

- [ ] **SEC-011** Canonicalize shared game JSON deterministically. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-012** Reject duplicate keys/noncanonical prohibited representations. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-013** Compare shared configuration bytes before game creation. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-014** Refuse any peer byte mismatch. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-015** Enforce fixed/minimum/negotiable Annex F classifications. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-016** Sign/verify shared configuration using approved scheme. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-017** Use unique per-game config filename. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-018** Require per-game config artifact in repository. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-019** Keep private TOML unsigned/local and subordinate. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-020** Test one-byte configuration mismatch refusal. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}

## Commit-Reveal

- [ ] **SEC-021** Define signed Step-0 declaration schema. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-022** Include OS, CPU cores/frequency, RAM and GPU/VRAM. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-023** Include model/provider and team identity. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-024** Include actual declared game count. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-025** Include exact Git commit hash. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-026** Sign and verify Step-0. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-027** Reject missing/false/invalid Step-0 fields. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-028** Record actual token budget/usage fields. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-029** Test Step-0 deterministic serialization. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-030** Keep private hardware-sensitive extras out of logs. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}

## Claims and audit

- [ ] **SEC-031** Generate fresh Nonce using cryptographic randomness. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-032** Keep Nonce secret until final audit. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-033** Build SHA-256 commitment over complete approved payload. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-034** Use constant-time digest comparison. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-035** Implement Commit state transition. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-036** Require peer acknowledgement before reveal. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-037** Reveal move/hint/intent without Nonce. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-038** Reject reveal-before-acknowledge. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-039** Reject commitment reuse and missing Nonce. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-040** Test same payload/new Nonce yields different digest. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}

## Adversarial security tests

- [ ] **SEC-041** Define common Capture Claim envelope. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-042** Verify overlap Capture Claim. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-043** Verify barrier-on-thief Capture Claim. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-044** Verify trapped-thief Capture Claim. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-045** Reject false capture with mandated loss. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-046** Append immutable commit/ack/reveal events. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-047** Reveal every Nonce at game end. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-048** Recompute every commitment during mutual audit. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-049** Stop on first mismatch and identify falsifying side. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-050** Map tamper to technical loss score zero. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}

## Verification and delivery

- [ ] **SEC-051** Test changes to state/move/intent/hint/step/role/game/Nonce. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-052** Test truncated/reordered/duplicated logs. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-053** Test forged signatures and wrong public keys. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-054** Test nonce secrecy in logs/errors before audit. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-055** Run known SHA-256/canonicalization vectors across processes. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-056** Run cross-repository contract fixtures. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-057** Run fuzz/property tests for malformed security messages. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-058** Run uv, Ruff, pytest, line, credential and dependency checks. {Trace: PRD-06; PLAN:Stage 6; PDF:applicable authority}
- [ ] **SEC-059** Record exact evidence, failures and corrections. {Trace: PLAN:Cross-Stage Verification}
- [ ] **SEC-060** Inspect staged diff and prove no key/Nonce/secret is staged. {Trace: PLAN:Git workflow}
- [ ] **SEC-061** Commit only reviewed Stage 6 files. {Trace: PLAN:Git workflow}
- [ ] **SEC-062** Push the dedicated Stage 6 branch. {Trace: PLAN:Git workflow}
- [ ] **SEC-063** Open a focused Stage 6 Pull Request. {Trace: PLAN:Git workflow}
- [ ] **SEC-064** Obtain independent security review when available or record the ADR-002 owner-approved Codex review exception. {Trace: PLAN:Review Policy; PLAN:Stage 6 gate}
- [ ] **SEC-065** Record PASS only after merge and synchronization; otherwise FAIL. {Trace: PDF:Ch10.4; PLAN:Stage 6 gate}
