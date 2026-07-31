from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from fastapi.testclient import TestClient

from backend import main

VALID_WAV = b"RIFF" + b"0000" + b"WAVE" + b"synthetic-payload"


def test_transcribe_stream_keeps_workspace_alive_then_cleans_it(monkeypatch) -> None:
    observed: dict[str, Path] = {}

    def fake_extract(input_path: Path, output_path: Path) -> None:
        assert input_path.exists()
        output_path.write_bytes(b"synthetic-wave")

    def fake_segments(
        audio_path: Path,
        language: str | None,
        model_name: str,
    ) -> Iterator[str]:
        observed["workspace"] = audio_path.parent
        assert audio_path.exists()
        yield (
            json.dumps(
                {"type": "segment", "start": 0.0, "end": 1.0, "text": "hello", "confidence": 0.9}
            )
            + "\n"
        )
        assert audio_path.exists()
        yield json.dumps({"type": "done", "language": language or "en", "model": model_name}) + "\n"

    monkeypatch.setattr(main, "_extract_audio", fake_extract)
    monkeypatch.setattr(main, "_transcribe_segments", fake_segments)

    with TestClient(main.app) as client:
        response = client.post(
            "/transcribe",
            files={"file": ("sample.wav", VALID_WAV, "audio/wav")},
            data={"language": "en", "model": "tiny"},
        )

    assert response.status_code == 200
    events = [json.loads(line) for line in response.text.splitlines()]
    assert [event["type"] for event in events] == ["segment", "done"]
    assert not observed["workspace"].exists()


def test_invalid_signature_never_calls_extraction(monkeypatch) -> None:
    def forbidden_extract(_input_path: Path, _output_path: Path) -> None:
        raise AssertionError("extraction must not run for invalid input")

    monkeypatch.setattr(main, "_extract_audio", forbidden_extract)

    with TestClient(main.app) as client:
        response = client.post(
            "/transcribe",
            files={"file": ("sample.wav", b"NOPE0000WAVEpayload", "audio/wav")},
        )

    assert response.status_code == 400
    assert "valid WAV" in response.json()["detail"]


def test_oversize_metadata_is_rejected_before_extraction(monkeypatch) -> None:
    monkeypatch.setattr(main, "MAX_FILE_BYTES", 12)

    def forbidden_extract(_input_path: Path, _output_path: Path) -> None:
        raise AssertionError("extraction must not run for oversize input")

    monkeypatch.setattr(main, "_extract_audio", forbidden_extract)

    with TestClient(main.app) as client:
        response = client.post(
            "/transcribe",
            files={"file": ("sample.wav", VALID_WAV, "audio/wav")},
        )

    assert response.status_code == 413


def test_extraction_failure_removes_workspace(monkeypatch) -> None:
    observed: dict[str, Path] = {}

    def failing_extract(input_path: Path, _output_path: Path) -> None:
        observed["workspace"] = input_path.parent
        raise RuntimeError("synthetic extraction failure")

    monkeypatch.setattr(main, "_extract_audio", failing_extract)

    with TestClient(main.app, raise_server_exceptions=False) as client:
        response = client.post(
            "/transcribe",
            files={"file": ("sample.wav", VALID_WAV, "audio/wav")},
        )

    assert response.status_code == 500
    assert not observed["workspace"].exists()
