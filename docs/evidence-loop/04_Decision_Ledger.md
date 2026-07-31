# Decision Ledger

| ID | Timestamp | Actor / role | Decision | Reason | Evidence | Conditions |
|---|---|---|---|---|---|---|
| DEC-001 | 2026-07-31 | User, product owner | Start the engineering evidence loop and implement the first technical slice. | Move from roadmap to tested evidence. | Current user instruction | Preserve governance gates and report measured results only. |
| DEC-002 | 2026-07-31 | Codex, implementation agent | Select backend bounded persistence plus response-lifetime cleanup as the first slice. | It removes the highest-severity confirmed runtime defect with a small testable surface. | CLM-001–003; AGD-002/003 | Frontend zero-copy, process cancellation, sidecar auth, inference packaging, and release remain out of scope. |
| DEC-003 | 2026-07-31 | Codex, governed increment reviewer | Proceed with conditions to the next engineering slice. | Unit, integration, coverage, lint, type, frontend check/build and bounded-memory gates pass. | CLM-005–008 | No release; require GitHub CI, Rust/package build, frontend selected-path ingest and worker cancellation before A0. |
