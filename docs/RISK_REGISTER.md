# Agdalus Risk Register

Scale: likelihood and impact are 1–5. Score = likelihood × impact. Critical control failures stop promotion.

| ID | Risk | L | I | Score | Control / mitigation | Evidence and owner trigger | Residual decision |
|---|---|---:|---:|---:|---|---|---|
| R-01 | Dependency drift or nonreproducible build | 5 | 4 | 20 | Lockfiles, pinned toolchains/actions, dependency diff, clean-build CI | Maintainer; every PR/release | No alpha on red CI |
| R-02 | Inference engine cannot be packaged acceptably | 4 | 5 | 20 | Time-boxed engine spike; compare package, license, CPU/GPU behavior and quality | Architect; AGD-005 report | Change engine or stop |
| R-03 | Temporary input deleted before stream finishes | 2 | 5 | 10 | Response-owned workspace cleanup, background fallback, lifecycle integration tests | Backend owner; every build | Backend completion/error/early-close paths proven; full worker disconnect drill remains |
| R-04 | Full-file buffering causes OOM/disk exhaustion | 3 | 5 | 15 | Backend 1 MiB chunked persistence implemented; selected-path frontend, preflight, quotas and hardware matrix remain | Performance owner; A0/A1 | Backend allocation reduced; whole-app risk remains open |
| R-05 | Cancellation leaves CPU work, child, or temp data | 4 | 4 | 16 | Cancellation token through FFmpeg/engine; process tree kill; reconciliation | Desktop owner; failure drill | Stop if orphan persists |
| R-06 | Fixed unauthenticated localhost API is abused or races | 3 | 5 | 15 | Ephemeral port, launch secret, strict origin/resource validation, readiness timeout | Security owner; boundary test | Critical on unauthorized success |
| R-07 | Model download fails, is tampered, or surprises user | 4 | 4 | 16 | Manifest/hash, explicit size/approval, bounded retry, resume, rollback | Runtime owner; clean install | Disable affected model |
| R-08 | Unsigned/broken installer destroys trust | 4 | 5 | 20 | Reproducible bundle, malware scan, signing/notarization, clean-machine smoke test | Release owner; each artifact | No public distribution |
| R-09 | Transcript edits/projects are lost or corrupted | 3 | 5 | 15 | Atomic journal, autosave opt-in, recovery, export backup, crash drills | UX/data owner; A1 | Stop pilot on data loss |
| R-10 | Accuracy/confidence presentation misleads users | 4 | 4 | 16 | Stable corpus, subgroup reporting, no false “confidence” metric, uncertainty copy | Evaluation owner; each engine/model | Narrow claims/features |
| R-11 | Privacy/local-only claim is false or unverifiable | 3 | 5 | 15 | Network trace, activity panel, raw-content telemetry prohibition, claim review | Product/security owner; each release | Critical: stop/withdraw claim |
| R-12 | Benchmark overfits or hides regressions | 3 | 4 | 12 | Visible dev set + sealed held-out set, baseline comparison, repeated cases | Evaluation owner; promotion | Reject candidate |
| R-13 | Saved data or telemetry becomes shadow memory | 3 | 5 | 15 | Explicit lifecycle, minimum data, no raw content, delete propagation/reconciliation | Privacy owner; data change | Critical on deleted-data reuse |
| R-14 | Cross-platform scope delays proof | 4 | 3 | 12 | Windows-first gate; macOS starts only after value proof | Product owner; sprint review | Defer macOS |
| R-15 | Demand/pricing assumptions fail | 4 | 4 | 16 | Design-partner interviews, observed tasks, intent test, support-cost measurement | Product owner; week 12 | Pivot or stop, do not inflate ROI |

## Immediate stop conditions

- Unauthorized local API/resource access succeeds.
- An unexplained network connection occurs during a claimed offline task.
- Source audio or transcript content enters logs/telemetry without explicit scope and consent.
- Deleted/temp data affects later behavior or remains after reconciliation deadline.
- Original user media is modified or lost.
- A high-impact external action, model download, or update occurs without the bound approval.
- Required trace or version evidence is missing for a promotion decision.
