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

const cssFiles = findFiles('src', (f) => f.endsWith('.css'));

console.log(`Checking UI tokens across ${cssFiles.length} CSS files...`);

const issues = [];

// Old v1 tokens that were deleted in Phase 5.7:
// --font-display, --font-body, --font-mono, --font-handwritten
// --color-*, --radius-*, --shadow-*, --max-width
const v1LegacyTokenRe = /--(?:color|radius|shadow|max-width)-[a-z0-9_-]+|--font-(?:display|body|mono|handwritten)\b/i;

for (const file of cssFiles) {
  const content = readFileSync(file, 'utf8');
  const lines = content.split('\n');
  lines.forEach((line, idx) => {
    // Check color: var(--ink)
    if (/color:\s*var\(--ink\)/i.test(line)) {
      issues.push({
        file,
        line: idx + 1,
        type: 'CONTRAST_RISK',
        message: `color: var(--ink) found. Text will be unreadable black-on-black on dark card surfaces.`,
        code: line.trim()
      });
    }
    // Check legacy v1 tokens
    if (v1LegacyTokenRe.test(line)) {
      issues.push({
        file,
        line: idx + 1,
        type: 'LEGACY_V1_TOKEN',
        message: `Deprecated v1 token used.`,
        code: line.trim()
      });
    }
  });
}

console.log(`Found ${issues.length} token issues:`);
for (const issue of issues) {
  console.log(`  [${issue.type}] ${issue.file}:${issue.line} -> ${issue.message} ("${issue.code}")`);
}
