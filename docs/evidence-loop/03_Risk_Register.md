# Increment Risk Register

| Risk | Likelihood | Impact | Evidence | Control in this increment | Residual state |
|---|---:|---:|---|---|---|
| R-03 Temporary input removed too early | 2 | 5 | CLM-001, CLM-008 | Response-owned cleanup wrapper, background fallback, normal/error/early-close assertions | Reduced for backend stream lifecycle; process cancellation remains |
| R-04 Full upload allocation / OOM | 3 | 5 | CLM-002, CLM-003, CLM-006 | Fixed-size reads, byte counter, early known-size rejection, partial-file cleanup | Backend reduced; frontend still copies selected path into a `File` |
| R-10 Invalid media accepted | 3 | 4 | SRC-001 | Validate the captured header after bounded persistence | AAC/WMA remain delegated to FFmpeg |
| R-12 Unsupported proof claim | 3 | 4 | CLM-U01–U03 | Scope evidence to the backend ingest/lifecycle slice | Release and privacy claims remain blocked |
