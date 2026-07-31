import type { TranscriptEvent } from './types';

const BASE = `http://127.0.0.1:${import.meta.env.VITE_AGDALUS_PORT ?? '54321'}`;

export async function healthCheck(): Promise<{ status: string; auto_model: string }> {
  const r = await fetch(`${BASE}/health`);
  return r.json();
}

/**
 * Stream transcription segments from the backend.
 * Calls `onSegment` for each received segment, `onDone` when complete.
 */
export async function transcribe(
  file: File,
  opts: { language: string; model: string },
  onSegment: (seg: TranscriptEvent) => void,
  onDone: () => void,
  signal?: AbortSignal,
): Promise<void> {
  const body = new FormData();
  body.append('file', file);
  body.append('language', opts.language);
  body.append('model', opts.model === 'auto' ? '' : opts.model);

  const response = await fetch(`${BASE}/transcribe`, { method: 'POST', body, signal });

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(err.detail ?? 'Transcription failed');
  }

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();
  let buf = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    const lines = buf.split('\n');
    buf = lines.pop() ?? '';
    for (const line of lines) {
      if (!line.trim()) continue;
      const event: TranscriptEvent = JSON.parse(line);
      onSegment(event);
      if (event.type === 'done') onDone();
    }
  }
}

export function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}
