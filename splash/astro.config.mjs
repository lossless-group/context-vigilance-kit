// @ts-check
import { defineConfig } from 'astro/config';
import pagefind from 'astro-pagefind';
import sitemap from '@astrojs/sitemap';

// Splash for context-vigilance-kit — the public face of the cv plugin:
// what the practice is, how to get started, and the patterns it has grown.
// Reads the kit's own changelog/ and context-v/; no corpus.
//
// Two hosts, one build (same pattern as the hope-ai splash):
//
//   GitHub Pages: https://lossless-group.github.io/context-vigilance-kit/
//                 (project page, base '/context-vigilance-kit/')
//   Vercel:       served from the domain root (base '/')
//
// Vercel sets VERCEL=1 during builds, and VERCEL_PROJECT_PRODUCTION_URL to the
// project's production domain. SITE_URL overrides both, e.g. once a custom
// domain is attached.
const onVercel = process.env.VERCEL === '1';
const site =
  process.env.SITE_URL ??
  (onVercel && process.env.VERCEL_PROJECT_PRODUCTION_URL
    ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
    : 'https://lossless-group.github.io');

export default defineConfig({
  site,
  base: onVercel || process.env.SITE_URL ? '/' : '/context-vigilance-kit/',
  trailingSlash: 'ignore',

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
