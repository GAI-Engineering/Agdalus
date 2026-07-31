<script lang="ts">
  import { transcribe, formatTime } from '$lib/api';
  import { LANGUAGES, MODEL_LABELS, type Segment, type ModelName } from '$lib/types';
  import { open } from '@tauri-apps/plugin-dialog';

  // ── State ──────────────────────────────────────────────────────────────────
  let file = $state<File | null>(null);
  let language = $state('');
  let model = $state<ModelName>('auto');
  let segments = $state<Segment[]>([]);
  let status = $state<'idle' | 'running' | 'done' | 'error'>('idle');
  let errorMsg = $state('');
  let detectedLang = $state('');
  let usedModel = $state('');
  let abortCtrl = $state<AbortController | null>(null);

  let isDragOver = $state(false);

  // ── File selection ─────────────────────────────────────────────────────────
  async function pickFile() {
    const selected = await open({
      multiple: false,
      filters: [{ name: 'Audio/Video', extensions: ['mp4', 'm4a', 'mp3', 'wav', 'flac', 'ogg', 'aac', 'wma'] }],
    });
    if (selected && typeof selected === 'string') {
      // Tauri returns a path string; wrap in a File-like for FormData
      await loadPath(selected);
    }
  }

  async function loadPath(path: string) {
    // Read file bytes via Tauri FS, create a File object
    const { readFile } = await import('@tauri-apps/plugin-fs');
    const bytes = await readFile(path);
    const name = path.split(/[\\/]/).pop() ?? 'audio';
    file = new File([bytes], name);
    segments = [];
    status = 'idle';
    errorMsg = '';
  }

  function onDrop(e: DragEvent) {
    e.preventDefault();
    isDragOver = false;
    const f = e.dataTransfer?.files[0];
    if (f) {
      file = f;
      segments = [];
      status = 'idle';
      errorMsg = '';
    }
  }

  // ── Transcription ──────────────────────────────────────────────────────────
  async function start() {
    if (!file || status === 'running') return;
    abortCtrl = new AbortController();
    segments = [];
    status = 'running';
    errorMsg = '';
    detectedLang = '';
    usedModel = '';

    try {
      await transcribe(
        file,
        { language, model },
        (event) => {
          if (event.type === 'segment') segments = [...segments, event];
          if (event.type === 'done') {
            detectedLang = event.language;
            usedModel = event.model;
          }
        },
        () => { status = 'done'; },
        abortCtrl.signal,
      );
    } catch (err: unknown) {
      if ((err as Error)?.name === 'AbortError') {
        status = 'idle';
      } else {
        errorMsg = (err as Error)?.message ?? 'Unknown error';
        status = 'error';
      }
    }
  }

  function cancel() {
    abortCtrl?.abort();
    abortCtrl = null;
  }

  // ── Export ─────────────────────────────────────────────────────────────────
  function buildText(): string {
    return segments.map(s => `[${formatTime(s.start)}] ${s.text}`).join('\n');
  }

  function buildSRT(): string {
    return segments.map((s, i) => {
      const fmt = (sec: number) => {
        const h = Math.floor(sec / 3600);
        const m = Math.floor((sec % 3600) / 60);
        const ss = Math.floor(sec % 60);
        const ms = Math.round((sec % 1) * 1000);
        return `${h.toString().padStart(2,'0')}:${m.toString().padStart(2,'0')}:${ss.toString().padStart(2,'0')},${ms.toString().padStart(3,'0')}`;
      };
      return `${i + 1}\n${fmt(s.start)} --> ${fmt(s.end)}\n${s.text}\n`;
    }).join('\n');
  }

  function buildMarkdown(): string {
    return segments.map(s => `**[${formatTime(s.start)}]** ${s.text}`).join('\n\n');
  }

  function download(content: string, filename: string, mime: string) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  const baseName = $derived(file ? file.name.replace(/\.[^.]+$/, '') : 'transcript');
</script>

