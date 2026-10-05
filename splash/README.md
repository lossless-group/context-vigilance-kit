# context-vigilance-kit splash

The kit's GitHub Pages site: what the practice is, how to get started, the patterns it has grown, the changelog, and the kit's own `context-v/` docs.

**Live:** https://lossless-group.github.io/context-vigilance-kit/

The design is lifted from the [context-v-corpus splash](https://lossless-group.github.io/context-v-corpus/) on purpose: one brand, two sites. The corpus is our own work at scale; this site is for people adopting the kit. See [`DESIGN.md`](DESIGN.md) for tokens, type, and component rules.

## Local dev

```bash
cd splash
pnpm install --ignore-workspace
pnpm dev          # http://localhost:4321/context-vigilance-kit/
pnpm build && pnpm preview   # needed to try search (the Pagefind index is built at build time)
```

## Where content lives

| Route | Source | Notes |
|---|---|---|
| `/` | `src/pages/index.astro` | Five acts: hook, practice, cycle, patterns, invitation |
| `/getting-started/` | `src/pages/getting-started/index.astro` | Install, first cycle, companions, config |
| `/patterns/` | `src/content/patterns/*.md` | Curated and synthetic: never copied from real projects. `maturity` (Canonical / Experimental / Emerging), `mode`, and `order` control grouping and order. |
| `/changelog/` | `../changelog/*.md` | The kit's ship log |
| `/context-v/` | `../context-v/**/*.md` | The kit's own docs. `extra/` is never loaded; `publish: false` or `private: true` keeps a doc off the site. |
| `/llms.txt`, `/llms-full.txt` | `src/llms/*.md` templates | Prose lives in the markdown; the endpoints only substitute tokens |

Share images (OG cards) are defined in `src/lib/seo.ts` and hosted on ImageKit.

## Deploy

`.github/workflows/pages.yml` builds `splash/` and deploys it on every push to `master` (the stable tier, and the branch plugin installs read). Pages must be set to **GitHub Actions** in the repo settings (the workflow's `enablement: true` bootstraps this on first run).

Analytics (OpenPanel) only load in production and only when the repo Variable `OPENPANEL_CLIENT_ID` is set. Without it, the site simply has no analytics.
