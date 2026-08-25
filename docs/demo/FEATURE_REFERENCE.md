# Agdalus feature and claim reference

Use this reference to decide what the product video may show and what the
narrator may claim. “Implemented” means the behavior exists in source. It does
not automatically mean the packaged desktop product has passed release gates.

## Recording-safe feature matrix

| Capability | Current surface | Evidence allowed in the video | Required wording or limitation |
|---|---|---|---|
| File intake | Drag/drop in the web UI; native picker code in Tauri | Show a WAV fixture being dropped | Browser recording does not prove native picker packaging |
| Format selection | MP4, M4A, MP3, WAV, FLAC, OGG, AAC, WMA filters/extensions | Say “the current interface accepts eight file extensions” | Do not say all formats transcribe successfully |
| File validation | Extension, byte budget, and selected magic-byte checks | Say “the backend rejects known oversize and invalid fixture inputs” | AAC/WMA validation is deferred to FFmpeg; FFmpeg is replaced in the demo |
| Language selection | Auto-detect plus ten named languages | Show the selector and name auto-detect | Do not claim measured quality for any language |
| Model selection | Auto, tiny, base, small, medium, large | Show the speed/quality labels | Labels are intent, not benchmark results |
| Transcript streaming | NDJSON events render segment-by-segment | Show the progress state, growing segment count, and persistent demo banner | Demo events carry `demo: true`; the UI labels them as deterministic, not Whisper output |
| Timestamped transcript | Segment start times and text are rendered | Show the completed fixture transcript | Editing and click-to-seek playback are roadmap items |
| Cancellation | UI aborts its HTTP request | Show the Cancel button only | Do not claim FFmpeg/Whisper worker termination |
| Export controls | Copy, TXT, SRT, and Markdown builders exist | Show the controls | Golden conformance and packaged download behavior are not yet proven |
| Bounded backend ingest | Upload persistence reads at most 1 MiB per request | Cite the 32 MiB allocation evaluation | Result is Python `tracemalloc`, not whole-process RSS |
| Workspace cleanup | Tested after completion, exception, and early iterator close | Cite fixture lifecycle tests | Client disconnect, process crash, and packaged sidecar cleanup remain open |
| Local architecture | Backend binds to `127.0.0.1` | Say “the current architecture uses a loopback backend” | Do not claim privacy certification or zero network activity |

## Evidence numbers approved for narration

| Claim | Value | Source | Boundary |
|---|---:|---|---|
| Automated tests | 24 passed, 0 failed | [Run manifest](../evidence/runs/2026-07-31-loop-001/RUN_MANIFEST.json) | Backend unit, integration, and allocation evaluation tests |
| Backend coverage | 80.62% | [Proof packet](../evidence/runs/2026-07-31-loop-001/PROOF_PACKET.md) | `backend.main`, not whole repository |
| Traced allocation reduction | 15.89x | [Proof packet](../evidence/runs/2026-07-31-loop-001/PROOF_PACKET.md) | 32 MiB synthetic fixture; Python allocation only |
| Maximum requested read | 1,048,576 bytes | [Proof packet](../evidence/runs/2026-07-31-loop-001/PROOF_PACKET.md) | Backend upload persistence path |
| Static quality gates | Ruff, Pyright, Svelte, and Vite passed | [Proof packet](../evidence/runs/2026-07-31-loop-001/PROOF_PACKET.md) | Does not include Rust/Tauri packaging |
| Promotion decision | Proceed with conditions | [Audit report](../evidence/runs/2026-07-31-loop-001/AUDIT_READINESS_REPORT.md) | Not release approval |

## Phrases to avoid

Do not use these phrases until their promotion gates pass:

- “Your recordings never leave your device.”
- “Production-ready,” “secure,” “private,” or “certified.”
- “Accurate transcription” or any speed/quality comparison.
- “Works on Windows/macOS” or “signed installer.”
- “Cancellation stops all processing.”
- “All supported formats work.”
- Any time-saved, ROI, adoption, or pricing conclusion.

## Current product story

Agdalus is being developed as a focused, local-first transcription workspace for
privacy-sensitive interview workflows. The current slice proves a bounded
backend intake and response-lifetime cleanup design, exposes a compact transcript
interface, and establishes reproducible engineering evidence. The next product
gates are selected-path ingestion, worker cancellation, authenticated sidecar
lifecycle, packaged inference, export conformance, and clean-machine desktop UAT.
