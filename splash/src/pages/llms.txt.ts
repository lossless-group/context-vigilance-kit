/**
 * /llms.txt — index of corpus content for LLM consumers.
 *
 * Spec: https://llmstxt.org/
 *
 * Emits a markdown file at the deployed site root listing every published
 * corpus entry, grouped by source repo. LLM crawlers / agentic tools that
 * follow the llms.txt convention will fetch this file directly from the
 * site root to learn what's available without crawling 500+ HTML pages.
 *
 * Conformance note: the spec assumes the file lives at the host root
 * (https://host/llms.txt). Until DNS for contextvigilance.com lands, this
 * splash deploys under a path (/context-vigilance-kit/), so the file lives
 * at https://lossless-group.github.io/context-vigilance-kit/llms.txt. Tools
 * pointed explicitly at that URL still work; convention-based discovery
 * starts working when the custom domain lands and `astro.config.mjs` flips
 * `base` to '/'.
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

  const byRepo = new Map<string, typeof published>();
  for (const entry of published) {
    const repo = (entry.data as any).source_repo_slug || 'unknown';
    if (!byRepo.has(repo)) byRepo.set(repo, [] as any);
    byRepo.get(repo)!.push(entry);
  }
  const repos = [...byRepo.keys()].sort();
  for (const repo of repos) {
    byRepo.get(repo)!.sort((a, b) => {
      const ta = ((a.data as any).title ?? a.id).toLowerCase();
      const tb = ((b.data as any).title ?? b.id).toLowerCase();
      return ta.localeCompare(tb);
    });
  }

  const lines: string[] = [];
  lines.push('# Context Vigilance');
  lines.push('');
  lines.push(`> ${STATIC_SEO.siteName}`);
  lines.push('');
  lines.push(
    'Treat context with the same vigilance as code — versioned, reviewed, cross-linked. ' +
      'This site is the public face of the Context Vigilance Kit: a live catalog of ' +
      `${published.length} context-v documents collected from ${repos.length} Lossless Group ` +
      'projects, plus the open spec and the schema agents follow when authoring or updating ' +
      'those documents.',
  );
  lines.push('');
  lines.push('## Reference');
  lines.push('');
  lines.push(`- [Full-text search](${root}/search/): Pagefind-indexed across the corpus.`);
  lines.push(
    `- [Full corpus content](${root}/llms-full.txt): every corpus entry concatenated as raw ` +
      'markdown — preferred ingest target for LLMs that can handle a single large document.',
  );
  lines.push('- [Source repository](https://github.com/lossless-group/context-vigilance-kit): the kit, the spec, and the collator.');
  lines.push('- [Lossless Group](https://lossless.group): the org that maintains this practice.');
  lines.push('');
  lines.push('## Corpus');
  lines.push('');
  lines.push(
    'Hand-authored context-v files from real projects in the Lossless tree. Each entry is a ' +
      'spec, prompt, blueprint, reminder, exploration, issue, or other context-v artifact. ' +
      'Grouped by source repository.',
  );
  lines.push('');

  for (const repo of repos) {
    lines.push(`### ${repo}`);
    lines.push('');
    for (const entry of byRepo.get(repo)!) {
      const data = entry.data as any;
      const title = data.title ?? entry.id;
      const url = `${root}/corpus/${entry.id}/`;
      const lede = data.lede ?? data.description ?? data.summary;
      lines.push(lede ? `- [${title}](${url}): ${lede}` : `- [${title}](${url})`);
    }
    lines.push('');
  }

  return new Response(lines.join('\n'), {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
};
