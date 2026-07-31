# ADR-E001: Bounded Upload Persistence and Response-Owned Cleanup

- **Status:** Accepted for increment implementation
- **Deciders:** Product owner via current instruction; Codex as scoped implementation agent
- **Evidence:** CLM-001–003

## Options

1. Keep full-file buffering and extend the temporary-directory lifetime. This fixes only the early deletion defect and retains OOM risk.
2. Persist the `UploadFile` in fixed-size chunks, validate its captured header, and give the response iterator cleanup ownership. **Selected.**
3. Replace multipart upload with a Tauri file-path command now. This is the intended end-state for zero-copy desktop ingest but crosses Rust, permissions, UI, and security boundaries and is too large for the first proof loop.

## Consequences

The backend no longer requires a bytes object proportional to upload size. Cleanup runs after iteration and also has a response background fallback. The frontend still reads a selected path into a browser `File`, and cancellation still does not terminate FFmpeg/Whisper; those remain explicitly open.
