/**
 * Derive a "kind" label from a corpus entry's path. The corpus aggregates
 * context-v files written under varying conventions across 28 repos — some
 * follow the canonical six folders (specs/prompts/blueprints/reminders/
 * explorations/issues), others have authored under habits/, workflow/,
 * plans/, journals/, brainstorms/, etc.
 *
 * The brief asks the splash to be honest about that long tail rather than
 * forcing every entry into the codified six. So we recognize a wider set
 * and bucket "everything else" into "other".
 */

const CANONICAL = new Set([
  'specs', 'prompts', 'blueprints', 'reminders', 'explorations', 'issues',
]);

const LONG_TAIL = new Set([
  'habits', 'workflow', 'workflows', 'plans', 'journals', 'brainstorms',
  'reflections', 'experiments', 'patterns', 'guides', 'changelog',
]);

export interface KindLabel {
  /** Path segment matched. Empty string when no segment matched. */
  slug: string;
  /** Display label (capitalized). */
  label: string;
  /** True when the slug is one of the codified six. */
  canonical: boolean;
}

export function deriveKind(
  sourceRelativePath: string | undefined,
  fallbackId: string,
): KindLabel {
  const path = (sourceRelativePath || fallbackId).toLowerCase();
  const segments = path.split('/').filter(Boolean);
  for (const seg of segments) {
    if (CANONICAL.has(seg)) {
      return { slug: seg, label: cap(singularize(seg)), canonical: true };
    }
    if (LONG_TAIL.has(seg)) {
      return { slug: seg, label: cap(singularize(seg)), canonical: false };
    }
  }
  return { slug: 'other', label: 'Other', canonical: false };
}

function singularize(s: string): string {
  if (s.endsWith('ies')) return s.slice(0, -3) + 'y';
  if (s.endsWith('s')) return s.slice(0, -1);
  return s;
}

function cap(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Cognitive mode hints — used by the Act 2 matrix. Not a hard mapping; just
 *  the heuristic the practice document uses to color which mode a folder
 *  most often expresses. Keep in sync with the narrative brief. */
export const COGNITIVE_MODE: Record<string, 'prep' | 'reflection' | 'journey'> = {
  specs: 'prep',
  prompts: 'prep',
  blueprints: 'reflection',
  reminders: 'reflection',
  patterns: 'reflection',
  habits: 'reflection',
  reflections: 'reflection',
  explorations: 'journey',
  issues: 'journey',
  journals: 'journey',
  workflow: 'journey',
  brainstorms: 'journey',
  experiments: 'journey',
  plans: 'prep',
};
