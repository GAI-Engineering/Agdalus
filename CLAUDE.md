# Agdalus — Development Notes

Consumer-grade local transcription app. Separate product from Verbatim (enterprise).
Shared concept: local Whisper + FFmpeg. Different: no governance gates, no corporate
compliance, cross-platform (Mac + Windows), Tauri 2 + SvelteKit + Python backend.

## Architecture

```
backend/main.py       FastAPI sidecar — transcription only, 127.0.0.1
src/routes/+page.svelte  Single-page UI — drop zone + transcript view
src-tauri/src/lib.rs  Tauri shell — backend lifecycle, file dialogs, FS
```

## Stack decisions (principal architect, 2026-07-31)

- **Tauri 2** over Electron: binary size (10 MB vs 150 MB), cold start, system webview
- **SvelteKit** with static adapter: matches Tauri's asset model
- **Python FastAPI sidecar**: reuses Whisper/FFmpeg patterns from Verbatim; keeps
  ML dependencies out of Rust
- **NDJSON streaming** from backend: segments appear as they're produced, no polling
- **Auto model selection**: tiny/base/small by RAM — consumer hardware varies wildly

## What this is NOT

- Not a replacement for Verbatim. Verbatim stays enterprise-only.
- No governance gates, no evidence trails, no compliance theater.
- No cloud transcription. Ever. Privacy is the product.
- No Teams/Zoom connector (consumer doesn't need corporate meeting retrieval).

## Development quick start

```bash
npm install
cd backend && pip install -r requirements.txt && cd ..
npm run tauri:dev
```

## Key consumer UX principles

1. Drop file → transcribes. Zero ceremony.
2. No authorization dialog. No session management. No job IDs.
3. Model auto-selected by RAM; user can override.
4. Export: TXT, SRT, MD. Copy to clipboard. That's it.
5. App is 1 window. 1 page. No settings screen in MVP.
