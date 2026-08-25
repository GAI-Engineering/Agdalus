# How to record the Agdalus evidence demo

This guide produces the browser-based demo shown in the storyboard. The fixture
replaces FFmpeg and Whisper while exercising the current file validation,
bounded persistence, NDJSON streaming, transcript rendering, and workspace
cleanup paths.

## Prerequisites

- Windows 10 or 11.
- Node.js 20 or newer and npm.
- Python 3.11 or newer virtual environment created from
  `backend/requirements-test.txt`.
- FFmpeg only for generating a valid silent WAV fixture.
- Windows Snipping Tool screen recording, Xbox Game Bar, or OBS Studio.
- No service already listening on ports 1420 or 54321.

## Prepare the repository

From the repository root:

```powershell
npm ci
python -m venv .venv-test
.\.venv-test\Scripts\python.exe -m pip install -r backend\requirements-test.txt
```

Verify the recording package before opening the UI:

```powershell
.\.venv-test\Scripts\ruff.exe check backend scripts
.\.venv-test\Scripts\pyright.exe backend scripts
.\.venv-test\Scripts\python.exe -m pytest -q
npm run check
npm run build
```

## Start the deterministic demo

Open terminal 1:

```powershell
npm run dev -- --host 127.0.0.1
```

Open terminal 2:

```powershell
.\.venv-test\Scripts\python.exe -m scripts.demo_fixture_backend
```

The fixture server prints a disclosure that FFmpeg and Whisper are replaced.
Confirm both services:

```powershell
Invoke-RestMethod http://127.0.0.1:54321/health
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:1420
```

## Generate the recording fixture

Create a valid one-second silent WAV in the Windows temporary directory:

```powershell
$demoWav = Join-Path $env:TEMP 'interview-demo.wav'
ffmpeg -hide_banner -loglevel error -y -f lavfi -i "anullsrc=r=16000:cl=mono" -t 1 $demoWav
Write-Output $demoWav
```

The fixture backend validates the WAV header but does not transcribe its audio.
The on-screen transcript is the deterministic content defined in
[`scripts/demo_fixture_backend.py`](../../scripts/demo_fixture_backend.py).

## Configure the recording window

1. Open `http://127.0.0.1:1420` in a Chromium-based browser.
2. Set the window content area to 1280 x 720 and browser zoom to 100%.
3. Hide bookmarks, downloads, notifications, personal tabs, and account avatars.
4. Use light mode to match the supplied screenshots, or record the entire video
   consistently in dark mode.
5. Open [the evidence slide](evidence-slide.html) in a second tab.
6. Put `interview-demo.wav` in an Explorer window beside the browser.

## Record the shot sequence

1. Record the disclosure slate for five seconds.
2. Show the idle interface for ten seconds.
3. Drag `interview-demo.wav` from Explorer onto the drop zone.
4. Open the Language and Model lists, then leave both on Auto.
5. Click **Transcribe** and keep the progress state visible while segments arrive.
6. Pause on the complete transcript and point to Copy, TXT, SRT, and MD.
7. Switch to the evidence slide and hold for at least 20 seconds.
8. Return to the transcript for the closing line.
9. Stop recording before opening terminals or other personal windows.

Follow the exact narration in [the product video script](PRODUCT_VIDEO_SCRIPT.md).

## Recording settings

| Setting | Recommended value |
|---|---|
| Canvas/output | 1280 x 720 |
| Frame rate | 30 fps |
| Video codec | H.264 |
| Video bitrate | 6–10 Mbps |
| Audio | 48 kHz, mono or stereo, peak between -12 and -6 dBFS |
| Cursor | Visible, no click animation |
| Output | MP4 for review; retain a high-quality source recording separately |

Record the voiceover separately when possible. It makes retakes and disclosure
corrections much cheaper than repeating the screen capture.

## Verification

Before publishing the recording, confirm:

- The opening fixture disclosure is readable for at least four seconds.
- The transcript exactly matches the deterministic fixture strings.
- The browser console contains no errors.
- The network view contains only the Vite development origin and the loopback
  POST to `127.0.0.1:54321/transcribe` during the demo flow.
- No narration exceeds the approved claims in
  [the feature reference](FEATURE_REFERENCE.md).
- The evidence slide says “Proceed with conditions,” not “Passed” or “Ready.”
- No personal paths, notifications, tokens, user names, or unrelated tabs appear.
- Captions are reviewed manually against the final audio.

## Troubleshooting

### Port 54321 is already in use

Stop the stale fixture/backend process before recording:

```powershell
Get-NetTCPConnection -LocalPort 54321 -State Listen |
  Select-Object LocalAddress, LocalPort, OwningProcess
```

Do not terminate a process until you have verified its identity.

### Browse files does nothing

The button calls the Tauri dialog plugin and is not expected to work in a normal
browser. Drag the fixture from Explorer onto the drop zone.

### The UI reports a failed fetch

Confirm the fixture backend is running and `/health` responds on port 54321.

### The transcript does not appear

Confirm the fixture is a real WAV file with a RIFF/WAVE header. Regenerate it
with the FFmpeg command above rather than renaming another file.

### The stream completes before the shot is framed

Restart the fixture server and reload the page. Rehearse cursor placement before
clicking **Transcribe**.
