/**
 * /llms-full.txt — concatenated raw markdown of every published corpus entry.
 *
 * Spec: https://llmstxt.org/
 *
 * Where /llms.txt is a link index, this is the full content — every corpus
 * entry's title, source URL, and raw markdown body, separated by horizontal
 * rules. This is the preferred ingest target for LLMs that can handle a
 * single large document (avoids per-page HTTP overhead and HTML noise).
 *
 * Size note: with ~600 corpus entries this file is multi-MB. That's the
 * cost of "give the model everything." Built statically at deploy time;
 * no runtime cost.
 */

import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { STATIC_SEO } from '@lib/seo';

export const GET: APIRoute = async () => {
  const site = import.meta.env.SITE ?? 'https://lossless-group.github.io';
  const base = import.meta.env.BASE_URL ?? '/';
  const root = new URL(base, site).toString().replace(/\/$/, '');

  const all = await getCollection('corpus');
  const published = all.filter(
    (e) => (e.data as any).publish !== false && (e.data as any).private !== true,
  );

  published.sort((a, b) => {
    const ra = ((a.data as any).source_repo_slug || 'unknown').toLowerCase();
    const rb = ((b.data as any).source_repo_slug || 'unknown').toLowerCase();
    if (ra !== rb) return ra.localeCompare(rb);
    const ta = ((a.data as any).title ?? a.id).toLowerCase();
    const tb = ((b.data as any).title ?? b.id).toLowerCase();
    return ta.localeCompare(tb);
  });

  const parts: string[] = [];
  parts.push(`# Context Vigilance — Full Corpus`);
  parts.push('');
  parts.push(`> ${STATIC_SEO.siteName}`);
  parts.push('');
  parts.push(
    `${published.length} context-v documents from the Lossless Group tree, concatenated as raw ` +
      'markdown for LLM ingest. Each document is preceded by a metadata header (title, source ' +
      'repo, source path, canonical URL) and separated by a horizontal rule.',
  );
  parts.push('');
  parts.push(`See also: ${root}/llms.txt (link index, lighter weight).`);
  parts.push('');

  for (const entry of published) {
    const data = entry.data as any;
    const title = data.title ?? entry.id;
    const repo = data.source_repo_slug || 'unknown';
    const sourcePath = data.source_relative_path || entry.id;
    const url = `${root}/corpus/${entry.id}/`;

    parts.push('---');
    parts.push('');
    parts.push(`## ${title}`);
    parts.push('');
    parts.push(`- Source repo: \`${repo}\``);
    parts.push(`- Source path: \`${sourcePath}\``);
    parts.push(`- Canonical URL: ${url}`);
    if (data.date_modified) {
      const dm = data.date_modified instanceof Date ? data.date_modified : new Date(data.date_modified);
      if (!Number.isNaN(dm.getTime())) parts.push(`- Last modified: ${dm.toISOString().slice(0, 10)}`);
    }
    parts.push('');
    parts.push(entry.body ?? '');
    parts.push('');
  }

  return new Response(parts.join('\n'), {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
};
