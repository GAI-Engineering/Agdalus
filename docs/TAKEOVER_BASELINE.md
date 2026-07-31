# Agdalus Takeover Baseline

**Baseline date:** 2026-07-31
**Repository:** https://github.com/GAI-Engineering/Agdalus
**Baseline commit:** `37c9d13f4752ba5bfb50091c7ee5affe19686ea0`
**Status:** discovery only; no release-readiness claim

## Ownership position

Agdalus is an early scaffold for local-first desktop transcription. The intended path—Tauri shell, Svelte UI, and local Python/Whisper sidecar—is coherent, but the checked-in repository is not yet a reproducible or usable product build. The immediate owner obligation is to establish a trustworthy golden path before adding features.

The product wedge adopted for planning is: **a signed, simple Windows desktop app for privacy-sensitive interview transcription, with audio that remains on the device and evidence a user can inspect.** macOS remains an intended platform after the Windows workflow is proven.

## Reproducible observations

| ID | Observation | Evidence | Consequence |
|---|---|---|---|
| B-01 | The only GitHub Actions run failed. | [Run 30596480593](https://github.com/GAI-Engineering/Agdalus/actions/runs/30596480593) | No green baseline exists. |
| B-02 | Frontend CI cannot start because no npm lockfile is committed. | `npm ci --ignore-scripts` exits 1; workflow log reports no dependency lockfile. | Dependencies and builds are not reproducible. |
| B-03 | Backend CI fails while building `openai-whisper==20240930` because `pkg_resources` is absent in its isolated build environment. | GitHub Actions backend log at the baseline run. | The documented Python install is not reproducible. |
| B-04 | Release configuration references missing icons and `entitlements.plist`; no `build.rs`, `Cargo.lock`, signed assets, LICENSE, or CHANGELOG are present. | Repository file inventory and `src-tauri/tauri.conf.json`. | Release workflow is aspirational, not operational. |
| B-05 | `StreamingResponse` is returned inside a `TemporaryDirectory` context. The generator consumes the WAV after the context exits. | `backend/main.py` transcription route. | Transcription can fail because its input is deleted before streaming completes. |
| B-06 | The frontend and backend both buffer the entire source file; advertised maximum is 2 GB. | `readFile()` → `File` in `+page.svelte`; `await file.read()` in `backend/main.py`. | Memory usage can exceed safe consumer-device limits. |
| B-07 | Cancel aborts the browser request but does not deterministically cancel FFmpeg/Whisper work. | `AbortController` exists only in frontend fetch flow. | Wasted CPU, unclear status, and leftover work are likely. |
| B-08 | Rust starts a fixed-port sidecar, waits a fixed 800 ms, and does not kill it on window close. | `src-tauri/src/lib.rs`. | Port collision, startup race, and orphan-process risk. |
| B-09 | The packaged backend executable named by Rust is neither built nor bundled. | Release config and repository inventory. | Production desktop build cannot perform transcription. |
| B-10 | README claims clickable playback sync and a signed installer, but neither is evidenced in source or release artifacts. | README compared with UI and release history. | Claims must be narrowed until verified. |
| B-11 | Tauri filesystem read scope spans broad home/appdata/desktop/document/download globs. | `src-tauri/tauri.conf.json`. | Permissions exceed the minimum needed for a chosen input file. |
| B-12 | No tests, evaluation dataset, license, issue backlog, PRs, releases, or versioned risk/evaluation records existed at takeover. | Local inventory and GitHub metadata. | Product, legal, and quality decisions lack an evidence trail. |

## Baseline checks performed

- `python -m compileall -q backend`: pass under local Python 3.13.
- `npm ci --ignore-scripts`: fail, missing lockfile.
- GitHub Actions baseline: backend and frontend fail before lint/type checks.
- Local Rust build: not run; Rust/Cargo are not installed in this workstation environment.
- Graphify analysis: 18 supported files, 178 nodes, 190 built edges, 16 communities, no import cycles. Diagnostic warning: 20 dangling endpoint edges and 3 undirected same-endpoint collapses; treat the graph as navigation evidence, not a perfect architectural oracle.

## Immediate operating rules

1. No release, privacy, accuracy, speed, ROI, signing, or cross-platform claim without a versioned artifact that reproduces it.
2. No feature work enters implementation ahead of P0 build, lifecycle, large-file, and cleanup controls.
3. Audio and transcript content are excluded from telemetry by default. Pilot metrics use local aggregates or explicit user-provided results.
4. Every story links to a risk and an evaluation hook. Critical control failure stops promotion.
5. All model/runtime downloads require pinned identity, integrity verification, bounded retries, visible disk/network cost, and cancellation.

## Next owner checkpoint

The next promotion target is **Internal Alpha A0**, not public beta. A0 requires a reproducible Windows install, a single 30-minute test file completing end-to-end, bounded memory, deterministic cancellation/cleanup, a resolvable local-only network trace, and a green CI run. See `EVALUATION_PLAN.md` for the exact gates.
