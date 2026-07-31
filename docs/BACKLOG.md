# Agdalus Governed Backlog

**Status legend:** `Done` has linked acceptance evidence; `In progress` is partially proven; `Ready` has an acceptance/evaluation definition; `Blocked` lacks a prerequisite; `Later` is evidence-gated.

| ID | Pri | Status | User and outcome | Acceptance evidence | Dependency | Evaluation hook | Risk |
|---|---:|---|---|---|---|---|---|
| AGD-001 | P0 | In progress | Maintainer can reproduce a clean build and test run. | npm lockfile, frontend check/build, pinned backend test environment, lint/type/test CI implemented; Rust/package smoke remains. | None | Loop-001 proof packet; future CI run ID | R-01, R-02 |
| AGD-002 | P0 | Done | User can transcribe without the source disappearing mid-stream. | Workspace exists during stream iteration and cleans after success, iterator error and early close; API integration passes. | AGD-001 | `docs/evidence/runs/2026-07-31-loop-001/PROOF_PACKET.md` | R-03, R-05 |
| AGD-003 | P0 | In progress | User can process long files without device-threatening memory amplification. | Backend uses 1 MiB bounded reads with 15.89× lower traced peak allocation on 32 MiB fixture; frontend zero-copy and 2-hour hardware RSS remain. | AGD-001 | Loop-001 memory evaluator | R-04 |
| AGD-004 | P0 | Ready | User can start, cancel, and close without orphan work. | Ephemeral port, launch secret, readiness timeout, cancel propagation, child kill and one-effect verification. | AGD-001 | Process/port/temp audit | R-05, R-06 |
| AGD-005 | P0 | Ready | Maintainer can package a working inference runtime. | Engine spike compares current Whisper, faster-whisper, and whisper.cpp on package size, install, CPU latency, WER, license, GPU path; ADR selects one. | AGD-001 | Versioned benchmark table | R-02, R-07 |
| AGD-006 | P0 | Blocked | New user can install and complete a first transcript. | Clean Windows installer, model manifest/checksum, disk/RAM forecast, approved download, cancel/retry/resume, actionable errors. | AGD-003–005 | Clean-machine first-run protocol | R-07, R-08 |
| AGD-007 | P0 | Blocked | User can correct text while listening at the relevant timestamp. | Accessible audio player, click-to-seek, editable text, undo, autosave-after-opt-in; correction survives restart. | AGD-002–004 | Timed correction task | R-09, R-10 |
| AGD-008 | P0 | Ready | User exports structurally correct transcript artifacts. | Golden TXT/MD/JSON/SRT fixtures; SRT timestamps valid at carry boundaries; filename/encoding tests. | AGD-001 | Deterministic round-trip tests | R-10 |
| AGD-009 | P0 | Ready | Maintainer can make bounded evidence-backed claims. | Versioned corpus manifest, reference transcripts, engine/model/config IDs, quality/latency/memory/cost/failure results and baseline comparison. | AGD-001, AGD-005 | One documented evaluation command | R-11, R-12 |
| AGD-010 | P0 | Blocked | User can verify what network activity occurred. | Activity view/export distinguishes user-approved model/update calls from inference; raw content absent; unexplained connection fails gate. | AGD-004, AGD-006 | Clean-machine packet/connection trace | R-06, R-13 |
| AGD-011 | P0 | Blocked | User can delete projects and derived data. | Explicit lifecycle for source references, transcript, temp audio, caches, queued work; deletion reconciliation test. | AGD-007 | Deletion propagation test | R-13 |
| AGD-012 | P0 | Blocked | Design partner can recover safely from failure. | Stable reason codes, retry boundaries, recovery guidance, original file untouched, support/rollback runbook. | AGD-002–011 | Failure drills | R-03–R-10 |
| AGD-013 | P1 | Blocked | Pilot owner can run a bounded Windows alpha. | 5–8 consented partners, approved script, support owner, rollback, claim sheet, risk acceptance, A1 gate. | All P0 | Pilot ledger | R-11–R-15 |
| AGD-014 | P1 | Later | User can queue multiple files. | Bounded queue, visible resource budget, pause/cancel/reorder, crash recovery; pilot demand threshold met. | AGD-013 | Completion/support burden delta | R-04, R-05 |
| AGD-015 | P1 | Later | User improves recurring names/terms. | Local glossary with explicit save/delete; measured WER improvement without regression. | AGD-009, AGD-013 | Paired corpus evaluation | R-10, R-13 |
| AGD-016 | P1 | Later | macOS user gets equivalent safe workflow. | Signed/notarized clean install and same functional/privacy gates. | Windows value gate | Cross-platform matrix | R-08, R-14 |
| AGD-017 | P2 | Later | Multi-speaker interviewer can label speakers faster. | Diarization benchmark and correction UX meet value threshold; uncertainty shown. | AGD-009, demand evidence | Speaker error + correction time | R-10, R-12 |
| AGD-018 | P2 | Later | Owner can test sustainable one-time pricing. | Ethical intent test, refund/support assumptions, qualified sample, no fabricated ROI. | AGD-013 | Pricing experiment ledger | R-15 |

## Explicitly deferred

Cloud transcription, team collaboration, meeting bots, automatic external actions, compliance certification, clinical/legal workflows, and LLM summarization are outside the 12-week scope. Adding any requires a recorded scope decision, updated risk/evaluation artifacts, and a new budget/consent model.
