export interface Segment {
  type: 'segment';
  start: number;
  end: number;
  text: string;
  confidence: number; // 0–1
  demo?: boolean;
}

export interface DoneEvent {
  type: 'done';
  language: string;
  model: string;
  demo?: boolean;
}

export type TranscriptEvent = Segment | DoneEvent;

export type ModelName = 'tiny' | 'base' | 'small' | 'medium' | 'large' | 'auto';

export const LANGUAGES: Record<string, string> = {
  '': 'Auto-detect',
  en: 'English',
  es: 'Spanish',
  fr: 'French',
  de: 'German',
  it: 'Italian',
  pt: 'Portuguese',
  nl: 'Dutch',
  ja: 'Japanese',
  ko: 'Korean',
  zh: 'Chinese',
};

export const MODEL_LABELS: Record<ModelName, string> = {
  auto: 'Auto (recommended)',
  tiny: 'Tiny — fastest, lower accuracy',
  base: 'Base — fast, good accuracy',
  small: 'Small — balanced',
  medium: 'Medium — high accuracy',
  large: 'Large — best accuracy, slow',
};
