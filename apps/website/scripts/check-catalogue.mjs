import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const coreFile = fs.readFileSync(path.join(root, 'src/data/courses.core.ts'), 'utf8');
const specFile = fs.readFileSync(path.join(root, 'src/data/courses.specialized.ts'), 'utf8');
const combined = coreFile + '\n' + specFile;

const slugs = [...combined.matchAll(/slug:\s*'([^']+)'/g)].map((m) => m[1]);
const ids = [...combined.matchAll(/id:\s*'([^']+)'/g)].map((m) => m[1]);
const canonicalPaths = [...combined.matchAll(/canonicalPath:\s*'([^']+)'/g)].map((m) => m[1]);

const errors = [];

if (slugs.length !== 11) {
  errors.push(`Expected 11 canonical tracks, found ${slugs.length}: ${slugs.join(', ')}`);
}
if (new Set(slugs).size !== slugs.length) {
  errors.push('Duplicate slugs detected');
}
if (new Set(ids).size !== ids.length) {
  errors.push('Duplicate IDs detected');
}
for (let i = 0; i < slugs.length; i++) {
  const expectedPath = `/learners/courses/${slugs[i]}`;
  if (canonicalPaths[i] !== expectedPath) {
    errors.push(`Mismatch canonicalPath for ${slugs[i]}: ${canonicalPaths[i]}`);
  }
  const routePage = path.join(root, 'src/app/learners/courses', slugs[i], 'page.tsx');
  if (!fs.existsSync(routePage)) {
    errors.push(`Missing route page for ${slugs[i]} at ${routePage}`);
  }
}

if (errors.length > 0) {
  console.error('Catalogue integrity check FAILED:');
  for (const e of errors) console.error(' -', e);
  process.exit(1);
}

console.log(`Catalogue integrity check PASSED: ${slugs.length} unique tracks, all routes present.`);
