from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import demo_fixture_backend


def test_demo_extract_audio_requires_validated_input(tmp_path: Path) -> None:
    output_path = tmp_path / "derived.wav"

    with pytest.raises(RuntimeError, match="validated demo input is missing"):
        demo_fixture_backend.demo_extract_audio(tmp_path / "missing.wav", output_path)

    assert not output_path.exists()


def test_demo_fixture_emits_stable_segment_and_done_contract(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "input.wav"
    input_path.write_bytes(b"RIFF0000WAVEfixture")
    derived_path = tmp_path / "derived.wav"
    demo_fixture_backend.demo_extract_audio(input_path, derived_path)
    monkeypatch.setattr(demo_fixture_backend.time, "sleep", lambda _seconds: None)

    events = [
        json.loads(line)
        for line in demo_fixture_backend.demo_transcribe_segments(
            derived_path,
            "en",
            "tiny",
        )
    ]

    assert len(events) == 5
    assert [event["type"] for event in events] == ["segment"] * 4 + ["done"]
    assert all(event["demo"] is True for event in events)
    assert [event["start"] for event in events[:4]] == [0.0, 4.2, 9.8, 15.4]
    assert events[-1] == {
        "type": "done",
        "language": "en",
        "model": "tiny",
        "demo": True,
    }
