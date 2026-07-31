# Agdalus Evaluation and Promotion Plan

## Purpose

This plan distinguishes deterministic product controls from probabilistic transcription quality. It does not authorize release; it defines reproducible evidence required for decisions.

## Versioned evidence manifest

Every run records: app commit/version, OS/hardware class, engine/model/hash, FFmpeg/runtime/toolchain versions, configuration/budget version, dataset manifest/hash, correlation ID, outcome reason code, latency, peak memory, peak temp disk, retries/timeouts, and test results. Raw audio/transcripts remain in the controlled evaluation corpus and are not copied into telemetry.

## Test corpus

- Synthetic fixtures: malformed headers, zero-byte, truncated, silent, stereo, variable-rate, unusual Unicode filename, and duration/size boundaries.
- Licensed/consented speech: 1, 10, 30, and 120-minute samples; quiet/noisy; at least English plus one secondary language only when reference transcripts exist.
- Development set is visible and used for debugging. Held-out set is sealed and opened only for promotion runs.
- Reference transcripts and segment timing rules are versioned; changes create a new dataset version.

## Deterministic gates

| Gate | Target |
|---|---|
| Clean checkout | One documented command installs and runs all checks; CI green. |
| Input integrity | Original file hash unchanged in every test. |
| Authorization boundary | Only the selected file/app-owned paths are readable; unauthorized local API attempt succeeds 0 times. |
| Network boundary | Inference produces 0 unexplained outbound connections; documented model/update connections require explicit approval. |
| Cleanup | 100% temp/process/port reconciliation after success, cancel, timeout, crash and restart. |
| Export correctness | 100% golden TXT/MD/JSON/SRT conformance; citations to app/model versions resolve. |
| Deletion | 100% propagation through projects, temp, cache, queue and recovery journal within the documented deadline. |
| Budget exhaustion | Request stops safely at file/duration/memory/disk/time/retry budget; no silent extension. |

## Performance and quality targets

Targets are hypotheses until the baseline run is complete.

| Metric | Internal A0 | Design alpha A1 | Beta decision B0 |
|---|---:|---:|---:|
| Supported-file completion | ≥90% synthetic/clean fixtures | ≥90% pilot corpus | ≥95% supported held-out corpus |
| Peak app+worker RSS | ≤2.0 GB or ≤35% of physical RAM, whichever is lower, excluding explicitly disclosed model residency | Same | Threshold revisited from observed hardware; no hidden regression |
| Temp disk | ≤1.5× decoded audio estimate with preflight and cleanup | Same | Same |
| Cancellation acknowledgement | ≤2 s UI; worker termination ≤10 s | Same | p95 reported |
| Startup readiness | p95 ≤10 s after runtime installed | p95 reported | p95 ≤5 s target if evidence supports |
| Transcript quality | Baseline WER/CER only | No regression versus chosen engine baseline | Held-out WER/CER reported by language/noise class |
| Correction value | Not required | Directional timing study | Median ≥50% active-time reduction vs participant baseline across ≥10 tasks |
| First success | Clean-machine completion | ≥80% unassisted among 5–8 partners | ≥80% among ≥15 qualified users |
| Critical incidents | 0 | 0 | 0 |

WER/CER are not sufficient alone. Reviewers also score usefulness (1–5), missing material, timestamp usefulness, names/terms, and required corrections. Do not collapse subgroup or difficult-audio failures into one average.

## Failure drills

Kill the UI, sidecar, FFmpeg, and model process independently; deny disk space; remove network during approved model download; corrupt the model cache; collide the preferred port; revoke file access; cancel at each stage; and restart after a partial project write. Each drill must yield a stable reason code, truthful user state, bounded retry, and reconciled resources.

## Cost and token economics

Core transcription is local deterministic/ML execution, not a hosted-token workflow. Measure CPU/GPU time, energy proxy where available, model/download bytes, disk, support minutes, and elapsed time. If an LLM-dependent feature is later proposed, it requires per-request input/output/call/time/cost budgets, a no-LLM baseline, content consent, and safe exhaustion behavior before implementation.

## Promotion decisions

1. Run deterministic gates.
2. Stop on any critical failure.
3. Compare candidate with last known-good using identical corpus/environment.
4. Run held-out and failure drills.
5. Review value, support burden, privacy, quality, latency, and cost together.
6. Update backlog, risk register, ADRs, known limitations, and claim sheet.
7. Accountable owner records promote, narrow, rollback, repeat, pivot, or stop.
