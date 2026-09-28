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

const tsxFiles = findFiles('src', (f) => f.endsWith('.tsx'));

console.log(`Auditing inline styles across ${tsxFiles.length} TSX files...`);

const inlineStyleHotspots = [];

for (const file of tsxFiles) {
  const content = readFileSync(file, 'utf8');
  const lines = content.split('\n');
  const occurrences = [];
  lines.forEach((line, idx) => {
    if (line.includes('style={{')) {
      occurrences.push({ line: idx + 1, text: line.trim() });
    }
  });
  if (occurrences.length > 0) {
    inlineStyleHotspots.push({
      file,
      count: occurrences.length,
      occurrences
    });
  }
}

inlineStyleHotspots.sort((a, b) => b.count - a.count);

console.log(`Found ${inlineStyleHotspots.length} files with inline styles:`);
for (const item of inlineStyleHotspots) {
  console.log(`  ${item.file}: ${item.count} inline style(s)`);
}
