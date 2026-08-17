# PRD 07 - Reporting and Visualization Shell
**Status:** Ready for review
**Repository:** salareen-thief
**Implementation:** Not started
**Specification:** 3.0.0

## Purpose
Complete the observable/submission shell: local-truth GUI, mandatory verified replay, league accounting, signed JSON results and separate Gmail/OAuth reporting from both peers (Ch7, Ch9, Ch10.3.7).

## Authority and Classification
- **Mandatory:** Chapters 7/9, Appendices A/C, Appendix E 8-10, 20 and 28-55, Annex F.
- **Fixed Annex F:** 6 games/series, diversity 10, minimum 2 different teams, maximum 10 games/team, tie 2. Annex F's six-game series is in unresolved tension with Appendix E rule 52's one counted game per opponent; neither interpretation is implemented until REP-BQ-07 is approved.
- **Negotiable:** series token budget ~200000.
- **Examples:** Tkinter/PyQt, layout and sample token-bucket code.
- **External:** Google setup, credentials, repository access, final form/PDF and annotated tag need human action.

## Scope
Local-truth live GUI; belief heatmap/turn lock; verified replay; screenshots; counted-game/league rules; declaration/config/log/result JSON lifecycle; independent agreeing peer reports; Gmail send-only OAuth; quota/token bucket/DOS/429 controls; two repositories/cross-links; academic README, tag and checklist.

## Non-Goals
Changing rules/strategy or weakening cryptographic audit. GUI never reveals global objective state.

## Mandatory Requirements
1. Display local truth only, belief heatmap and YOUR TURN/LOCKED (Ch7; E8-E9).
2. Replay recomputes every commitment and disqualifies any tamper (E20).
3. Count one game per opponent; warm-ups remain uncounted (E52).
4. Enforce the non-contradictory Annex F league values and truthful counts (E31, E37-E38); the six-versus-one contradiction remains blocked.
5. Both peers agree and independently report (E35-E36).
6. Attach machine-readable JSON, never free-text-only results (E32-E34).
7. Send to Annex F address with declaration/config/log/result data (E51; F20).
8. Report total tokens per game/series (E54).
9. Use OAuth gmail.send only; never passwords/read scopes (Appendix A; E30).
10. Apply quota/token-bucket/DOS/429 controls (E28-E29).
11. Ignore credentials.json/token.json and all secrets (E39-E40).
12. Maintain two accessible, cross-linked repositories, required docs/report/tag (E41-E50).

## Acceptance Criteria
- AC07-01: GUI local truth/lock behavior is verified.
- AC07-02: valid replay shows Verified OK; mutation shows TAMPERED/disqualification.
- AC07-03: peer JSON reports validate and agree.
- AC07-04: sender uses gmail.send and attaches JSON.
- AC07-05: rate/quota/DOS/429 tests prevent flooding.
- AC07-06: credential scans are clean.
- AC07-07: league count/diversity/cap/tie rules pass.
- AC07-08: repositories contain/cross-link required artifacts/screenshots/commit IDs.
- AC07-09: all implementation and submission gates pass.

## Blocked Questions
- **REP-BQ-01:** complete declaration/log/result JSON schemas are not fully enumerated.
- **REP-BQ-02:** email subject/body, persistence and duplicate-send policy are unspecified.
- **REP-BQ-03:** GUI toolkit/layout/accessibility are not mandated.
- **REP-BQ-04:** game_id versus game_uid derivation is inconsistent.
- **REP-BQ-05:** league scheduling/opponent discovery/aggregation are undefined.
- **REP-BQ-06:** group code, form fields and deadlines are external inputs.
- **REP-BQ-07:** Annex F fixes six games in a series against an opponent, while Appendix E rule 52 permits only one counted game per opponent. The PDF does not define whether "game" and "series/sub-game" reconcile these rules.
