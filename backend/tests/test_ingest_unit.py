from __future__ import annotations

import asyncio
import io
import tempfile
from pathlib import Path

import pytest
from fastapi import HTTPException, UploadFile

from backend import main


def _upload(data: bytes, filename: str = "sample.wav") -> UploadFile:
    return UploadFile(file=io.BytesIO(data), filename=filename, size=len(data))


def test_persist_upload_captures_header_across_small_chunks(tmp_path: Path) -> None:
    data = b"RIFF" + b"1234" + b"WAVE" + b"payload"
    destination = tmp_path / "input.wav"

    receipt = asyncio.run(
        main._persist_upload(
            _upload(data),
            destination,
            max_bytes=len(data),
            chunk_bytes=2,
        )
    )

    assert receipt.bytes_written == len(data)
    assert receipt.header == data[:12]
    assert destination.read_bytes() == data


def test_persist_upload_accepts_exact_byte_limit(tmp_path: Path) -> None:
    data = b"x" * 9
    destination = tmp_path / "exact.bin"

    receipt = asyncio.run(
        main._persist_upload(_upload(data), destination, max_bytes=9, chunk_bytes=4)
    )

    assert receipt.bytes_written == 9
    assert destination.read_bytes() == data


def test_persist_upload_rejects_limit_plus_one_and_removes_partial_file(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "partial.bin"

    with pytest.raises(HTTPException) as exc:
        asyncio.run(
            main._persist_upload(
                _upload(b"x" * 10),
                destination,
                max_bytes=9,
                chunk_bytes=4,
            )
        )

    assert exc.value.status_code == 413
    assert not destination.exists()


@pytest.mark.parametrize(
    ("extension", "header"),
    [
        (".wav", b"RIFF0000WAVE"),
        (".mp4", b"0000ftyp0000"),
        (".m4a", b"0000ftyp0000"),
        (".mp3", b"ID3" + b"0" * 9),
        (".flac", b"fLaC" + b"0" * 8),
        (".ogg", b"OggS" + b"0" * 8),
        (".aac", b"0" * 12),
        (".wma", b"0" * 12),
    ],
)
def test_validate_signature_accepts_supported_header(extension: str, header: bytes) -> None:
    main._validate_signature(header, extension)


@pytest.mark.parametrize(
    ("extension", "header"),
    [
        (".wav", b"NOPE0000WAVE"),
        (".mp4", b"0000nope0000"),
        (".mp3", b"NOPE" + b"0" * 8),
        (".flac", b"NOPE" + b"0" * 8),
        (".ogg", b"NOPE" + b"0" * 8),
    ],
)
def test_validate_signature_rejects_invalid_header(extension: str, header: bytes) -> None:
    with pytest.raises(HTTPException) as exc:
        main._validate_signature(header, extension)

    assert exc.value.status_code == 400


def test_stream_cleanup_runs_after_last_line() -> None:
    workspace = tempfile.TemporaryDirectory(prefix="agdalus_test_")
    marker = Path(workspace.name) / "alive"
    marker.write_text("yes", encoding="utf-8")

    def lines():
        assert marker.exists()
        yield "one\n"
        assert marker.exists()
        yield "two\n"

    assert list(main._stream_with_cleanup(lines(), workspace.cleanup)) == ["one\n", "two\n"]
    assert not marker.parent.exists()


def test_stream_cleanup_runs_when_iterator_raises() -> None:
    workspace = tempfile.TemporaryDirectory(prefix="agdalus_test_")
    root = Path(workspace.name)

    def lines():
        yield "one\n"
        raise RuntimeError("synthetic stream failure")

    with pytest.raises(RuntimeError, match="synthetic stream failure"):
        list(main._stream_with_cleanup(lines(), workspace.cleanup))

    assert not root.exists()


def test_stream_cleanup_runs_when_consumer_closes_early() -> None:
    workspace = tempfile.TemporaryDirectory(prefix="agdalus_test_")
    root = Path(workspace.name)
    stream = main._stream_with_cleanup(iter(["one\n", "two\n"]), workspace.cleanup)

    assert next(stream) == "one\n"
    assert root.exists()
    stream.close()

    assert not root.exists()
