import os

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')

meta_jsonld_findings = []

for folder in ['cpanel_public_html', 'apps/website', 'apps/portal']:
    dir_path = os.path.join(root, folder)
    for dirpath, dirnames, filenames in os.walk(dir_path):
        if 'node_modules' in dirnames:
            dirnames.remove('node_modules')
        if '.next' in dirnames:
            dirnames.remove('.next')
        for fname in filenames:
            if fname.endswith(('.html', '.tsx', '.jsx', '.ts', '.js', '.txt')):
                fpath = os.path.join(dirpath, fname)
                relpath = os.path.relpath(fpath, root).replace('\\', '/')
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        for idx, line in enumerate(f, 1):
                            if 'dbert.online' in line:
                                if any(k in line for k in ['og:', 'twitter:', 'ld+json', '@type', 'sameAs', 'canonical', 'url":']):
                                    meta_jsonld_findings.append((relpath, idx, line.strip()))
                except Exception as e:
                    pass

print(f"Total meta/JSON-LD findings: {len(meta_jsonld_findings)}")
with open(os.path.join(agent_dir, 'meta_jsonld_findings.txt'), 'w', encoding='utf-8') as out:
    for r, i, l in meta_jsonld_findings:
        out.write(f"{r}:{i} -> {l[:150]}\n")
