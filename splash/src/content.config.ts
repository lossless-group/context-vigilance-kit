import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// ─── Lenient preprocessors ────────────────────────────────────────────────
// Every doc here is hand-authored, and conventions evolve. The schema must
// tolerate every shape — never throw on author-written frontmatter.

const lenientString = z.preprocess(
  (v) => (v === '' || v === null ? undefined : v),
  z.string().optional(),
);

const lenientStringArray = z.preprocess(
  (v) => {
    if (v === '' || v === null || v === undefined) return undefined;
    if (Array.isArray(v)) return v.map(String);
    if (typeof v === 'string') return [v];
    return v;
  },
  z.array(z.string()).optional(),
);

const lenientDate = z.preprocess(
  (v) => {
    if (v === undefined || v === null || v === '') return undefined;
    if (v instanceof Date) return Number.isNaN(v.getTime()) ? undefined : v;
    if (typeof v === 'string') {
      const t = v.trim();
      if (!t || t === '[]' || t === '~' || /^tbd$/i.test(t)) return undefined;
      const d = new Date(t);
      return Number.isNaN(d.getTime()) ? undefined : d;
    }
    return undefined;
  },
  z.date().optional(),
);

const lenientBoolean = z.preprocess(
  (v) => (v === '' || v === null ? undefined : v),
  z.boolean().optional(),
);

const lenientNumber = z.preprocess(
  (v) => {
    if (v === '' || v === null || v === undefined) return undefined;
    const n = Number(v);
    return Number.isNaN(n) ? undefined : n;
  },
  z.number().optional(),
);

// ─── Shared doc schema ────────────────────────────────────────────────────
// The context-vigilance frontmatter baseline. `.passthrough()` lets unknown
// keys (site_uuid, hex_code, files_changed, …) ride along without noise.

const docSchema = z
  .object({
    title: lenientString,
    lede: lenientString,
    description: lenientString,
    summary: lenientString,
    status: lenientString,
    at_semantic_version: lenientString,
    semantic_version: lenientString,

    date_created: lenientDate,
    date_modified: lenientDate,
    date_authored_initial_draft: lenientDate,
    date_authored_current_draft: lenientDate,
    date_first_published: lenientDate,

    authors: lenientStringArray,
    augmented_with: lenientStringArray,
    tags: lenientStringArray,

    publish: lenientBoolean,
    private: lenientBoolean,
  })
  .passthrough();

// The kit's own ship log: ../changelog/*.md
const changelog = defineCollection({
  loader: glob({ pattern: '*.md', base: '../changelog' }),
  schema: docSchema,
});

// The kit's own context-v/ (its specs, explorations, issues). extra/ is
// scratch and gitignored by convention, so it is never loaded.
const context = defineCollection({
  loader: glob({ pattern: ['**/*.md', '!extra/**', '!**/README.md'], base: '../context-v' }),
  schema: docSchema,
});

// Curated, synthetic pages: the patterns that have emerged across years of
// context-v files. Written for the splash; never copied from real projects.
const patterns = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/patterns' }),
  schema: docSchema.extend({
    order: lenientNumber,
    // Canonical | Experimental | Emerging
    maturity: lenientString,
    // prep | reflection | journey | practice
    mode: lenientString,
  }),
});

export const collections = { changelog, context, patterns };
