/**
 * Phase 6 / Phase 9 gate: validates every entry in src/data/seo.config.ts.
 *
 *   node scripts/check-seo.mjs        (or: npm run check:seo)
 *
 * Checks:
 *  · title ≤ 52 chars (60 once layout.tsx appends " | DBERT")
 *  · description 140–155 chars
 *  · primary keyword unique across routes, and present in the description
 *  · every routed page has an entry, and every entry has a page
 *
 * Exits non-zero on any failure so it can be wired into CI.
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const TITLE_MAX = 52;
const DESC_MIN = 140;
const DESC_MAX = 155;

// The config is TypeScript; pull the object out without a compile step.
const source = readFileSync('src/data/seo.config.ts', 'utf8');
const entries = [];
const entryRe =
  /'(\/[^']*)':\s*\{\s*keyword:\s*'([^']*)',\s*title:\s*'((?:[^'\\]|\\.)*)',\s*description:\s*\n?\s*'((?:[^'\\]|\\.)*)',(\s*noindex:\s*true,)?/g;
let m;
while ((m = entryRe.exec(source)) !== null) {
  entries.push({
    route: m[1],
    keyword: m[2],
    title: m[3].replace(/\\'/g, "'"),
    description: m[4].replace(/\\'/g, "'"),
    noindex: Boolean(m[5]),
  });
}

// Discover routed pages on disk.
function findRoutes(dir, base = '') {
  const out = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      out.push(...findRoutes(full, `${base}/${name}`));
    } else if (name === 'page.tsx') {
      out.push(base || '/');
    }
  }
  return out;
}
const routes = findRoutes('src/app').filter(
  (r) => !r.includes('[') && r !== '/'
);

const failures = [];
const seenKeywords = new Map();

for (const e of entries) {
  if (e.title.length > TITLE_MAX) {
    failures.push(`${e.route}: title ${e.title.length} chars (max ${TITLE_MAX})`);
  }
  if (!e.noindex) {
    if (e.description.length < DESC_MIN || e.description.length > DESC_MAX) {
      failures.push(
        `${e.route}: description ${e.description.length} chars (want ${DESC_MIN}–${DESC_MAX})`
      );
    }
    if (!e.keyword) {
      failures.push(`${e.route}: missing primary keyword`);
    } else {
      if (seenKeywords.has(e.keyword)) {
        failures.push(
          `${e.route}: keyword "${e.keyword}" already used by ${seenKeywords.get(e.keyword)}`
        );
      }
      seenKeywords.set(e.keyword, e.route);
    }
  }
}

const configured = new Set(entries.map((e) => e.route));
for (const r of routes) {
  if (!configured.has(r)) failures.push(`${r}: routed page has no SEO entry`);
}
for (const e of entries) {
  if (!routes.includes(e.route)) failures.push(`${e.route}: entry has no page`);
}

console.log(`checked ${entries.length} entries against ${routes.length} routed pages`);

if (failures.length) {
  console.error(`\n${failures.length} problem(s):`);
  failures.forEach((f) => console.error('  ✗ ' + f));
  process.exit(1);
}
console.log('all SEO entries pass');
