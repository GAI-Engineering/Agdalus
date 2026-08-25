"""Run Agdalus with deterministic transcript events for product recording.

This helper exercises the real upload validation, bounded persistence, NDJSON
streaming, and workspace cleanup paths. It replaces FFmpeg and Whisper only.
It is a recording fixture, not evidence of packaged inference or accuracy.
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Iterator
from pathlib import Path

import uvicorn

from backend import main

DEMO_SEGMENTS = (
    (0.0, 4.2, "Agdalus turns a local recording into a timestamped transcript."),
    (4.2, 9.8, "The current interface supports language and model selection."),
    (9.8, 15.4, "Transcript segments stream into the workspace as they become available."),
    (15.4, 21.0, "You can copy the result or export TXT, SRT, and Markdown files."),
)


def demo_extract_audio(input_path: Path, output_path: Path) -> None:
    """Create a deterministic derived artifact after real input validation."""
    if not input_path.is_file():
        raise RuntimeError("validated demo input is missing")
    output_path.write_bytes(b"agdalus-demo-derived-audio")


def demo_transcribe_segments(
    audio_path: Path,
    language: str | None,
    model_name: str,
) -> Iterator[str]:
    """Yield stable NDJSON events slowly enough to record the streaming state."""
    if not audio_path.is_file():
        raise RuntimeError("derived demo audio is missing")

    for start, end, text in DEMO_SEGMENTS:
        time.sleep(0.45)
        yield (
            json.dumps(
                {
                    "type": "segment",
                    "start": start,
                    "end": end,
                    "text": text,
                    "confidence": 0.92,
                    "demo": True,
                }
            )
            + "\n"
        )

    yield (
        json.dumps(
            {
                "type": "done",
                "language": language or "en",
                "model": model_name,
                "demo": True,
            }
        )
        + "\n"
    )


def run() -> None:
    """Bind the fixture server to loopback on the configured demo port."""
    port = int(os.environ.get("AGDALUS_PORT", "54321"))
    main._extract_audio = demo_extract_audio
    main._transcribe_segments = demo_transcribe_segments
    print(
        "Agdalus deterministic recording fixture: FFmpeg and Whisper are replaced; "
        "upload/lifecycle behavior remains real.",
        flush=True,
    )
    uvicorn.run(main.app, host="127.0.0.1", port=port, log_level="warning")


if __name__ == "__main__":
    run()
