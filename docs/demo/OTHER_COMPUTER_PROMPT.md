# Prompt for starting Agdalus on another computer

Copy the prompt below into Codex or another coding agent on the destination
computer. It is written for Windows PowerShell and a clean clone of the GitHub
repository.

## Copy-paste prompt

```text
Clone and start the Agdalus development evidence demo from:
https://github.com/GAI-Engineering/Agdalus

Use Windows PowerShell. Work in a new, clearly named folder. Do not modify,
commit, or push repository files unless I explicitly ask after the demo works.

Objectives:
1. Clone the repository and check out the immutable
   demo-evidence-loop-001 tag. Verify HEAD resolves to that tag before continuing:
   git checkout demo-evidence-loop-001
   if ((git rev-parse HEAD) -ne (git rev-list -n 1 demo-evidence-loop-001)) { throw 'Demo tag verification failed' }
2. Read README.md, docs/demo/README.md,
   docs/demo/FEATURE_REFERENCE.md, and
   docs/demo/RECORDING_RUNBOOK.md before running anything.
3. Verify Git, Node.js 20+, npm, Python 3.11 or newer, and FFmpeg are installed. If a
   prerequisite is missing, tell me exactly what is missing and ask before
   making a machine-wide installation.
4. Install repository dependencies with reproducible commands:
   npm ci
   python -m venv .venv-test
   .\.venv-test\Scripts\python.exe -m pip install -r backend\requirements-test.txt
5. Run the quality gates before starting the demo:
   .\.venv-test\Scripts\ruff.exe check backend scripts
   .\.venv-test\Scripts\ruff.exe format --check backend scripts
   .\.venv-test\Scripts\pyright.exe backend scripts
   .\.venv-test\Scripts\python.exe -m pytest -q --cov=backend.main --cov-report=term-missing --cov-fail-under=80
   npm run check
   npm run build
6. Stop if any gate fails. Diagnose the failure, but do not change source files
   unless I authorize a fix.
7. Confirm ports 1420 and 54321 are free. Do not terminate an existing process
   until you identify it and receive my approval.
8. Start the frontend in one PowerShell terminal:
   npm run dev -- --host 127.0.0.1
9. Start the deterministic recording backend in a second terminal:
   .\.venv-test\Scripts\python.exe -m scripts.demo_fixture_backend
10. Generate a valid one-second silent WAV fixture:
    $demoWav = Join-Path $env:TEMP 'interview-demo.wav'
    ffmpeg -hide_banner -loglevel error -y -f lavfi -i "anullsrc=r=16000:cl=mono" -t 1 $demoWav
11. Verify both local services:
    Invoke-RestMethod http://127.0.0.1:54321/health
    Invoke-WebRequest -UseBasicParsing http://127.0.0.1:1420
12. Open http://127.0.0.1:1420 in the browser. Drag interview-demo.wav onto
    the drop zone, leave Language and Model on Auto, and click Transcribe.
13. Verify four timestamped deterministic segments appear and the Copy, TXT,
    SRT, and MD controls are visible. Check the browser console for errors.
14. Open docs/demo/evidence-slide.html for the evidence portion of the demo.
15. Report the exact commit SHA, tool versions, test/build results, service
    URLs, and any deviations from the recording runbook.

Important evidence boundary:
- This is a development evidence demo, not a release build.
- scripts/demo_fixture_backend.py replaces FFmpeg extraction and Whisper
  inference with deterministic transcript events.
- The demo exercises the real validation, bounded upload persistence, NDJSON
  streaming, transcript rendering, and workspace cleanup paths.
- Do not claim packaged inference, transcription accuracy, privacy
  certification, worker cancellation, whole-process memory bounds, signed
  desktop packaging, or release readiness.
- Keep the opening disclosure from docs/demo/README.md visible in any recording.

When finished, leave the services running for me and give me concise steps for
stopping them safely. Do not commit or push anything.
```

## Manual clone command

If the destination computer is already prepared, the initial clone is:

```powershell
git clone https://github.com/GAI-Engineering/Agdalus.git
Set-Location Agdalus
git checkout demo-evidence-loop-001
git rev-parse HEAD
```

Continue with the commands in the [recording runbook](RECORDING_RUNBOOK.md).
