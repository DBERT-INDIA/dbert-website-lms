import re
from collections import defaultdict

IN_FILE = r"c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_m1_1\all_grouped_matches.txt"

with open(IN_FILE, "r", encoding="utf-8") as f:
    text = f.read()

file_blocks = text.strip().split("\n\n")

categories = defaultdict(list)

for block in file_blocks:
    if not block.strip():
        continue
    lines = block.split("\n")
    header = lines[0] # e.g. "FILE: deploy/dbert-unified-nginx.conf (6 occurrences)"
    m = re.match(r"FILE:\s*(.*?)\s*\((\d+)\s+occurrences\)", header)
    if not m:
        continue
    path = m.group(1)
    count = int(m.group(2))
    
    entries = []
    for line in lines[1:]:
        line = line.strip()
        if line.startswith("Line "):
            entries.append(line)

    if path.startswith("scratch/"):
        categories["scratch"].append((path, count, entries))
    elif path.startswith("deploy/"):
        categories["deploy"].append((path, count, entries))
    elif path.startswith("dbert-api-package/docs/"):
        categories["dbert-api-package/docs"].append((path, count, entries))
    elif path.startswith("dbert-api-package/website-content/"):
        categories["dbert-api-package/website-content"].append((path, count, entries))
    elif path.startswith("cpanel_public_html/"):
        categories["cpanel_public_html"].append((path, count, entries))
    elif path.startswith("apps/website/"):
        categories["apps/website"].append((path, count, entries))
    elif path.startswith("apps/portal/"):
        categories["apps/portal"].append((path, count, entries))
    elif path.endswith(".md"):
        categories["markdown_docs"].append((path, count, entries))
    else:
        categories["other"].append((path, count, entries))

for cat, files in sorted(categories.items()):
    total_occs = sum(c for _, c, _ in files)
    print(f"=== {cat}: {len(files)} files, {total_occs} occurrences ===")
    for p, c, _ in files:
        print(f"  {p} ({c})")
