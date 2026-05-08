// @ts-check
import { defineConfig } from 'astro/config';

// Splash for context-vigilance-kit — catalog of context-v files across
// the Lossless Group tree. v0: local-only, no Pagefind, no MDX.
//
// Live URL once deployed: https://lossless-group.github.io/context-vigilance-kit/
// Adjust `site` / `base` when you wire GitHub Pages.
export default defineConfig({
  site: 'https://lossless-group.github.io',
  base: '/context-vigilance-kit/',
  trailingSlash: 'ignore',
  build: { format: 'directory' },
});
