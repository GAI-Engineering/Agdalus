"""Agdalus local transcription server.

Runs as a Tauri sidecar, bound to 127.0.0.1 only. Receives audio/video files
from the Svelte frontend, transcribes them with Whisper, and streams segments
back as newline-delimited JSON (NDJSON).

No auth, no sessions, no job IDs — consumer product, single user, local only.
"""
from __future__ import annotations

import os
import struct
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Iterator

import uvicorn
import whisper
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# ── Constants ──────────────────────────────────────────────────────────────────

SUPPORTED_EXTENSIONS = {".mp4", ".m4a", ".mp3", ".wav", ".flac", ".ogg", ".aac", ".wma"}
MAX_FILE_BYTES = 2 * 1024 * 1024 * 1024  # 2 GB
MODELS_DIR = Path.home() / ".agdalus" / "models"

# Auto-select model by available RAM (rough heuristic)
def _auto_model() -> str:
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / 1e9
    except ImportError:
        ram_gb = 8  # assume 8 GB if psutil not available
    if ram_gb >= 16:
        return "small"
    if ram_gb >= 8:
        return "base"
    return "tiny"

VALID_MODELS = {"tiny", "base", "small", "medium", "large"}

# ── Format validation (magic bytes) ──────────────────────────────────────────

def _validate_signature(data: bytes, ext: str) -> None:
    """Raise HTTPException if file header doesn't match expected format."""
    if len(data) < 12:
        raise HTTPException(400, f"File too small to be a valid {ext} file.")
    if ext in {".mp4", ".m4a"}:
        if data[4:8] != b"ftyp":
            raise HTTPException(400, f"Not a valid {ext} file (missing ftyp box).")
    elif ext == ".wav":
        if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
            raise HTTPException(400, "Not a valid WAV file (missing RIFF/WAVE header).")
    elif ext == ".mp3":
        if not (data[:3] == b"ID3" or (data[0] == 0xFF and (data[1] & 0xE0) == 0xE0)):
            raise HTTPException(400, "Not a valid MP3 file.")
    elif ext == ".flac":
        if data[:4] != b"fLaC":
            raise HTTPException(400, "Not a valid FLAC file (missing fLaC marker).")
    elif ext == ".ogg":
        if data[:4] != b"OggS":
            raise HTTPException(400, "Not a valid OGG file (missing OggS marker).")
    # AAC and WMA: deferred to FFprobe; no reliable magic byte for all variants

# ── Audio extraction ──────────────────────────────────────────────────────────

def _extract_audio(input_path: Path, output_path: Path) -> None:
    """Run FFmpeg to extract 16kHz mono WAV from any supported container."""
    result = subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(input_path),
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "16000", "-ac", "1",
            str(output_path),
        ],
        capture_output=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise HTTPException(
            422,
            f"FFmpeg could not extract audio: {result.stderr.decode(errors='replace')[:200]}",
        )

# ── Transcription ──────────────────────────────────────────────────────────────

_model_cache: dict[str, whisper.Whisper] = {}
_model_lock = threading.Lock()

def _load_model(name: str) -> whisper.Whisper:
    with _model_lock:
        if name not in _model_cache:
            _model_cache[name] = whisper.load_model(name, download_root=str(MODELS_DIR))
        return _model_cache[name]

def _transcribe_segments(
    audio_path: Path,
    language: str | None,
    model_name: str,
) -> Iterator[str]:
    """Yield NDJSON lines: one per segment + a final summary line."""
    import json

    model = _load_model(model_name)
    result = model.transcribe(
        str(audio_path),
        language=language or None,
        word_timestamps=False,
        verbose=False,
    )
    for seg in result["segments"]:
        line = json.dumps({
            "type": "segment",
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"].strip(),
            "confidence": round(
                # avg_logprob → 0-1 confidence approximation
                min(1.0, max(0.0, (seg.get("avg_logprob", -1.0) + 1.0))),
                3,
            ),
        })
        yield line + "\n"

    yield json.dumps({
        "type": "done",
        "language": result.get("language", language or "unknown"),
        "model": model_name,
    }) + "\n"

# ── App ────────────────────────────────────────────────────────────────────────

app = FastAPI(title="Agdalus", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["tauri://localhost", "http://localhost:1420", "http://127.0.0.1:1420"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "auto_model": _auto_model()}


@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    language: str = Form(default=""),
    model: str = Form(default=""),
) -> StreamingResponse:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported format: {ext or '(no extension)'}")

    model_name = model.strip() if model.strip() in VALID_MODELS else _auto_model()
    lang = language.strip() or None

    data = await file.read()
    if len(data) > MAX_FILE_BYTES:
        raise HTTPException(413, "File exceeds 2 GB limit.")
    _validate_signature(data, ext)

    with tempfile.TemporaryDirectory(prefix="agdalus_") as tmp:
        tmp_path = Path(tmp)
        input_file = tmp_path / f"input{ext}"
        input_file.write_bytes(data)
        audio_file = tmp_path / "audio.wav"
        _extract_audio(input_file, audio_file)

        return StreamingResponse(
            _transcribe_segments(audio_file, lang, model_name),
            media_type="application/x-ndjson",
        )


if __name__ == "__main__":
    port = int(os.environ.get("AGDALUS_PORT", "54321"))
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
