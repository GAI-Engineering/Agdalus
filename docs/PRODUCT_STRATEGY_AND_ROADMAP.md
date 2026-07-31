# Agdalus Product Strategy and Value-Driven Roadmap

**Decision date:** 2026-07-31
**Horizon:** 12 weeks to a measured Windows beta decision
**Planning status:** hypotheses and gates, not outcome claims

## 1. Product thesis

Agdalus should not compete by becoming another broad AI media suite. Its best initial job is narrower:

> Help a privacy-sensitive Windows user turn a recorded interview into a correct, editable, timestamped transcript without uploading the recording or learning a technical tool.

The product wins only if it proves four things together: installation is trustworthy, the first transcript succeeds without setup expertise, correction is materially faster than manual transcription, and users can verify the local-only boundary.

## 2. Segment and ICP

### Primary design segment

| Element | Definition |
|---|---|
| User / buyer | Individual qualitative researcher, independent journalist, oral historian, or interview-led creator using Windows; buyer and user are usually the same person. |
| Urgent job | Convert 30–120 minute interviews into editable, timestamped text while retaining control of sensitive source audio. |
| Current alternatives | Manual transcription, unsigned/open-source desktop software, Mac-only local tools, or metered cloud editors. |
| Pain | Upload reluctance, uncertain privacy, installation friction, long correction cycles, and recurring cost for irregular workloads. |
| Switching trigger | A sensitive interview, a deadline, a cloud-policy restriction, or an unexpectedly high recurring transcription bill. |
| Initial exclusion | Clinical documentation, legal evidentiary transcription, live accessibility captions, team collaboration, and regulated compliance promises. |

### Secondary segments, gated by primary evidence

1. Podcasters and video creators needing private rough transcripts and subtitles.
2. Students and faculty transcribing lectures or research recordings with authorization.
3. macOS privacy-sensitive interviewers who want a simpler alternative, only after Windows reliability is proven.

## 3. Competitive map

