# PRD 06 - Security and Cryptography
**Status:** Approved for minimum mandatory implementation
**Repository:** salareen-thief
**Implementation:** In progress on `feat/stage-6-7-security-series`
**Specification:** 3.0.0

## Purpose
Secure the proven remote protocol with byte-identical signed configuration, SHA-256 Commit-Reveal, secret Nonces, Capture Claim verification, complete logs and signed Step-0 declarations (Ch5; Ch10.3.6).

## Authority and Classification
- **Mandatory:** Chapter 5, Appendix B, Appendix E 11-24 and 46-48, Annex F.
- **Fixed:** SHA-256 Commit-Reveal; fresh cryptographic Nonces; deterministic canonical bytes; tamper mismatch causes technical loss/zero.
- **Example:** sample payload/code and 16-byte token are illustrative; production record must cover all agreed fields.
- **Engineering decisions:** canonical JSON profile, signature/key algorithm/distribution, claim schema and log chaining require cross-repository approval.

## Scope
Peer byte comparison/refusal; shared-config signing/locking; per-game named config; Commit/Acknowledge/Reveal/final audit; complete commitment context; all-cause Capture Claims; append-only audit logs; signed Step-0 hardware/model/team/game-count/exact-commit declaration; token accounting; constant-time comparison.

## Non-Goals
New strategy/tunnel behavior, Gmail, GUI and league orchestration. Crypto cannot resolve game-rule ambiguity.

## Mandatory Requirements
1. Require byte-identical shared JSON and refuse mismatch (Appendix B; E11).
2. Enforce Annex F classifications (E12).
3. Use SHA-256 Commit-Reveal for every move (E17).
4. Keep a fresh secure Nonce secret until final audit (E18).
5. Acknowledge before reveal; reveal move/hint with Nonce hidden.
6. Reveal all Nonces and recompute all commitments after the game.
7. Any mismatch/tamper gives the falsifier technical loss/zero (E19).
8. Lock the scent model before play (E23).
9. Sign Step-0 hardware/model/team/game-count/exact Git commit declaration (E24, E53).
10. Record actual token usage (E54).
11. Verify truthful capture claims and reject false claims (E21-E22, E46-E47).
12. Never commit private keys, Nonces before reveal, secrets or credentials.

## Acceptance Criteria
- AC06-01: byte differences refuse before state creation.
- AC06-02: canonical inputs hash identically across repositories.
- AC06-03: any altered field/Nonce fails audit.
- AC06-04: reused/predictable/missing Nonces reject.
- AC06-05: phase violations reject without mutation.
- AC06-06: every capture cause uses one verified claim path.
- AC06-07: false claims produce mandated loss.
- AC06-08: single-field log mutation is detected.
- AC06-09: Step-0 binds exact commit and required metadata.
- AC06-10: secrets never appear in Git/logs/errors/fixtures.
- AC06-11: security, negative and cross-peer tests plus all gates pass.

## Engineering Decisions and Residual Blockers
- Canonical profile: sorted-key, compact UTF-8 JSON with no NaN, duplicate keys,
  or alternate byte encodings.
- Signatures: Ed25519 from `cryptography`; signatures use validated, case-sensitive
  standard Base64. Public keys are provisioned out of band; private keys never
  enter Git.
- Commitments: domain-separated SHA-256 over canonical complete payload and a
  fresh 32-byte secret nonce; acknowledgement is mandatory before reveal.
- Claims and logs: one common capture envelope and a SHA-256 previous-entry chain;
  first falsifying mismatch fails closed.
- **SEC-BQ-01:** production public-key identity provisioning remains external.
- **SEC-BQ-02:** resolved for the minimum mandatory protocol by the shared schema.
- **SEC-BQ-03:** resolved for deterministic overlap/barrier/trapped evidence.
- **SEC-BQ-04:** intent truth/lie vocabulary and audit method are incomplete.
- **SEC-BQ-05:** partial audit/crash recovery is unspecified.
- **SEC-BQ-06:** conflicting peer tamper allegations require an agreed protocol.
