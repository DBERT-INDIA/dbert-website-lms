import os
import re

WEBSITE_CONTENT_DIR = r"c:\Users\user\Desktop\dbert-website-lms\dbert-api-package\website-content"
ROOT_DIR = r"c:\Users\user\Desktop\dbert-website-lms"

results = []

for root, dirs, files in os.walk(WEBSITE_CONTENT_DIR):
    for f in files:
        filepath = os.path.join(root, f)
        rel_path = os.path.relpath(filepath, ROOT_DIR).replace("\\", "/")
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as fp:
                for line_idx, line in enumerate(fp, 1):
                    if "dbert.online" in line:
                        snip = line.strip()
                        # Determine classification and replacement
                        classification = "Blocker"
                        if "internship.dbert.online" in line:
                            replacement = "lms.dbert.in"
                        else:
                            replacement = "dbert.in"
                            
                        # If it's a comment or placeholder
                        if snip.startswith("//") or snip.startswith("/*") or snip.startswith("*") or snip.startswith("#"):
                            classification = "Warning"
                        elif "placeholder=" in snip:
                            classification = "Warning"
                        elif rel_path.endswith(".css"):
                            classification = "Warning"
                            
                        results.append({
                            "path": rel_path,
                            "line": line_idx,
                            "snippet": snip,
                            "replacement": replacement,
                            "classification": classification
                        })
        except Exception as e:
            print(f"Error {filepath}: {e}")

print(f"Found {len(results)} occurrences in dbert-api-package/website-content")
blockers = sum(1 for r in results if r["classification"] == "Blocker")
warnings = sum(1 for r in results if r["classification"] == "Warning")
print(f"Blockers: {blockers}, Warnings: {warnings}")

# Let's inspect unique files
unique_files = sorted(set(r["path"] for r in results))
print(f"Across {len(unique_files)} files.")
