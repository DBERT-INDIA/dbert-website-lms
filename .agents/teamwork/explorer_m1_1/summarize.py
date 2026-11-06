import csv
from collections import defaultdict

TSV_FILE = r"c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_m1_1\fast_matches.tsv"

files_summary = defaultdict(list)

with open(TSV_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        path = row["FilePath"]
        line_no = row["LineNumber"]
        snippet = row["Snippet"]
        files_summary[path].append((line_no, snippet))

print(f"Total unique files with occurrences: {len(files_summary)}")

# Group files by top-level section
categories = {
    "apps/portal": [],
    "apps/website/src": [],
    "apps/website (static/other)": [],
    "cpanel_public_html": [],
    "dbert-api-package/website-content": [],
    "dbert-api-package (backend/docs/env)": [],
    "deploy": [],
    "scripts": [],
    "documentation & root markdown": [],
    "other": []
}

for path, items in files_summary.items():
    if path.startswith("apps/portal/"):
        categories["apps/portal"].append((path, len(items)))
    elif path.startswith("apps/website/src/"):
        categories["apps/website/src"].append((path, len(items)))
    elif path.startswith("apps/website/"):
        categories["apps/website (static/other)"].append((path, len(items)))
    elif path.startswith("cpanel_public_html/"):
        categories["cpanel_public_html"].append((path, len(items)))
    elif path.startswith("dbert-api-package/website-content/"):
        categories["dbert-api-package/website-content"].append((path, len(items)))
    elif path.startswith("dbert-api-package/"):
        categories["dbert-api-package (backend/docs/env)"].append((path, len(items)))
    elif path.startswith("deploy/"):
        categories["deploy"].append((path, len(items)))
    elif path.startswith("scripts/"):
        categories["scripts"].append((path, len(items)))
    elif path.endswith(".md"):
        categories["documentation & root markdown"].append((path, len(items)))
    else:
        categories["other"].append((path, len(items)))

for cat, flist in categories.items():
    total_matches = sum(count for _, count in flist)
    print(f"\n=== {cat} ({len(flist)} files, {total_matches} occurrences) ===")
    for p, c in sorted(flist, key=lambda x: x[0]):
        print(f"  {p} ({c})")
