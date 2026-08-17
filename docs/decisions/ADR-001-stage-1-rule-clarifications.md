# ADR-001: Stage 1 Rule Clarifications

**Status:** Approved
**Date:** 2026-08-17
**Branch:** `feat/stage-1-gameplay`
**Decision owner:** Areen

## Context and Authority

Specification version 3.0.0 Chapter 3.4 mandates orthogonal movement or STAY,
permits cop barriers on the current or an adjacent orthogonal cell, declares a
barrier on the thief and a thief with no legal adjacent move to be captures,
and requires truthful declarations. Chapter 3.4-3.5 describes Capture Claim for
capture. Appendix E rules 13-16 consolidate movement/barrier obligations and
rules 46-47 consolidate both special capture paths. Annex F independently lists
move ceiling and survival threshold as minimum 35.

The PDF does not specify an off-board response, a relationship between the two
minimum counters, or the special captures' exact claim procedure. It also
permits STAY while defining trapped capture from unavailable adjacent cells.
These gaps required explicit project decisions. Mandatory PDF text remains
higher authority: the revised own-cell decision follows Chapter 3.4 rather than
rejecting a placement the chapter permits.

## Decisions

1. **Off-board movement:** reject explicitly as out of bounds and return the
   exact original immutable state.
2. **Counter relationship:** an accepted Stage 1 configuration requires
   `max_moves == survival_threshold`. Unequal values produce a deterministic
   relationship issue and no episode outcome.
3. **Capture Claim:** overlap, barrier-on-thief, and trapped-thief captures use
   one local deterministic Capture Claim boundary based on board/state facts.
4. **Cop-own-cell barrier:** accept when other placement and quota rules pass.
   Add the permanent barrier, increment usage once, and keep the cop in place.
   Existing occupancy is grandfathered: STAY and legal exit are allowed, but
   after exit neither agent may enter. Duplicate placement is rejected. If the
   agents already overlap, overlap Capture Claim takes priority.
5. **STAY versus trapping:** STAY does not prevent trapped capture. The thief is
   trapped when no adjacent orthogonal destination is available because it is
   outside the board or blocked by a barrier. No unrelated capture rule is
   added.

## Alternatives Considered

- Treating off-board behavior as unspecified at runtime was rejected because a
  deterministic local response is required.
- Allowing unequal counters with inferred precedence was rejected because the
  PDF supplies no precedence.
- Applying Capture Claim only to overlap was rejected as an unsupported split
  between capture causes.
- Rejecting own-cell placement was withdrawn because it contradicts Chapter
  3.4. Relocation/removal of the cop was rejected because the PDF requires no
  such transition.
- Treating STAY as an escape from trapping was rejected because it would nullify
  the mandatory adjacent-cell trapped rule.

## Deterministic Consequences

All rejection results preserve object identity. Accepted transitions are
immutable and configuration-driven. Every capture records its distinct cause,
becomes terminal only after a valid deterministic claim, receives capture score
`(cop=20, thief=5)`, and rejects later ordinary actions. Repeated identical
inputs must produce identical complete results.

## Deferred Work

Capture Claim here is not cryptographic proof. Nonce, Commit-Reveal, hashing,
signatures, log audit, peer verification, remote configuration comparison,
networking, and MCP remain later-stage integration requirements.
