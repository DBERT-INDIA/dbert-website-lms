import os

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')
scan_path = os.path.join(agent_dir, 'clean_scan.txt')

all_findings = []
with open(scan_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\r\n')
        parts = line.split(':', 2)
        if len(parts) >= 3:
            path, lineno, content = parts[0], parts[1], parts[2]
            all_findings.append((path.replace('\\', '/'), int(lineno), content))

print(f"Total findings loaded: {len(all_findings)}")

# Group by category
categories = {
    "ENV_FILES": [],
    "PORTAL_CODE": [],
    "PORTAL_CONFIG_DEPLOY": [],
    "PORTAL_TEMPLATES": [],
    "PORTAL_STATIC_SEO": [],
    "DEPLOY_CONFIGS": [],
    "DEPLOY_DOCS": [],
    "WEBSITE_SOURCE_CONFIG": [],
    "WEBSITE_STATIC_BUILD_CPANEL": [],
    "WEBSITE_STATIC_BUILD_APPS": [],
    "DBERT_API_PACKAGE": [],
    "ROOT_SCRIPTS_DOCS": [],
    "SCRATCH_FILES": []
}

for path, lineno, content in all_findings:
    if path.startswith('apps/portal/.env'):
        categories["ENV_FILES"].append((path, lineno, content))
    elif path.startswith('apps/portal/cgi-bin'):
        categories["PORTAL_CODE"].append((path, lineno, content))
    elif path.startswith('apps/portal/app.py'):
        categories["PORTAL_CODE"].append((path, lineno, content))
    elif path.startswith('apps/portal/deploy'):
        categories["PORTAL_CONFIG_DEPLOY"].append((path, lineno, content))
    elif path.startswith('apps/portal/templates'):
        categories["PORTAL_TEMPLATES"].append((path, lineno, content))
    elif path.startswith('apps/portal/sitemap') or path.startswith('apps/portal/robots'):
        categories["PORTAL_STATIC_SEO"].append((path, lineno, content))
    elif path.startswith('deploy/'):
        if path.endswith(('.conf', '.service', '.sh')):
            categories["DEPLOY_CONFIGS"].append((path, lineno, content))
        else:
            categories["DEPLOY_DOCS"].append((path, lineno, content))
    elif path.startswith('cpanel_public_html/'):
        categories["WEBSITE_STATIC_BUILD_CPANEL"].append((path, lineno, content))
    elif path.startswith('apps/website/out/') or path.startswith('apps/website/') and any(path.endswith(ext) for ext in ['.html', '.txt', '.js', '.css', '.xml']) and not path.startswith('apps/website/src'):
        categories["WEBSITE_STATIC_BUILD_APPS"].append((path, lineno, content))
    elif path.startswith('dbert-api-package/'):
        categories["DBERT_API_PACKAGE"].append((path, lineno, content))
    elif path.startswith('scratch/'):
        categories["SCRATCH_FILES"].append((path, lineno, content))
    else:
        categories["ROOT_SCRIPTS_DOCS"].append((path, lineno, content))

for cat, items in categories.items():
    print(f"{cat}: {len(items)} items")

with open(os.path.join(agent_dir, 'grouped_findings.txt'), 'w', encoding='utf-8') as out:
    for cat, items in categories.items():
        out.write(f"\n{'='*70}\n{cat} ({len(items)} items)\n{'='*70}\n")
        # For huge categories like static build or sitemap, summarize
        for p, l, c in items[:50]:
            out.write(f"{p}:{l} -> {c[:120]}\n")
        if len(items) > 50:
            out.write(f"... and {len(items)-50} more items in {cat}\n")

print("Grouped findings written.")
