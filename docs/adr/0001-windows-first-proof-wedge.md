# ADR-0001: Windows-First Proof Wedge and Evidence-Gated Expansion

- **Status:** Accepted for planning
- **Date:** 2026-07-31
- **Decision owners:** Product and engineering owner
- **Baseline:** `37c9d13f4752ba5bfb50091c7ee5affe19686ea0`

## Context

The scaffold names Windows and macOS, a Python Whisper sidecar, and a broad set of transcription features. The repository has no green build or packaged sidecar, and mature alternatives already cover Mac and cross-platform offline transcription. Pursuing platform and feature breadth now would delay proof of a trustworthy end-to-end workflow.

## Decision

For the first 12 weeks, optimize for one vertical slice: a privacy-sensitive Windows interviewer installs Agdalus, explicitly obtains a verified local model, selects a file, receives an editable timestamped transcript, corrects it with synchronized playback, exports it, and can inspect/delete local artifacts.

Architecture remains Tauri + Svelte for the shell/UI during the first proof cycle. The inference engine is **not** permanently decided: current OpenAI Whisper/Python, faster-whisper, and whisper.cpp must be compared through AGD-005. The selected engine must satisfy packaging, license, quality, latency, memory, integrity, and GPU/CPU fallback gates.

macOS, batch, diarization, cloud features, and LLM summarization are gated on Windows value evidence and separate scope decisions.

## Consequences

- Faster route to reproducible value and clearer design-partner recruitment.
- Signed Windows packaging and local boundary evidence become product work, not release polish.
- Some existing README claims are narrowed until implemented and verified.
- macOS momentum is intentionally deferred despite existing config.
- The inference engine may change, accepting near-term spike cost to avoid locking in an unpackageable runtime.

## Revisit triggers

- Engine spike shows no feasible Windows package.
- Fewer than 5 qualified Windows design partners can be recruited.
- Pilot data shows privacy/local control is not a meaningful switching trigger.
- Support burden or hardware failure rate makes the consumer model unsustainable.
- A material legal/license constraint invalidates the distribution model.
