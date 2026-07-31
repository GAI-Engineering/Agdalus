from __future__ import annotations

import asyncio
import tracemalloc
from pathlib import Path

import pytest

from backend import main


class GeneratedUpload:
    """Generate bytes per read so the test never holds the full fixture in memory."""

    def __init__(self, total_bytes: int) -> None:
        self.remaining = total_bytes
        self.max_requested = 0

    async def read(self, size: int) -> bytes:
        self.max_requested = max(self.max_requested, size)
        take = min(size, self.remaining)
        self.remaining -= take
        return b"x" * take


@pytest.mark.evaluation
def test_32_mib_persistence_has_bounded_python_allocation(tmp_path: Path) -> None:
    total_bytes = 32 * 1024 * 1024
    upload = GeneratedUpload(total_bytes)
    destination = tmp_path / "generated.bin"

    tracemalloc.start()
    try:
        receipt = asyncio.run(
            main._persist_upload(
                upload,
                destination,
                max_bytes=total_bytes,
                chunk_bytes=main.UPLOAD_CHUNK_BYTES,
            )
        )
        _, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    assert receipt.bytes_written == total_bytes
    assert destination.stat().st_size == total_bytes
    assert upload.max_requested <= 1024 * 1024
    assert peak_bytes < 8 * 1024 * 1024
