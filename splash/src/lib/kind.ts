/**
 * Derive a "kind" label from a doc's path inside context-v/: the canonical
 * eight folders, the experimental tier, and a long tail of folders seen in
 * real repos. Anything unrecognized buckets into "other" rather than being
 * forced into the codified set.
 */

const CANONICAL = new Set([
  'specs', 'plans', 'prompts', 'blueprints', 'reminders', 'agent-skills',
  'explorations', 'issues',
]);

/** Proposed folders in the experimental tier — named by the skill but with
 *  shapes deliberately not yet enforced across repos. */
const EXPERIMENTAL = new Set([
  'loops', 'handoffs', 'decisions', 'habits', 'contracts',
]);

const LONG_TAIL = new Set([
  'workflow', 'workflows', 'journals', 'brainstorms',
  'reflections', 'experiments', 'patterns', 'guides', 'changelog',
  'sitemap', 'narratives', 'profiles', 'inquiry', 'models', 'strategy',
]);

export interface KindLabel {
  /** Path segment matched. Empty string when no segment matched. */
  slug: string;
  /** Display label (capitalized). */
  label: string;
  /** True when the slug is one of the codified eight. */
  canonical: boolean;
  /** True when the slug is in the skill's experimental tier. */
  experimental?: boolean;
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
    if (EXPERIMENTAL.has(seg)) {
      return { slug: seg, label: cap(singularize(seg)), canonical: false, experimental: true };
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
 *  the heuristic for which mode a folder most often expresses. */
export const COGNITIVE_MODE: Record<string, 'prep' | 'reflection' | 'journey'> = {
  specs: 'prep',
  plans: 'prep',
  prompts: 'prep',
  blueprints: 'reflection',
  reminders: 'reflection',
  'agent-skills': 'reflection',
  patterns: 'reflection',
  habits: 'reflection',
  reflections: 'reflection',
  contracts: 'reflection',
  decisions: 'prep',
  loops: 'reflection',
  handoffs: 'journey',
  explorations: 'journey',
  issues: 'journey',
  journals: 'journey',
  workflow: 'journey',
  brainstorms: 'journey',
  experiments: 'journey',
};
