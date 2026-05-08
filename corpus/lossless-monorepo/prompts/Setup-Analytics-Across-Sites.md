---
source_root: /Users/mpstaton/code/lossless-monorepo/context-v
source_relative_path: prompts/Setup-Analytics-Across-Sites.md
source_repo_slug: lossless-monorepo
collated_at: '2026-05-08'
source_path: "context-v/prompts/Setup-Analytics-Across-Sites.md"
---



# Note to Agents:

We have not chosen a single analytics platform, and to be honest we don't really need one but we are launching a lot of project splash pages and, for when we have a custom domain, pushing out a marketing site.  It would be good to see "traction" or "interest" once we start promoting.


## For now in May 2026, Umami and Fathom are our starters.

> Umami will only allow three sites on their hosted platform without payment, though they have a self-host OSS option.  Fathom is a little more polished and allows unlimited websites (you pay based on traffic), but we can't self-host it.  

> Though we don't really self-host now it's an ambition of ours.

Anyway, the actual snippets are in a .gitignore folder called .analytics at monorepo root.
`/Users/mpstaton/code/lossless-monorepo/.analytics`

We have 8 sites to hook up.  Discuss.

If you read the docs for each platform, you'll see that they have different features and syntactic differences in embedding snippets.  We need to decide which one to use for each site. 

My first pass concern is just general traffic.  

Though, I would like to know what people actually click on.


---

# Convergence (2026-05-06)

We are intentionally splitting this into two passes. **This prompt is Pass 1 — get scripts live and start collecting traffic.** Pass 2 (clicks, custom events, flows, goals) is captured in a sibling prompt: [[Implement-Deeper-Analytics-Tracking]] — `/Users/mpstaton/code/lossless-monorepo/context-v/prompts/Implement-Deeper-Analytics-Tracking.md`.

## Pass 1 — Get it live (this prompt)

### Platform allocation
Already encoded in `/Users/mpstaton/code/lossless-monorepo/.analytics/Setup-Analytics-Platforms-Across-Live-Sites.md`:

- **Umami** — top 3 only (free-tier ceiling): `lossless.group`, `the-water-foundation.com`, `mpstaton.com`
- **Fathom** — all 8 sites (unlimited on traffic-based pricing)

### Implementation rules
1. **Production-only gate.** Wrap every script tag in `{import.meta.env.PROD && (...)}` so localhost and PR previews don't pollute the dashboards.
2. **One canonical `<head>` per site.** Each Astro site has multiple layouts, but only one of them should own the `<head>`. If a site renders `<head>` from several layouts, fix that first by routing through a shared `<BaseHead>` partial; analytics surfaces the duplication but is not the sole reason to fix it.
3. **Tiny `<Analytics />` component per site.** Per-site, not per-monorepo — each site is its own Astro app with its own IDs. The component just emits the two (or one) script tags, gated on `PROD`.
4. **Snippets are copied verbatim from `.analytics/Setup-Analytics-Platforms-Across-Live-Sites.md`** — do not regenerate IDs.
5. **No event instrumentation in Pass 1.** Just the passive scripts.

### Per-site placement — as shipped (2026-05-06)

Each site got an `<Analytics />` component at `src/components/Analytics.astro` containing the verbatim snippets from `.analytics/`, gated on `import.meta.env.PROD`, with `is:inline` on the script tags so Astro/Vite doesn't try to bundle the external CDN URLs.

| Site | Component | Wired into |
|---|---|---|
| `lossless.group` | `site/src/components/Analytics.astro` | `src/layouts/Layout.astro` + 3 slide-embed pages (`pages/slides/[collection]/[...slug].astro`, `pages/slides/embed/[...slug].astro`, `pages/slides/embed/astro/[...slug].astro`) |
| `the-water-foundation.com` | `astro-knots/sites/twf_site/src/components/Analytics.astro` | `BoilerPlateHTML.astro`, `OneSlideDeck.astro`, `MarkdownSlideDeck.astro` (3 layouts each emit their own `<html>` — see Pass 2 cleanup note below) |
| `mpstaton.com` | `astro-knots/sites/mpstaton-site/src/components/Analytics.astro` | `BaseLayout.astro`, `PromotionDeckLayout.astro` |
| `fullstack-vc.com` | `astro-knots/sites/fullstack-vc/src/components/Analytics.astro` | `BoilerPlateHTML.astro` (single canonical head; `OneSlideDeck` wraps `BaseThemeLayout` which wraps this) |
| `lossless-group.github.io/content-farm` | `content-farm/splash/src/components/Analytics.astro` | `src/layouts/BaseLayout.astro` |
| `lossless-group.github.io/astro-knots` | `astro-knots/splash/src/components/Analytics.astro` | `src/layouts/BaseLayout.astro` |
| `lossless-group.github.io/memopop-ai` | `ai-labs/memopop-ai/apps/memopop-site/src/components/Analytics.astro` | `apps/memopop-site/src/layouts/BaseLayout.astro` |
| `hypernova-site` | `astro-knots/sites/hypernova-site/src/components/Analytics.astro` | `src/layouts/BoilerPlateHTML.astro` |

### Skipped on lossless.group
These pages emit their own `<head>` but are debug/internal-only — no analytics added, no need:
- `src/pages/debug-mocs.astro`
- `src/pages/test-tag-mocs.astro`
- `src/pages/debug/sequential-section.astro`
- `src/pages/backlink.astro` (SSR redirect handler — no UI)

### Cleanup deferred to Pass 2 / future
- **`twf_site` head duplication**: `BoilerPlateHTML`, `OneSlideDeck`, and `MarkdownSlideDeck` all emit their own `<html>`. `MarkdownSlideDeck` even nests `<html>` inside its own `<body>` (broken). For Pass 1 we instrumented all three; the right long-term fix is to route slide layouts through `BoilerPlateHTML` so there's one canonical head. Not blocking analytics — Umami/Fathom dedupe pageviews via session, so the worst-case is double-fire on a malformed page.
- **`mpstaton-site` head duplication**: `BaseLayout` (public) and `PromotionDeckLayout` (private gated decks) each emit their own `<html>`. Both instrumented. PromotionDeck pages are noindex but still want traction tracking.
- **`lossless.group` slide-embed pages**: 3 dynamic pages emit their own complete HTML rather than going through `Layout.astro`. Could be refactored to a shared `<BaseHead>` partial. Not urgent.

### Still-open questions
- **`memopop-ai` deploy URL**: the snippet is in place, but the Fathom dashboard must list the actual live domain or events won't record. If `lossless-group.github.io/memopop-ai` is wrong (subdomain, Vercel, etc.), update the Fathom site config — no code change needed.
- **Live status**: snippets are gated on `PROD`, so any site that isn't actually deployed yet just won't fire. Safe no-op.

## Pass 2 — Deeper tracking (separate prompt)

See [[Implement-Deeper-Analytics-Tracking]]. That prompt covers:
- Fathom `trackEvent()` for CTAs, form submits, downloads
- Umami `data-umami-event` attributes and `umami.track()` calls
- Outbound link tracking (manual on both platforms)
- SPA pageview tracking (if any of the sites become SPAs)
- Goals/conversions on Fathom
- A small set of named events shared across sites for cross-site comparability

**Do not start Pass 2 work until Pass 1 is shipped and we've seen at least a week of baseline traffic.** Premature instrumentation is noise.
