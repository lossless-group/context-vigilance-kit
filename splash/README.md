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

One build, two hosts. `astro.config.mjs` picks the base path from the environment:

| Host | URL | Base | How it deploys |
|---|---|---|---|
| GitHub Pages | `lossless-group.github.io/context-vigilance-kit/` | `/context-vigilance-kit/` | `.github/workflows/pages.yml` on every push to `master` (the stable tier, and the branch plugin installs read) |
| Vercel | the project's domain | `/` | Vercel's Git integration (detected via `VERCEL=1`) |

`SITE_URL` overrides both, e.g. `SITE_URL=https://contextvigilance.com` once a custom domain is attached. `robots.txt`, the sitemap, canonical URLs, and `llms.txt` all follow it.

### Setting up Vercel (once)

1. Vercel → **Add New → Project** → import `lossless-group/context-vigilance-kit`.
2. **Root Directory: `splash`.** Vercel reads `splash/vercel.json` (framework Astro, `pnpm install`, `pnpm build`, output `dist`).
3. **Production branch: `master`**, to match the Pages deploy (Settings → Git).
4. Environment variable `OPENPANEL_CLIENT_ID` (Production), see below.
5. Don't add a `packageManager` pin to `package.json`; it breaks Vercel's pnpm. `splash/.npmrc` points `@jsr` at `npm.jsr.io` so the LFM package installs without anyone's global config.

## Analytics (OpenPanel)

`src/components/Analytics.astro` loads OpenPanel in **production builds only**, and only when `OPENPANEL_CLIENT_ID` is set. Without it the site has no analytics, which is fine.

- The client ID is public by design (it's in the HTML). Never put the client *secret* anywhere in this site.
- **GitHub Pages:** repo Settings → Secrets and variables → Actions → **Variables** → `OPENPANEL_CLIENT_ID`. The workflow injects it at build time.
- **Vercel:** project Settings → Environment Variables → `OPENPANEL_CLIENT_ID`, then redeploy.
- **In OpenPanel:** the client's **supported domains** must list every origin the site is served from (`https://lossless-group.github.io/`, the Vercel domain, any custom domain). A missing origin means every event is rejected with a 401, while the script looks perfectly healthy.
- Verify: `curl -s <site> | grep -c openpanel` should be 1, then in an incognito window with extensions off, DevTools → Network → `api.openpanel.dev/track` should return 200.

See the `openpanel-analytics` skill for the full pattern.
