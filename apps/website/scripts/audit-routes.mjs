import { readdirSync, statSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

function findRoutes(dir, base = '') {
  const out = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      out.push(...findRoutes(full, `${base}/${name}`));
    } else if (name === 'page.tsx') {
      out.push({
        route: base || '/',
        filePath: full,
      });
    }
  }
  return out;
}

const routes = findRoutes('src/app');

const auditData = [];

for (const { route, filePath } of routes) {
  const code = readFileSync(filePath, 'utf8');
  
  // Detect CSS modules imported
  const cssModuleImports = [...code.matchAll(/import\s+([A-Za-z0-9_]+)\s+from\s+['"]([^'"]+\.module\.css)['"]/g)].map(m => m[2]);
  
  // Detect inline styles
  const inlineStylesCount = (code.match(/style=\{\{/g) || []).length;
  
  // Detect handcrafted element usages
  const hasHandNote = /HandNote|handnote/.test(code);
  const hasHandArrow = /HandDrawnArrow|hand-arrow/.test(code);
  const hasMarker = /marker/.test(code);
  const hasProofMark = /proof-mark/.test(code);
  const hasRedline = /redline/.test(code);

  // Detect CTAs (Button or Link with btn class or prominent href)
  const buttonsCount = (code.match(/<button/g) || []).length;
  const linkBtnCount = (code.match(/className=\{?[^}]*btn/g) || []).length;

  // Extract primary heading
  const h1Match = code.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
  const h1Text = h1Match ? h1Match[1].replace(/<[^>]+>/g, '').trim() : '';

  auditData.push({
    route,
    h1Text,
    cssModules: cssModuleImports,
    inlineStylesCount,
    handcrafted: {
      hasHandNote,
      hasHandArrow,
      hasMarker,
      hasProofMark,
      hasRedline,
    },
    buttonsCount,
    linkBtnCount,
    lines: code.split('\n').length
  });
}

writeFileSync('../../route-audit-output.json', JSON.stringify(auditData, null, 2), 'utf8');
console.log(`Audited ${auditData.length} routes written to route-audit-output.json`);
