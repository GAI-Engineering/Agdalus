# Fixture UAT Report: Loop 001

## Workflow

POST a synthetic valid WAV multipart upload to `/transcribe`; replace FFmpeg and Whisper with deterministic fixtures; verify NDJSON segment and done events; verify input/derived files exist at each stream yield; verify workspace removal after response completion.

## Results

| Scenario | Result |
|---|---|
| Valid WAV, normal response | Pass |
| Invalid WAV signature | Pass: HTTP 400; extraction not called |
| Known oversize upload | Pass: HTTP 413; extraction not called |
| Extraction exception | Pass: HTTP 500; workspace removed |
| Iterator exception | Pass: cleanup runs |
| Consumer closes iterator early | Pass: cleanup runs |

## Boundary

This is fixture UAT of the backend contract, not end-user desktop UAT. FFmpeg, Whisper, Tauri, installer, model download, client network disconnect, and real media quality remain untested in this run.
