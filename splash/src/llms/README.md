# Source of truth: human-editable prose for the llms.txt endpoints

These markdown files are read at build time by the endpoints in
`splash/src/pages/llms.txt.ts` and `splash/src/pages/llms-full.txt.ts`. The
endpoints are deliberately dumb — they do token substitution and append the
dynamic link lists and bodies. **All voice, framing, and structural prose lives
here, not in TypeScript.**

If you want to tweak the wording on `/llms.txt` or `/llms-full.txt`, edit
the corresponding `.md` file in this directory and rebuild. No code changes.

## Files

- `llms.md` — template for `/llms.txt` (the link index).
- `llms-full.md` — template for `/llms-full.txt` (the concatenated full content).

## Tokens (substituted at build time)

| Token | Used in | Replaced with |
|---|---|---|
| `{{SITE_NAME}}` | both | `STATIC_SEO.siteName` from `splash/src/lib/seo.ts` |
| `{{ROOT_URL}}`, `{{GETTING_STARTED_URL}}`, `{{SEARCH_URL}}`, `{{LLMS_FULL_URL}}` | `llms.md` | Absolute URLs on the deployed site |
| `{{PATTERN_COUNT}}` | `llms.md` | Number of pattern pages |
| `{{PATTERN_INDEX}}`, `{{CHANGELOG_INDEX}}`, `{{CONTEXT_INDEX}}` | `llms.md` | Link lists for each section |
| `{{ENTRY_COUNT}}`, `{{BODIES}}`, `{{LLMS_INDEX_URL}}` | `llms-full.md` | Total docs, their concatenated bodies, and the index URL |

Tokens are simple `{{NAME}}` placeholders — no Mustache, no Handlebars, no
templating engine. If a token is missing in the markdown, the endpoint emits
the file without it. If you add a new dynamic value, register it in the
endpoint's substitution map and document it here.

## Why a separate directory and not `src/lib/` or `src/content/`?

`src/lib/` is for code (TypeScript). `src/content/` is for Astro content
collections, which expect specific schemas and Astro-managed loaders. These
files are neither — they're prose templates that the build step reads as raw
strings via Vite's `?raw` import. Giving them their own directory keeps the
purpose obvious and makes the source-of-truth boundary easy to find.
