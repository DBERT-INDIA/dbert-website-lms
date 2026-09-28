import { readdirSync, statSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

function findFiles(dir, filter) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      if (name !== 'node_modules' && name !== '.next') {
        out.push(...findFiles(full, filter));
      }
    } else if (filter(name)) {
      out.push(full);
    }
  }
  return out;
}

const pageFiles = findFiles('src/app', (f) => f === 'page.tsx');

console.log(`Auditing heading hierarchy across ${pageFiles.length} pages...`);

const headingReports = [];

for (const file of pageFiles) {
  const content = readFileSync(file, 'utf8');
  
  // Find all headings
  const headings = [...content.matchAll(/<(h[1-6])([^>]*)>([\s\S]*?)<\/\1>/gi)].map(m => ({
    level: parseInt(m[1][1], 10),
    tag: m[1].toLowerCase(),
    attrs: m[2],
    text: m[3].replace(/<[^>]+>/g, '').trim().slice(0, 60)
  }));

  const h1Count = headings.filter(h => h.level === 1).length;
  const skips = [];
  
  for (let i = 0; i < headings.length - 1; i++) {
    if (headings[i+1].level - headings[i].level > 1) {
      skips.push(`${headings[i].tag} -> ${headings[i+1].tag}`);
    }
  }

  headingReports.push({
    file,
    h1Count,
    headingsCount: headings.length,
    skips
  });
}

const multipleH1s = headingReports.filter(r => r.h1Count > 1);
const zeroH1s = headingReports.filter(r => r.h1Count === 0);
const skippedLevels = headingReports.filter(r => r.skips.length > 0);

console.log(`Heading audit summary:`);
console.log(`  Pages with zero <h1>: ${zeroH1s.length}`);
console.log(`  Pages with multiple <h1>: ${multipleH1s.length}`);
console.log(`  Pages with skipped heading levels: ${skippedLevels.length}`);

if (zeroH1s.length > 0) {
  console.log(`\nPages missing <h1>:`);
  zeroH1s.forEach(p => console.log(`  ✗ ${p.file}`));
}
if (multipleH1s.length > 0) {
  console.log(`\nPages with multiple <h1>:`);
  multipleH1s.forEach(p => console.log(`  ✗ ${p.file} (${p.h1Count} <h1> tags)`));
}
if (skippedLevels.length > 0) {
  console.log(`\nPages with skipped heading levels:`);
  skippedLevels.slice(0, 10).forEach(p => console.log(`  ⚠ ${p.file}: ${p.skips.join(', ')}`));
}
