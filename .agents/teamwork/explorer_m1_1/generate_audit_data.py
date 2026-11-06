import os
import re
import json

ROOT_DIR = r"c:\Users\user\Desktop\dbert-website-lms"

# Files/dirs to ignore
IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".pytest_cache",
    "__pycache__",
    ".agents",
    ".next",
    "_next",
    "cpanel-build",
    "scratch",
}

BINARY_EXTS = {
    ".zip", ".pdf", ".pptx", ".db", ".sqlite", ".sqlite3", ".pyc", ".pyd",
    ".dll", ".exe", ".so", ".tar.gz", ".tgz", ".png", ".jpg", ".jpeg",
    ".gif", ".ico", ".webp", ".woff", ".woff2", ".ttf", ".eot"
}

all_findings = []

for root, dirs, files in os.walk(ROOT_DIR):
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in BINARY_EXTS:
            continue
        filepath = os.path.join(root, f)
        rel_path = os.path.relpath(filepath, ROOT_DIR).replace("\\", "/")
        
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as fp:
                for line_idx, line in enumerate(fp, 1):
                    if "dbert.online" in line:
                        raw_snip = line.strip()
                        snip = raw_snip
                        if len(snip) > 200:
                            pos = snip.find("dbert.online")
                            start = max(0, pos - 40)
                            end = min(len(snip), pos + 100)
                            snip = ("..." if start > 0 else "") + snip[start:end] + ("..." if end < len(snip) else "")

                        # Determine target domain replacement
                        if "internship.dbert.online" in raw_snip:
                            replacement = "lms.dbert.in"
                        else:
                            replacement = "dbert.in"

                        # Determine classification
                        # 1. Intentional redirect rule
                        if rel_path == "deploy/dbert-unified-nginx.conf":
                            classification = "Intentional redirect rule"
                        elif rel_path in ("apps/website/.htaccess", "apps/website/public/.htaccess", "cpanel_public_html/.htaccess"):
                            classification = "Intentional redirect rule"
                        elif rel_path == "deploy/deploy_ec2_unified.sh" and "certbot" in raw_snip:
                            classification = "Intentional redirect rule"
                        elif rel_path == "deploy/FILEZILLA_DEPLOYMENT_GUIDE.md" and "Optional for 301 redirects" in raw_snip:
                            classification = "Intentional redirect rule"
                        # 2. Warning
                        elif rel_path.endswith(".md"):
                            classification = "Warning"
                        elif rel_path.startswith("dbert-api-package/docs/"):
                            classification = "Warning"
                        elif rel_path.endswith(".css") or "/*" in raw_snip or raw_snip.startswith("//") or raw_snip.startswith("#"):
                            classification = "Warning"
                        elif "placeholder=" in raw_snip:
                            classification = "Warning"
                        # 3. Blocker
                        else:
                            classification = "Blocker"

                        all_findings.append({
                            "file": rel_path,
                            "line": line_idx,
                            "snippet": snip,
                            "replacement": replacement,
                            "classification": classification,
                        })
        except Exception as e:
            print(f"Error reading {rel_path}: {e}")

out_path = os.path.join(ROOT_DIR, ".agents/teamwork/explorer_m1_1/audit_data.json")
with open(out_path, "w", encoding="utf-8") as out:
    json.dump(all_findings, out, indent=2)

print(f"Total findings: {len(all_findings)}")
counts = {}
for item in all_findings:
    c = item["classification"]
    counts[c] = counts.get(c, 0) + 1
print("Counts by classification:", counts)

file_counts = {}
for item in all_findings:
    c = item["classification"]
    f = item["file"]
    file_counts.setdefault(f, {})[c] = file_counts.setdefault(f, {}).get(c, 0) + 1

print("\nFiles summary:")
for f, cdict in sorted(file_counts.items()):
    print(f"  {f}: {cdict}")
