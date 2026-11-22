// @ts-check
import { defineConfig } from 'astro/config';
import pagefind from 'astro-pagefind';
import sitemap from '@astrojs/sitemap';

// Splash for context-vigilance-kit — the public face of the cv plugin:
// what the practice is, how to get started, and the patterns it has grown.
// Reads the kit's own changelog/ and context-v/; no corpus.
//
// Hosted on Vercel only, at the domain root (base '/'). The GitHub Pages copy
// was retired on 2026-11-21; lossless-group.github.io belongs to the corpus.
//
// Vercel sets VERCEL=1 during builds and VERCEL_ENV to production / preview.
// Production builds use the custom domain, context-v.dev, so canonical URLs,
// the sitemap, robots.txt, and llms.txt all name it. Preview builds use their
// own deployment URL. Local builds use context-v.dev. SITE_URL overrides everything.
const onVercel = process.env.VERCEL === '1';
const site =
  process.env.SITE_URL ??
  (onVercel
    ? process.env.VERCEL_ENV === 'production'
      ? 'https://context-v.dev'
      : `https://${process.env.VERCEL_URL ?? process.env.VERCEL_PROJECT_PRODUCTION_URL}`
    : 'https://context-v.dev');

export default defineConfig({
  site,
  base: '/',
  trailingSlash: 'ignore',

  // Astro 7's HTML compression drops the whitespace between a word and an
  // inline element that starts on the next source line ("read<a>Agent
  // Skills</a>" instead of "read Agent Skills"). Keep source whitespace.
  compressHTML: false,

  integrations: [
    // astro-pagefind runs Pagefind against `dist/` after `astro build` and
    // copies pagefind/* into the published output. Search runs entirely
    // client-side from the static index — no backend, no cost.
    pagefind(),

    // @astrojs/sitemap auto-generates sitemap-index.xml + sitemap-0.xml from
    // every page Astro emits. Filter excludes the llms.txt endpoints (those
    // serve LLMs, not search engines) and the 404 page.
    sitemap({
      filter: (page) =>
        !page.includes('/llms.txt') &&
        !page.includes('/robots.txt') &&
        !page.includes('/llms-full.txt') &&
        !page.endsWith('/404/') &&
        !page.endsWith('/404'),
    }),
  ],

  build: {
    // Pagefind needs a stable per-page URL — directory output ensures each
    // detail page's data-pagefind-body lives at /<section>/<slug>/index.html.
    format: 'directory',
  },
});