<main>
  <!-- Drop zone / file picker -->
  <section
    class="dropzone"
    class:active={isDragOver}
    class:has-file={!!file}
    ondragover={(e) => { e.preventDefault(); isDragOver = true; }}
    ondragleave={() => { isDragOver = false; }}
    ondrop={onDrop}
    aria-label="Drop zone"
  >
    {#if file}
      <span class="filename">{file.name}</span>
      <button onclick={() => { file = null; segments = []; status = 'idle'; }} class="clear" aria-label="Remove file">✕</button>
    {:else}
      <div class="drop-hint">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
          <path d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>
          <polyline points="16 8 12 4 8 8"/>
          <line x1="12" y1="4" x2="12" y2="16"/>
        </svg>
        <p>Drop audio or video here</p>
        <button onclick={pickFile}>Browse files</button>
      </div>
    {/if}
  </section>

  <!-- Controls -->
  <section class="controls">
    <select bind:value={language} aria-label="Language" disabled={status === 'running'}>
      {#each Object.entries(LANGUAGES) as [code, label]}
        <option value={code}>{label}</option>
      {/each}
    </select>

    <select bind:value={model} aria-label="Model" disabled={status === 'running'}>
      {#each Object.entries(MODEL_LABELS) as [key, label]}
        <option value={key}>{label}</option>
      {/each}
    </select>

    {#if status === 'running'}
      <button onclick={cancel} class="danger">Cancel</button>
    {:else}
      <button onclick={start} class="primary" disabled={!file}>Transcribe</button>
    {/if}
  </section>

  <!-- Progress indicator -->
  {#if status === 'running'}
    <div class="progress" role="status" aria-live="polite">
      <span class="spinner" aria-hidden="true"></span>
      Transcribing{segments.length > 0 ? ` — ${segments.length} segment${segments.length === 1 ? '' : 's'}` : '…'}
    </div>
  {/if}

  <!-- Error -->
  {#if status === 'error'}
    <div class="error-banner" role="alert">{errorMsg}</div>
  {/if}

  <!-- Transcript -->
  {#if segments.length > 0}
    <section class="transcript-wrap">
      <div class="transcript-header">
        <span class="meta">
          {segments.length} segments
          {#if detectedLang} · {detectedLang}{/if}
          {#if usedModel} · {usedModel}{/if}
        </span>
        <div class="export-btns">
          <button onclick={() => navigator.clipboard.writeText(segments.map(s => s.text).join(' '))}>Copy text</button>
          <button onclick={() => download(buildText(), `${baseName}.txt`, 'text/plain')}>TXT</button>
          <button onclick={() => download(buildSRT(), `${baseName}.srt`, 'text/plain')}>SRT</button>
          <button onclick={() => download(buildMarkdown(), `${baseName}.md`, 'text/markdown')}>MD</button>
        </div>
      </div>
      <div class="transcript" role="list">
        {#each segments as seg (seg.start)}
          <div class="segment" role="listitem">
            <span class="ts">{formatTime(seg.start)}</span>
            <span class="text" style:opacity={0.5 + seg.confidence * 0.5}>{seg.text}</span>
          </div>
        {/each}
      </div>
    </section>
  {/if}
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 860px;
    margin: 0 auto;
    padding: 24px 20px;
    gap: 12px;
  }

  /* Drop zone */
  .dropzone {
    border: 2px dashed var(--border);
    border-radius: var(--radius);
    background: var(--surface);
    min-height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: border-color 0.15s, background 0.15s;
    position: relative;
  }
  .dropzone.active { border-color: var(--accent); background: color-mix(in srgb, var(--accent) 8%, var(--surface)); }
  .dropzone.has-file { min-height: 52px; border-style: solid; }

  .drop-hint {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    color: var(--text-muted);
  }
  .drop-hint p { font-size: 13px; }

  .filename {
    font-size: 13px;
    font-weight: 500;
    color: var(--text);
    user-select: text;
    padding: 0 40px 0 12px;
  }
  .clear {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    border: none;
    background: transparent;
    color: var(--text-muted);
    font-size: 14px;
    padding: 4px 6px;
  }
  .clear:hover { color: var(--danger); background: transparent; }

  /* Controls */
  .controls {
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
  }
  .controls select { flex: 1; min-width: 140px; }
  button.danger { border-color: var(--danger); color: var(--danger); }
  button.danger:hover { background: color-mix(in srgb, var(--danger) 12%, var(--surface)); }

  /* Progress */
  .progress {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--text-muted);
    padding: 6px 0;
  }
  .spinner {
    width: 14px; height: 14px;
    border: 2px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Error */
  .error-banner {
    background: color-mix(in srgb, var(--danger) 10%, var(--surface));
    border: 1px solid color-mix(in srgb, var(--danger) 40%, var(--border));
    border-radius: var(--radius);
    padding: 8px 12px;
    font-size: 13px;
    color: var(--danger);
  }

  /* Transcript */
  .transcript-wrap {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--surface);
    overflow: hidden;
  }

  .transcript-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    flex-wrap: wrap;
    gap: 8px;
  }
  .meta { font-size: 12px; color: var(--text-muted); }
  .export-btns { display: flex; gap: 6px; flex-wrap: wrap; }
  .export-btns button { font-size: 12px; padding: 4px 10px; }

  .transcript {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
    user-select: text;
  }

  .segment {
    display: flex;
    gap: 10px;
    padding: 5px 12px;
    border-radius: 4px;
    transition: background 0.1s;
  }
  .segment:hover { background: color-mix(in srgb, var(--accent) 6%, var(--surface)); }

  .ts {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
    white-space: nowrap;
    padding-top: 2px;
    min-width: 36px;
  }
  .text { font-size: 14px; line-height: 1.55; }
</style>
