/**
 * Phase 8.1 gate: internal-link mesh audit.
 *
 *   npm start   (in another shell)
 *   node scripts/check-links.mjs [baseUrl]
 *
 * Crawls every indexable route from src/data/seo.config.ts plus the homepage,
 * collects internal links, and reports:
 *   · orphans        — routes no other page links to (must be zero)
 *   · dead links     — internal hrefs that 404
 *   · thin outlinks  — pages linking to fewer than MIN_OUTLINKS internal routes
 *
 * Exits non-zero if there are orphans or dead links.
 */
import { readFileSync } from 'node:fs';

const BASE = process.argv[2] || 'http://localhost:3000';
const MIN_OUTLINKS = 3;

const cfg = readFileSync('src/data/seo.config.ts', 'utf8');
const noindex = new Set();
const routes = [];
for (const m of cfg.matchAll(/'(\/[^']*)':\s*\{([\s\S]*?)\n  \},/g)) {
  routes.push(m[1]);
  if (/noindex:\s*true/.test(m[2])) noindex.add(m[1]);
}
const indexable = ['/', ...routes.filter((r) => !noindex.has(r))];

const linksFrom = new Map();
const linkedTo = new Map();
const allHrefs = new Set();

const normalise = (href) => {
  if (!href) return null;
  if (/^(https?:|mailto:|tel:|#)/i.test(href)) return null;
  const clean = href.split('#')[0].split('?')[0];
  if (!clean.startsWith('/')) return null;
  return clean.length > 1 && clean.endsWith('/') ? clean.slice(0, -1) : clean;
};

for (const route of indexable) {
  const res = await fetch(BASE + route);
  if (!res.ok) {
    console.error(`  ! ${route} returned ${res.status}`);
    continue;
  }
  const html = await res.text();
  // Strip nav and footer: their links are global chrome and would make every
  // page look well-linked, hiding real orphans.
  const body = html
    .replace(/<header[\s\S]*?<\/header>/gi, '')
    .replace(/<footer[\s\S]*?<\/footer>/gi, '');

  const found = new Set();
  for (const m of body.matchAll(/href="([^"]+)"/g)) {
    const href = normalise(m[1]);
    if (!href || href === route) continue;
    found.add(href);
    allHrefs.add(href);
    if (!linkedTo.has(href)) linkedTo.set(href, new Set());
    linkedTo.get(href).add(route);
  }
  linksFrom.set(route, found);
}

/* Legal pages are reached from the footer by convention and are exempt from
   keyword targeting in docs/seo-content-plan.md — footer-only is correct for
   them, so they do not count as orphans. */
const FOOTER_ONLY_OK = new Set(['/privacy', '/terms', '/refund']);

const orphans = indexable.filter(
  (r) => r !== '/' && !FOOTER_ONLY_OK.has(r) && !linkedTo.has(r)
);
const thin = [...linksFrom.entries()]
  .filter(([, out]) => out.size < MIN_OUTLINKS)
  .map(([r, out]) => `${r} (${out.size})`);

const dead = [];
for (const href of allHrefs) {
  if (indexable.includes(href)) continue;
  const res = await fetch(BASE + href, { method: 'HEAD' });
  if (res.status === 404) dead.push(`${href}  ← linked from ${[...linkedTo.get(href)].join(', ')}`);
}

console.log(`crawled ${indexable.length} indexable routes\n`);

console.log(`orphans (no inbound link outside nav/footer): ${orphans.length}`);
orphans.forEach((o) => console.log('  ✗ ' + o));

console.log(`\ndead internal links: ${dead.length}`);
dead.forEach((d) => console.log('  ✗ ' + d));

console.log(`\npages with fewer than ${MIN_OUTLINKS} internal outlinks: ${thin.length}`);
thin.forEach((t) => console.log('  · ' + t));

if (orphans.length || dead.length) process.exit(1);
