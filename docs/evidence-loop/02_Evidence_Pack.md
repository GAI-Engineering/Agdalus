# Evidence Pack

## Verified claims

| Claim | Statement | Source | Confidence | Assumptions | Engineering / risk implication |
|---|---|---|---:|---|---|
| CLM-001 | The baseline route returns a `StreamingResponse` from inside a `TemporaryDirectory` context, so cleanup occurs before lazy response iteration is guaranteed to finish. | SRC-001, `backend/main.py` at baseline | 5/5 | Starlette consumes the supplied iterator after the route returns. | R-03 requires response-lifetime cleanup. |
| CLM-002 | The baseline backend calls `await file.read()` without a size argument and therefore materializes the complete upload in one bytes object before enforcing the 2 GB limit. | SRC-001; SRC-003 documents sized reads | 5/5 | No middleware rejects the body earlier. | R-04 requires chunked bounded persistence. |
| CLM-003 | `UploadFile.read(size)` supports bounded asynchronous reads over its spooled file object. | SRC-003 | 5/5 | Installed FastAPI preserves the documented contract. | A chunked copy is a tried-and-true control for this slice. |
| CLM-004 | The baseline CI fails before tests because frontend lockfiles are absent and the Whisper source package build fails. | SRC-002 | 5/5 | The linked run corresponds to the baseline commit. | Test dependencies must be separated from the inference runtime; frontend lock must be generated. |
| CLM-005 | The implemented backend suite passes 24 tests with 80.62% line coverage of `backend.main` in the pinned Python 3.12 environment. | Loop-001 proof packet and JUnit artifact | 5/5 | Local clean environment matches declared pins; GitHub CI has not rerun. | AGD-002 can close; CI promotion remains conditional. |
| CLM-006 | A generated 32 MiB fixture measured 33,562,436 baseline peak traced bytes and 2,112,587 bounded peak traced bytes, a 15.89× reduction. | Reproducible evaluator and Loop-001 manifest | 5/5 | `tracemalloc` represents Python allocations, not total process RSS. | Backend memory target passes for this fixture; whole-app claim remains blocked. |
| CLM-007 | `npm ci`, `npm run check`, and `npm run build` now complete with zero Svelte errors or warnings. | Loop-001 proof packet; `package-lock.json` | 5/5 | Local Node 22 differs from CI Node 20. | Frontend build blocker is removed locally; CI confirmation remains. |
| CLM-008 | Integration tests prove the workspace exists during response iteration and is removed after normal completion; unit tests cover iterator failure and early close. | Loop-001 proof packet | 5/5 | Tests mock FFmpeg and Whisper to isolate lifecycle control. | R-03 is reduced for the tested boundary, not full worker cancellation. |

## Unsupported claims

- CLM-U01: The current packaged application successfully transcribes files. No packaged application evidence exists.
- CLM-U02: Whole-application memory is bounded for all supported sizes. Backend persistence is measured, but frontend copying and model residency remain.
- CLM-U03: Client disconnect always terminates Whisper/FFmpeg. This slice cleans resources around the response iterator but does not yet implement worker cancellation.

## Restricted-use boundaries

Evidence from synthetic fixtures may support implementation correctness and memory-behavior claims for the tested boundary. It does not support transcription accuracy, privacy certification, release readiness, production safety, or user ROI.
