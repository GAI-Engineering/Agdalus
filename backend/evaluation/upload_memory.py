"""Compare baseline full-read allocation with bounded upload persistence."""

from __future__ import annotations

import argparse
import asyncio
import json
import tempfile
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path

from backend import main


class GeneratedUpload:
    def __init__(self, total_bytes: int) -> None:
        self.remaining = total_bytes
        self.max_requested = 0

    async def read(self, size: int = -1) -> bytes:
        self.max_requested = max(self.max_requested, size)
        take = self.remaining if size < 0 else min(size, self.remaining)
        self.remaining -= take
        return b"x" * take


@dataclass(frozen=True)
class EvaluationResult:
    fixture_bytes: int
    chunk_bytes: int
    baseline_peak_bytes: int
    bounded_peak_bytes: int
    peak_reduction_ratio: float
    baseline_elapsed_seconds: float
    bounded_elapsed_seconds: float
    bounded_bytes_written: int
    maximum_read_request_bytes: int


async def _baseline_full_read(upload: GeneratedUpload) -> int:
    return len(await upload.read())


def _measure(coro) -> tuple[object, int, float]:
    tracemalloc.start()
    started = time.perf_counter()
    try:
        result = asyncio.run(coro)
        elapsed = time.perf_counter() - started
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return result, peak, elapsed


def evaluate(total_bytes: int, chunk_bytes: int) -> EvaluationResult:
    baseline_upload = GeneratedUpload(total_bytes)
    baseline_size, baseline_peak, baseline_elapsed = _measure(_baseline_full_read(baseline_upload))
    if baseline_size != total_bytes:
        raise RuntimeError("baseline fixture generation was incomplete")

    bounded_upload = GeneratedUpload(total_bytes)
    with tempfile.TemporaryDirectory(prefix="agdalus_eval_") as workspace:
        destination = Path(workspace) / "generated.bin"
        receipt, bounded_peak, bounded_elapsed = _measure(
            main._persist_upload(
                bounded_upload,
                destination,
                max_bytes=total_bytes,
                chunk_bytes=chunk_bytes,
            )
        )
        if not isinstance(receipt, main.UploadReceipt):
            raise RuntimeError("bounded persistence returned an invalid receipt")
        if destination.stat().st_size != total_bytes:
            raise RuntimeError("bounded fixture persistence was incomplete")

    return EvaluationResult(
        fixture_bytes=total_bytes,
        chunk_bytes=chunk_bytes,
        baseline_peak_bytes=baseline_peak,
        bounded_peak_bytes=bounded_peak,
        peak_reduction_ratio=round(baseline_peak / max(bounded_peak, 1), 2),
        baseline_elapsed_seconds=round(baseline_elapsed, 4),
        bounded_elapsed_seconds=round(bounded_elapsed, 4),
        bounded_bytes_written=receipt.bytes_written,
        maximum_read_request_bytes=bounded_upload.max_requested,
    )


def main_cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size-mib", type=int, default=32)
    parser.add_argument("--chunk-mib", type=int, default=1)
    args = parser.parse_args()
    if args.size_mib <= 0 or args.chunk_mib <= 0:
        parser.error("sizes must be positive")

    result = evaluate(args.size_mib * 1024 * 1024, args.chunk_mib * 1024 * 1024)
    print(json.dumps(asdict(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main_cli()
