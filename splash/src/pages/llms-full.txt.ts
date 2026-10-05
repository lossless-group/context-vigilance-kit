/**
 * /llms-full.txt — the kit's patterns, changelog, and context-v docs as one
 * markdown file for LLM ingest. Spec: https://llmstxt.org/
 *
 * Prose template: `splash/src/llms/llms-full.md`. This file only gathers
 * bodies and substitutes tokens.
 */

import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { STATIC_SEO } from '@lib/seo';
import { isPublished } from '@lib/repo';
import template from '../llms/llms-full.md?raw';

export const GET: APIRoute = async () => {
  const site = import.meta.env.SITE ?? 'https://lossless-group.github.io';
  const base = import.meta.env.BASE_URL ?? '/';
  const root = new URL(base, site).toString().replace(/\/$/, '');

  const patterns = (await getCollection('patterns')).sort(
    (a, b) => ((a.data as any).order ?? 99) - ((b.data as any).order ?? 99),
  );
  const changelog = (await getCollection('changelog')).filter((e) => isPublished(e.data as any));
  const context = (await getCollection('context')).filter((e) => isPublished(e.data as any));

  const parts: string[] = [];
  const add = (section: string, title: string, url: string, body: string | undefined) => {
    parts.push('---', '', `## ${title}`, '', `- Section: ${section}`, `- Canonical URL: ${url}`, '', body ?? '', '');
  };
  for (const p of patterns) add('Pattern', (p.data as any).title ?? p.id, `${root}/patterns/${p.id}/`, p.body);
  for (const e of changelog) add('Changelog', (e.data as any).title ?? e.id, `${root}/changelog/${e.id}/`, e.body);
  for (const e of context) add('Kit context-v', (e.data as any).title ?? e.id, `${root}/context-v/${e.id}/`, e.body);

  const tokens: Record<string, string> = {
    SITE_NAME: STATIC_SEO.siteName,
    ENTRY_COUNT: String(patterns.length + changelog.length + context.length),
    LLMS_INDEX_URL: `${root}/llms.txt`,
    BODIES: parts.join('\n').trimEnd(),
  };
  const body = template.replace(/\{\{(\w+)\}\}/g, (match, name) =>
    Object.prototype.hasOwnProperty.call(tokens, name) ? tokens[name] : match,
  );
  return new Response(body, { headers: { 'Content-Type': 'text/markdown; charset=utf-8' } });
};
