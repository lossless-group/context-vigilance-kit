/**
 * /llms.txt — index of the kit's site for LLM consumers. Spec: https://llmstxt.org/
 *
 * The human-editable prose template lives at `splash/src/llms/llms.md`
 * (tokens documented in `splash/src/llms/README.md`). This file is the dumb
 * assembler: it loads the template, computes link lists, and substitutes
 * tokens. To change the voice, edit the markdown, not this file.
 *
 * On GitHub Pages the site lives under a path (/context-vigilance-kit/), so
 * root-level discovery doesn't work there; on Vercel (base '/') it does.
 */

import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { STATIC_SEO } from '@lib/seo';
import { isPublished } from '@lib/repo';
import template from '../llms/llms.md?raw';

function line(title: string, url: string, lede?: string) {
  return lede ? `- [${title}](${url}): ${lede}` : `- [${title}](${url})`;
}

export const GET: APIRoute = async () => {
  const site = import.meta.env.SITE ?? 'https://lossless-group.github.io';
  const base = import.meta.env.BASE_URL ?? '/';
  const root = new URL(base, site).toString().replace(/\/$/, '');

  const patterns = (await getCollection('patterns')).sort(
    (a, b) => ((a.data as any).order ?? 99) - ((b.data as any).order ?? 99),
  );
  const changelog = (await getCollection('changelog')).filter((e) => isPublished(e.data as any));
  const context = (await getCollection('context')).filter((e) => isPublished(e.data as any));

  const tokens: Record<string, string> = {
    SITE_NAME: STATIC_SEO.siteName,
    ROOT_URL: `${root}/`,
    GETTING_STARTED_URL: `${root}/getting-started/`,
    SEARCH_URL: `${root}/search/`,
    LLMS_FULL_URL: `${root}/llms-full.txt`,
    PATTERN_COUNT: String(patterns.length),
    PATTERN_INDEX: patterns
      .map((p) => line(`${(p.data as any).title} (${(p.data as any).maturity})`, `${root}/patterns/${p.id}/`, (p.data as any).lede))
      .join('\n'),
    CHANGELOG_INDEX: changelog
      .map((e) => line((e.data as any).title ?? e.id, `${root}/changelog/${e.id}/`, (e.data as any).lede))
      .join('\n'),
    CONTEXT_INDEX: context
      .map((e) => line((e.data as any).title ?? e.id, `${root}/context-v/${e.id}/`, (e.data as any).lede))
      .join('\n'),
  };

  const body = template.replace(/\{\{(\w+)\}\}/g, (match, name) =>
    Object.prototype.hasOwnProperty.call(tokens, name) ? tokens[name] : match,
  );
  return new Response(body, { headers: { 'Content-Type': 'text/markdown; charset=utf-8' } });
};
