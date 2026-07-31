# Graph Report - C:\Claude Cowork\JHU Course\mini_projects\08_agdalus  (2026-07-31)

## Corpus Check
- Corpus is ~3,461 words - fits in a single context window. You may not need a graph.

## Summary
- 178 nodes · 190 edges · 16 communities (14 shown, 2 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.89)
- Token cost: 1,784 input · 5,201 output

## Community Hubs (Navigation)
- CI and Release Pipeline
- Desktop Bundle Assets
- Frontend Toolchain
- Transcription Backend
- Filesystem Permissions
- Package Scripts
- Tauri Application Config
- TypeScript Configuration
- Transcript API and Types
- Backend Process Lifecycle
- Tauri Frontend Plugins
- Single-Page User Interface
- Global Layout and Styles
- Svelte Static Build

## God Nodes (most connected - your core abstractions)
1. `scripts` - 9 edges
2. `compilerOptions` - 9 edges
3. `transcribe()` - 8 edges
4. `Python Backend Dependencies` - 8 edges
5. `bundle` - 6 edges
6. `icon` - 6 edges
7. `allow` - 6 edges
8. `Agdalus Consumer Transcription Product` - 6 edges
9. `_transcribe_segments()` - 5 edges
10. `BackendProcess` - 5 edges

## Surprising Connections (you probably didn't know these)
- `On-Device Audio Transcription` --semantically_similar_to--> `Local-First Privacy`  [INFERRED] [semantically similar]
  README.md → CLAUDE.md
- `Native Desktop Sidecar Architecture` --semantically_similar_to--> `Python FastAPI Sidecar`  [INFERRED] [semantically similar]
  README.md → CLAUDE.md
- `Verbatim` --semantically_similar_to--> `Verbatim Enterprise Transcription Studio`  [INFERRED] [semantically similar]
  README.md → CLAUDE.md
- `Backend CI Job` --references--> `Python Backend Dependencies`  [EXTRACTED]
  .github/workflows/ci.yml → backend/requirements.txt
- `Frontend CI Job` --conceptually_related_to--> `Agdalus HTML Application Shell`  [INFERRED]
  .github/workflows/ci.yml → src/app.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local-First Transcription Stack** — readme_local_transcription, backend_requirements_openai_whisper, backend_requirements_ffmpeg_python, claude_local_first_privacy [INFERRED 0.85]
- **Desktop Sidecar Delivery Architecture** — claude_tauri_2, claude_sveltekit_static_adapter, claude_fastapi_sidecar, readme_native_desktop_architecture [INFERRED 0.95]
- **Cross-Platform Release Pipeline** — _github_workflows_release_cross_platform_build, _github_workflows_release_tauri_release, backend_requirements_python_dependencies [EXTRACTED 1.00]

## Communities (16 total, 2 thin omitted)

### Community 0 - "CI and Release Pipeline"
Cohesion: 0.09
Nodes (30): Backend CI Job, CI Workflow, Frontend CI Job, Cross-Platform Build Matrix, Release Workflow, Tauri Draft Release, FastAPI 0.115.0, ffmpeg-python 0.2.0 (+22 more)

### Community 1 - "Desktop Bundle Assets"
Cohesion: 0.11
Nodes (18): icons/128x128@2x.png, icons/128x128.png, icons/32x32.png, icons/icon.icns, icons/icon.ico, bundle, active, icon (+10 more)

### Community 2 - "Frontend Toolchain"
Cohesion: 0.12
Nodes (17): devDependencies, svelte, svelte-check, @sveltejs/adapter-static, @sveltejs/kit, @sveltejs/vite-plugin-svelte, @tauri-apps/cli, typescript (+9 more)

### Community 3 - "Transcription Backend"
Cohesion: 0.20
Nodes (15): _auto_model(), _extract_audio(), health(), _load_model(), Agdalus local transcription server.  Runs as a Tauri sidecar, bound to 127.0.0, Yield NDJSON lines: one per segment + a final summary line., Raise HTTPException if file header doesn't match expected format., Run FFmpeg to extract 16kHz mono WAV from any supported container. (+7 more)

### Community 4 - "Filesystem Permissions"
Cohesion: 0.13
Nodes (15): $APPDATA/**, $DESKTOP/**, $DOCUMENT/**, $DOWNLOAD/**, $HOME/**, all, readFile, scope (+7 more)

### Community 5 - "Package Scripts"
Cohesion: 0.14
Nodes (13): name, private, scripts, build, check, check:watch, dev, preview (+5 more)

### Community 6 - "Tauri Application Config"
Cohesion: 0.14
Nodes (13): app, macOSPrivateApi, windows, withGlobalTauri, build, beforeBuildCommand, beforeDevCommand, devUrl (+5 more)

### Community 7 - "TypeScript Configuration"
Cohesion: 0.17
Nodes (11): ./.svelte-kit/tsconfig.json, compilerOptions, allowJs, checkJs, esModuleInterop, forceConsistentCasingInFileNames, resolveJsonModule, skipLibCheck (+3 more)

### Community 8 - "Transcript API and Types"
Cohesion: 0.20
Nodes (6): DoneEvent, LANGUAGES, MODEL_LABELS, ModelName, Segment, TranscriptEvent

### Community 9 - "Backend Process Lifecycle"
Cohesion: 0.36
Nodes (8): Child, Mutex, Option, BackendProcess, get_backend_port(), run(), start_backend(), String

### Community 10 - "Tauri Frontend Plugins"
Cohesion: 0.22
Nodes (9): dependencies, @tauri-apps/api, @tauri-apps/plugin-dialog, @tauri-apps/plugin-fs, @tauri-apps/plugin-shell, @tauri-apps/api, @tauri-apps/plugin-dialog, @tauri-apps/plugin-fs (+1 more)

### Community 11 - "Single-Page User Interface"
Cohesion: 0.33
Nodes (4): $lib/api, @tauri-apps/plugin-dialog, @tauri-apps/plugin-fs, $lib/types

## Knowledge Gaps
- **81 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+76 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `bundle` connect `Desktop Bundle Assets` to `Tauri Application Config`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `plugins` connect `Filesystem Permissions` to `Tauri Application Config`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `devDependencies` connect `Frontend Toolchain` to `Package Scripts`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **What connects `name`, `version`, `private` to the rest of the system?**
  _81 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CI and Release Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.08735632183908046 - nodes in this community are weakly interconnected._
- **Should `Desktop Bundle Assets` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Should `Frontend Toolchain` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._