# Proof Packet: Loop 001

## Reproduce

```powershell
py -3.12 -m venv .venv-test
.\.venv-test\Scripts\python.exe -m pip install -r backend\requirements-test.txt
.\.venv-test\Scripts\ruff.exe check backend\
.\.venv-test\Scripts\ruff.exe format --check backend\
.\.venv-test\Scripts\python.exe -m pytest -q --cov=backend.main --cov-report=term-missing --cov-fail-under=80
.\.venv-test\Scripts\pyright.exe backend\
.\.venv-test\Scripts\python.exe -m backend.evaluation.upload_memory --size-mib 32 --chunk-mib 1
npm ci --ignore-scripts --no-audit --no-fund
npm run check
npm run build
```

## Observed evidence

- Tests: 24 passed in 1.42 seconds under the pinned Python 3.12 environment.
- Coverage: 80.62% of `backend.main`; enforced minimum 80%.
- Ruff: zero findings; formatting check passes.
- Pyright: zero errors, warnings, or information findings.
- Svelte: zero errors and zero warnings.
- Vite static build: pass.
- Memory comparison: 33,562,436 baseline peak traced bytes versus 2,112,587 bounded peak traced bytes for 32 MiB; 15.89x reduction; maximum requested read 1,048,576 bytes.
- Lifecycle: integration/unit fixtures verify live workspace during yields and cleanup after completion, exception, and early consumer close.

## Proof limitations

`tracemalloc` does not measure native model memory or total RSS. API integration mocks FFmpeg and Whisper. Local Node is 22 while CI declares Node 20. Rust and a packaged sidecar were not built. The GitHub workflow change has not run remotely because this working tree has not been committed or pushed.