| Alternative | Demonstrated strength | Gap Agdalus may target | Strategic response |
|---|---|---|---|
| MacWhisper | Mature Mac product; free and €64 pay-once tiers; local/cloud models, many export and workflow features. [Official site](https://www.macwhisper.com/) | Mac-first and broad feature surface leave no obvious reason to attack it head-on. | Do not lead with macOS or feature parity. Learn from its onboarding and proof of one-time pricing. |
| Buzz | Free/open-source, offline, Windows/macOS/Linux, live transcription, speaker features and multiple backends; Windows build is documented as unsigned. [Official GitHub](https://github.com/chidiwilliams/buzz) | Trustworthy signed Windows install and lower-complexity interview workflow may be a wedge. | Compete on verified install trust, first-run success, safe defaults, and correction workflow—not raw feature count. |
| Descript | Integrated cloud media editor with transcription, collaboration, and AI tools; plans meter media hours/AI credits. [Official pricing](https://www.descript.com/pricing) | Cloud workflow, recurring spend, and broad editor complexity are mismatched for privacy-sensitive occasional use. | Position around local control and a focused interview-to-transcript path; do not build a video editor. |
| Manual transcription | Maximum human control and no new software trust requirement. | Very high time cost and inconsistent timestamping. | Measure correction time against this baseline; never assume savings without observed trials. |
| Generic Whisper CLI | Flexible and free for technical users. | Setup, models, FFmpeg, commands, exports, and error recovery are burdensome. | Package the technical stack into a trustworthy, inspectable appliance. |

### Differentiation thesis

Agdalus is **the smallest trustworthy path from a sensitive interview file to an editable Windows transcript**. Differentiation must exist as capabilities:

- signed, reproducible installer and pinned local inference assets;
- explicit local-only mode with a user-verifiable network activity view;
- zero-copy/path-based ingestion with bounded memory and deterministic cleanup;
- first-run hardware/disk check and model recommendation with transparent tradeoffs;
- timestamp-linked playback, edit, autosave, and TXT/SRT/MD/JSON export;
- local evaluation report showing file, engine/model version, duration, processing time, and failures—without retaining raw content unless the user saves a project.

## 4. Value hypotheses and scorecard

These are targets for pilot decisions, not current performance claims.

| Scenario | Baseline | Product-assisted target | Evidence | Decision gate |
|---|---|---|---|---|
| First install to first completed transcript | User's current tool or manual setup | ≥80% of design partners complete without synchronous help; median ≤10 minutes excluding model download | Instrumented local event timings + observer checklist | 8/10 complete; zero critical privacy/lifecycle failures |
| Correct a 30-minute interview | Manual transcription or user's current product | ≥50% reduction in active correction time | Screen-recorded timing with consent; final edit distance/WER sample | Median target met across ≥10 tasks; no subgroup regression hidden |
| Local-only confidence | User's pre-task confidence | ≥4/5 post-task confidence and 100% network trace consistent with documented downloads only | Local connection log export + questionnaire | Every pilot run explains each connection; unexplained connection stops pilot |
| Transcript usefulness | Existing method | Reviewer usefulness ≥4/5 and evidence completeness ≥95% | Blind rubric on the same source and reference transcript | No unsupported product claim; results versioned by engine/model |
| Reliability | Existing app/manual process | ≥90% successful completion on supported pilot files | Manifested test corpus; outcome/error codes | 0 data-loss events; bounded retries; failure returns actionable state |
| Cost | Cloud plan or manual time | One-time pricing is preferred by ≥40% of qualified interviewees at tested price | Van Westendorp/interview + landing-page intent test | Pricing decision only after ≥20 qualified responses |

Required scorecard fields per run: scenario, baseline method, assisted method, active time, elapsed time, correction count, usefulness, confidence, evidence completeness, unsupported claim count, acceptance decision, app/engine/model/dataset/config versions.

## 5. Priority model

`Value score = (customer value + urgency + proof speed + risk reduction + dependency unlock) × confidence ÷ effort`

Each factor is 1–5, confidence is 0.50–0.95, and effort uses 1/2/3/5/8 story-point sizing. The score ranks economic attention; delivery sequence still respects dependencies and stop gates.

| Rank | Capability | Score | Delivery sequence | Why now |
|---:|---|---:|---:|---|
| 1 | Correct exports + editable timestamp transcript | 5.95 | 6 | Direct user outcome and fast proof; depends on reliable core. |
| 2 | Reproducible build/CI/release skeleton | 4.75 | 1 | Unlocks every credible test and release. |
| 3 | Bounded path-based ingest + temp lifecycle | 4.50 | 2 | Removes current correctness and memory blockers. |
| 4 | Authenticated sidecar lifecycle + cancellation | 3.91 | 3 | Reduces local attack, race, orphan, and wasted-work risk. |
| 5 | Model/runtime onboarding and integrity | 2.50 | 4 | Required for nontechnical first-run success. |
| 6 | Timestamp playback + correction workflow | 2.43 | 7 | Main rework/time-saving mechanism. |
| 7 | Deterministic evaluation harness | 2.34 | 5 | Converts accuracy/speed/privacy statements into evidence. |
| 8 | Crash recovery and local project save | 1.89 | 8 | Protects completed work and makes longer jobs usable. |
| 9 | Signed Windows design-partner beta | 1.61 | 9 | Tests demand only after technical proof. |
| 10 | Batch queue | 1.11 | 10, evidence-gated | Valuable to creators, but not required to prove the interview wedge. |
| 11 | macOS parity | 0.94 | 11, evidence-gated | Market exists, but competitive density is higher. |
| 12 | Diarization | 0.69 | Later experiment | High value in some interviews, high technical/quality uncertainty. |

## 6. Twelve-week roadmap

### Sprint 0 — Week 1: restore truth and reproducibility

- Create lockfiles, pin toolchains, add license decision, build script, icons/entitlements placeholders that cannot masquerade as signed release assets.
- Make CI test actual install, frontend checks, backend tests, Rust formatting/checks, and a package smoke build.
- Add stable error schema, correlation IDs, budget config, architecture decisions, and release checklist.
- Fix Python dependency installation or replace the current engine package only through a measured packaging spike.

**Exit gate:** green CI from a clean checkout; one documented command reproduces tests. No release claim.

### Sprint 1 — Weeks 2–3: safe golden path

- Replace browser/HTTP full-file copies with a least-privilege selected-path handoff or bounded streaming design.
- Keep temporary files alive until the generator completes; clean them on success, cancel, timeout, error, and restart.
- Use an ephemeral port and per-launch secret; health polling with timeout replaces fixed sleep.
- Tie window close and request cancel to child-process termination; add one-effect verification and stable reason codes.
- Bound duration/file size/resources before expensive work; provide truthful degraded/error states.

**Exit gate:** 1/10/30/120-minute fixtures complete or fail safely; memory stays within the platform threshold in `EVALUATION_PLAN.md`; no orphan sidecar/temp file.

### Sprint 2 — Weeks 4–5: install and first success

- Package the chosen inference engine and FFmpeg path reproducibly.
- Add model manifest, checksum, disk/RAM forecast, explicit download approval, retry/cancel/resume, and version display.
- Build a signed-internal Windows installer and clean-machine smoke test.
- Narrow Tauri permissions to explicitly selected files and app-owned storage.

**Exit gate:** internal A0 install and first transcript on two clean Windows hardware classes; every network connection attributable to an approved model/update operation.

### Sprint 3 — Weeks 6–7: usable transcript

- Editable segments, audio player, click-to-seek timestamps, keyboard navigation, accessible focus/status states.
- Correct TXT/SRT/MD/JSON export with round-trip tests; autosave only after the user opts to save a project.
- Crash recovery journal and explicit delete/clear action that propagates through projects, temp files, caches, and queued work.

**Exit gate:** rubric-based correction study on the versioned pilot set; zero export conformance failures.

### Sprint 4 — Weeks 8–9: evidence and design-partner alpha

- Run quality, latency, memory, disk, failure, cancellation, and privacy trace suites on two hardware tiers.
- Recruit 5–8 design partners; provide support and rollback; collect only consented aggregate evidence.
- Fix top task blockers; do not add batch, diarization, or AI summaries during alpha.

**Exit gate:** A1 gates pass and no open critical risk. Otherwise narrow or repeat.

### Sprint 5 — Weeks 10–12: beta and business decision

- Expand to 15–20 qualified pilot users only if A1 passes.
- Test onboarding, privacy proof presentation, and one-time price intent.
- Decide: Windows beta, another hardening cycle, pivot segment, or stop.
- macOS packaging spike is allowed only after the Windows value gate is met.

**Exit gate:** documented decision with adoption, quality, safety, cost, support burden, and claim-boundary evidence. A public launch is a separate approval.

## 7. A/B and product experiments

| Experiment | A | B | Primary metric | Guardrail | Minimum evidence |
|---|---|---|---|---|---|
| Onboarding | Automatic model recommendation | Recommendation plus visible speed/quality/disk explanation | First-transcript completion | Wrong-model/OOM rate | ≥20 qualified sessions; assignment logged |
| Privacy proof | Static “local only” copy | Expandable connection/activity panel | Confidence score and completion | No hidden/unexplained network call | ≥20 sessions; qualitative reason coding |
| Transcript correction | Segment list editor | Continuous document editor with timestamp gutter | Active correction time | Export correctness and accessibility | Same 10+ files/users in counterbalanced tasks |
| Pricing intent | Free core + optional supporter purchase | 14-day full trial then one-time license | Qualified purchase intent | No deceptive scarcity; refund clarity | ≥40 qualified landing/interview responses |

Experiments do not ship a winner on conversion alone. Hard privacy, data-loss, crash, or correctness regression rejects a variant.

## 8. Design-partner targets

These are archetypes to recruit, not claims that named organizations have agreed.

| Target archetype | Buyer | Workflow | Value hypothesis | Success metric | Support / rollback |
|---|---|---|---|---|---|
| JHU qualitative researcher | Principal investigator or research assistant | Consent-authorized research interviews | Local processing reduces upload concerns and correction effort | First success + ≥50% active-time reduction | Owner-led onboarding; uninstall/delete guide; revert to approved incumbent |
| Independent investigative journalist | Journalist/editor | Sensitive source interviews | Signed offline workflow improves source-control confidence | 4/5 confidence; no unexplained network events | Same-day support; original audio untouched; export to existing editor |
| Oral-history volunteer | Program lead/volunteer | Long archival interviews | Simple timestamps and correction reduce training burden | 80% unassisted completion | Sample-only pilot; preserve master file; manual workflow fallback |
| Interview-led podcaster | Creator | Recorded guest episode to show notes/subtitles | Local transcript lowers recurring cost and speeds edit prep | Completion reliability + correction time | Limit to transcript/subtitle step; return to current media editor |

Pilot boundaries: no clinical/legal suitability, no compliance certification, no promise of perfect speaker identity, no guarantee that local processing alone satisfies an organization's policy, and no proof of ROI beyond observed participants/tasks.

## 9. GTM and pricing hypothesis

- **Positioning:** “Private interview transcription for Windows—drop a file, keep it local, edit with timestamps.”
- **Proof package:** signed build identity, reproducible release manifest, network activity explanation, engine/model versions, supported-hardware matrix, benchmark report, known limitations, uninstall/delete guide.
- **Acquisition:** design-partner referrals, qualitative research communities, journalism/privacy communities, and a comparison page focused on workflow fit rather than competitor disparagement.
- **Pricing assumption:** test a free limited core or trial against a one-time $29–$59 license. No subscription is assumed unless ongoing cloud cost/value is deliberately introduced.
- **Support assumption:** one owner supports the first 20 users; measure minutes per successful activation and top failure categories before scale.

## 10. Now / next / later / not planned

| Now | Next, if evidence supports | Later experiment | Not planned for this product thesis |
|---|---|---|---|
| Reproducible build, safe ingest, lifecycle, model setup, editing/playback, exports, evaluation, signed Windows alpha | Project history, batch queue, glossary/hotwords, VTT/DOCX, GPU acceleration, macOS | Diarization, translation, watched folders, CLI, local summarization with separate consent/budget | Cloud transcription by default, team workspace, meeting bot, video editor, hidden telemetry, compliance certification, clinical/legal automation |

## 11. Claim boundaries

Until promotion evidence exists, approved language is limited to: **“Agdalus is being developed as a local-first desktop transcription tool. It is not yet released.”**

Do not claim that recordings never leave the device until clean-machine network traces show only documented, user-approved downloads/update checks and the app exposes the boundary truthfully. Do not claim signed installers, supported formats, clickable playback, accuracy, speed, time saved, lower cost, security, safety, accessibility, cross-platform support, or release readiness from code intent alone.
