# Official reference-v1 interoperability evidence

Date: 2026-08-19

Salareen's official adapter was checked against amireman's exact pinned Police
implementation at commit `0e976b06b1920fd5ed161ad1909d980bfa9962a4`.

- The closed agreement contains exactly 14 terms and uses `setting="Haifa"`.
- The terms SHA-256 is
  `ad9e1bfd724e9debcde523833381cb7982a5d619d693d3738b59e0da61f4d81a`.
- The published commit-reveal vector is
  `4047830b8108320cbf48c1c1e1f09c6c0d47da51c225ce2cf40c7857cefc3030`.
- Thief capture responses are sealed into its own audit records, and a caught
  Thief sends `STAY` without changing position.
- Barrier-on-thief and post-barrier trapped-thief conditions both produce capture.
- A six-game localhost HTTP `/mcp` run passed mutual per-game audits, result
  agreement, and `official_reference_v1` consensus SHA
  `cbd54105eee6ab3f949ae41432d4dcbb7300c8f8e5979ebdc2494d7778927ee4`.
- Full suite: 470 passed. Ruff and the 150-line source gate passed.

The public stable domain is an operator-managed deployment value and is not stored
in Git. A live tunnel check remains required immediately before the friendly.
