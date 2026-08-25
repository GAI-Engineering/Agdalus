# Three-minute Agdalus product video script

## Video objective

Show the product thesis, current interface, deterministic end-to-end fixture,
engineering evidence, and next release conditions in under three minutes. The
viewer should understand both the value proposition and the exact maturity level.

Target length: 2:45 to 3:00. Record at 1280 x 720, 30 fps, browser zoom 100%.

## Storyboard and voiceover

| Time | Picture | Presenter action | Voiceover / on-screen copy | Evidence |
|---:|---|---|---|---|
| 0:00–0:05 | Black disclosure slate | Hold for five seconds | **On screen:** “Development evidence demo. Deterministic transcript fixture. FFmpeg, Whisper, and desktop packaging are not exercised.” | Claim boundary |
| 0:05–0:18 | Title: “Agdalus” over idle UI | Fade into the product | “Agdalus is being developed as a focused, local-first transcription workspace for people working with sensitive interviews and recordings.” | Product thesis, not release claim |
| 0:18–0:34 | Idle desktop state | Move pointer across the drop zone | “The experience starts with one job: choose an audio or video file, select a language and model preference, and turn the result into readable, timestamped text.” | Current UI and intended workflow |
| 0:34–0:50 | Drop `interview-demo.wav` | Drag the fixture into the drop zone | “For this recording I am using a deterministic WAV fixture. The backend still performs extension, size, header, bounded-copy, and cleanup behavior.” | Fixture backend boundary |
| 0:50–1:05 | Language/model selectors | Open each selector briefly; leave Auto selected | “The interface exposes auto-detection plus ten named languages, and six model choices from automatic selection through the larger model tiers. These labels are options, not benchmark claims.” | Source-defined controls |
| 1:05–1:30 | Click Transcribe; show progress | Let at least two segments arrive | “Segments stream into the interface as newline-delimited events. The words you see are deterministic fixture content; this shot demonstrates the upload and streaming contract, not Whisper accuracy.” | Real streaming path, synthetic inference |
| 1:30–1:48 | Completed transcript | Hover over timestamped rows | “The current result view presents timestamped segments, detected language, and the selected model in one compact workspace.” | Current UI |
| 1:48–2:02 | Export controls | Point to Copy, TXT, SRT, and MD | “The frontend includes copy, plain text, SRT subtitle, and Markdown export actions. Golden export conformance and packaged desktop downloads remain promotion gates.” | Implemented builders, bounded claim |
| 2:02–2:28 | Open `evidence-slide.html` | Pause on each metric | “The first engineering loop produced 24 passing tests and 80.62 percent coverage of the backend module. On a 32 mebibyte synthetic fixture, bounded persistence reduced traced Python peak allocation by 15.89 times, with one-mebibyte maximum read requests.” | Loop 001 proof packet |
| 2:28–2:45 | Evidence slide, limitations panel | Highlight “Proceed with conditions” | “That is evidence for one backend slice, not a release approval. Packaged inference, whole-process memory, authenticated sidecar startup, worker cancellation, and clean-machine desktop testing remain open.” | Audit readiness report |
| 2:45–2:58 | Return to completed transcript | Slow zoom out | “Agdalus now has a measurable foundation: a focused workflow, bounded intake, deterministic cleanup, and explicit gates for the work that comes next.” | Synthesis |
| 2:58–3:00 | End card | Fade to black | **On screen:** “Agdalus 0.1 development evidence demo • Loop 001” | Versioned close |

## Presenter notes

- Speak at 125–140 words per minute.
- Keep the cursor still while speaking; move only when the script names an action.
- Never hide the opening disclosure or remove the fixture qualification.
- Do not open the native “Browse files” dialog in a normal browser. Drag the
  generated fixture file from Explorer instead.
- If the stream completes too quickly, restart the fixture backend. It emits one
  segment every 450 milliseconds.
- Use the [feature reference](FEATURE_REFERENCE.md) for Q&A after the video.

## Short 45-second cut

“Agdalus is being developed as a focused, local-first transcription workspace.
This development demo uses deterministic transcript content, replacing FFmpeg
and Whisper while retaining the real upload, streaming, and cleanup paths. The
interface accepts a recording, exposes language and model choices, streams
timestamped segments, and provides copy, TXT, SRT, and Markdown actions. The
first engineering loop produced 24 passing tests, 80.62 percent coverage of the
backend module, and a 15.89-times reduction in traced Python peak allocation for
a 32-mebibyte fixture. The decision is proceed with conditions, not release:
packaged inference, cancellation, sidecar authentication, and desktop UAT remain
open.”
