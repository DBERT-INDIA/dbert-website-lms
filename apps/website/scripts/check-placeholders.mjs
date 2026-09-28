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

const tsxFiles = findFiles('src', (f) => f.endsWith('.tsx') || f.endsWith('.ts'));

console.log(`Auditing placeholder text, zero metrics, and TODOs across ${tsxFiles.length} files...`);

const findings = [];

for (const file of tsxFiles) {
  const content = readFileSync(file, 'utf8');
  const lines = content.split('\n');
  lines.forEach((line, idx) => {
    // Check for zero-metric patterns like '0 ventures', '0 SaaS', '0+ fellows', '~0 mo'
    if (/(?:['"`\s]0\s*(?:ventures|SaaS|fellows|mo|products|startups))/i.test(line)) {
      findings.push({
        file,
        line: idx + 1,
        type: 'ZERO_METRIC',
        text: line.trim()
      });
    }
    // Check for TODO or FIXME
    if (/\b(?:TODO|FIXME|XXX)\b/i.test(line) && !file.includes('check-')) {
      findings.push({
        file,
        line: idx + 1,
        type: 'TODO_COMMENT',
        text: line.trim()
      });
    }
    // Check for lorem ipsum
    if (/lorem\s+ipsum/i.test(line)) {
      findings.push({
        file,
        line: idx + 1,
        type: 'LOREM_IPSUM',
        text: line.trim()
      });
    }
  });
}

console.log(`Found ${findings.length} placeholder / zero-metric items:`);
for (const item of findings) {
  console.log(`  [${item.type}] ${item.file}:${item.line} -> ${item.text}`);
}
