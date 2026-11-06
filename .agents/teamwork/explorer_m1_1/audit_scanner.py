import os
import re

ROOT_DIR = r"c:\Users\user\Desktop\dbert-website-lms"
OUTPUT_FILE = r"c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_m1_1\all_matches.tsv"

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".pytest_cache",
    "__pycache__",
    ".agents/teamwork",
    ".next",
    "cpanel-build",
}

BINARY_EXTENSIONS = {
    ".zip", ".pdf", ".pptx", ".db", ".sqlite", ".sqlite3", ".pyc", ".pyd",
    ".dll", ".exe", ".so", ".tar.gz", ".tgz", ".png", ".jpg", ".jpeg",
    ".gif", ".ico", ".webp", ".woff", ".woff2", ".ttf", ".eot"
}

matches = []

for root, dirs, files in os.walk(ROOT_DIR):
    rel_root = os.path.relpath(root, ROOT_DIR).replace("\\", "/")
    
    # Check if we should skip this directory
    skip = False
    for ign in IGNORE_DIRS:
        if rel_root == ign or rel_root.startswith(ign + "/"):
            skip = True
            break
    if skip:
        dirs[:] = []
        continue

    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in BINARY_EXTENSIONS:
            continue
        filepath = os.path.join(root, f)
        rel_path = os.path.relpath(filepath, ROOT_DIR).replace("\\", "/")
        
        # Avoid scanning our own output files
        if rel_path.startswith(".agents/teamwork/explorer_m1_1/"):
            continue

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file_obj:
                for line_idx, line in enumerate(file_obj, 1):
                    if "dbert.online" in line:
                        matches.append((rel_path, line_idx, line.strip()))
        except Exception as e:
            print(f"Error reading {rel_path}: {e}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("FilePath\tLineNumber\tSnippet\n")
    for path, line_no, snippet in matches:
        out.write(f"{path}\t{line_no}\t{snippet}\n")

print(f"Total occurrences found: {len(matches)}")
