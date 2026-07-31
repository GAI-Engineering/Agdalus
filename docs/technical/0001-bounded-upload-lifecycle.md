# Technical Design 0001: Bounded Upload and Response-Lifetime Workspace

## Scope

Implement the backend portion of AGD-002 and AGD-003 without changing the public `/transcribe` form contract.

## Data flow

1. Reject unsupported extension and a known oversize `UploadFile.size` before work.
2. Allocate an isolated app workspace.
3. Read the upload in 1 MiB chunks into the workspace, counting bytes before each write.
4. Retain only the first 12 header bytes for deterministic signature validation.
5. Reject oversize or invalid input and remove the partial workspace.
6. Extract WAV into the same workspace.
7. Return NDJSON through an iterator whose `finally` owns workspace cleanup.
8. Attach an idempotent background cleanup fallback for responses that finish without normal iterator exhaustion.
9. Close the framework upload handle after persistence, before inference streaming begins.

## Interfaces

- `_persist_upload(upload, destination, max_bytes, chunk_bytes) -> UploadReceipt`
- `UploadReceipt(bytes_written, header)`
- `_stream_with_cleanup(lines, cleanup) -> Iterator[str]`

## Budgets

- Upload read chunk: 1 MiB.
- Maximum accepted bytes: existing 2 GiB limit, enforced during the copy even if size metadata is missing.
- Signature memory: 12 bytes.
- Retry count: zero inside this boundary.
- FFmpeg timeout: existing 300 seconds; worker cancellation is a later slice.

## Acceptance evidence

- Unit: valid and invalid signatures, exact limit, limit+1 rejection, partial-file removal, header capture across small reads, cleanup on normal and exceptional iteration.
- Integration: synthetic WAV request streams NDJSON while the derived audio exists and removes the workspace after completion; invalid and oversize requests do not call extraction.
- Evaluation: a generated 32 MiB upload persists with traced Python peak allocation below 8 MiB and no single read request above 1 MiB.
- Static: Ruff passes; Pyright or equivalent type check passes for the backend slice.

## Claim boundary

Passing evidence proves bounded Python-side persistence and completed-response cleanup for the tested backend path. It does not prove frontend zero-copy, client-disconnect worker termination, transcription accuracy, packaged-app behavior, or release readiness.
