# Agdalus

Local-first audio transcription for individuals. Drag a file in, get readable text out. Your recordings never leave your device.

**Status:** Early development — not yet released.

## What it does

- Transcribe MP4, M4A, MP3, WAV, FLAC, OGG, AAC, WMA files locally
- Per-segment timestamps, clickable playback sync
- Export as plain text, SRT subtitles, Markdown, or JSON
- English, Spanish, French, German, and more via Whisper
- Auto-selects model size based on available RAM

## Architecture

```
Agdalus/
  backend/        Python — FastAPI transcription server (Whisper + FFmpeg)
  src/            SvelteKit frontend
  src-tauri/      Tauri 2 Rust shell (window, file dialogs, sidecar lifecycle)
  docs/
```

The Python backend runs as a Tauri sidecar process bound to 127.0.0.1. The Rust shell manages its lifecycle and provides native drag-drop and file-dialog APIs. All audio processing happens on-device.

## Development setup

### Prerequisites

- Rust + Cargo (https://rustup.rs)
- Node.js 20+
- Python 3.11+
- FFmpeg on PATH

### Install

```bash
# Frontend dependencies
npm install

# Python backend
cd backend
python -m venv .venv
.venv/Scripts/activate        # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
cd ..

# Run in dev mode (Tauri launches backend automatically)
npm run tauri dev
```

### Build

```bash
npm run tauri build
```

Produces a signed installer for the current platform. CI builds for both Mac and Windows via `.github/workflows/release.yml`.

## Relationship to Verbatim

Agdalus shares the audio validation and Whisper runner patterns pioneered in [Verbatim](https://github.com/muammarlone/Verbatim), the enterprise transcription studio. Verbatim targets managed corporate endpoints with full governance gates. Agdalus strips that layer entirely — no evidence trails, no compliance gates, no credential lockers — and adds native cross-platform desktop packaging for individual users.

## License

TBD
