import os
import re

ROOT_DIR = r"c:\Users\user\Desktop\dbert-website-lms"
OUTPUT_FILE = r"c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_m1_1\fast_matches.tsv"

IGNORE_DIR_NAMES = {
    ".git",
    "node_modules",
    ".pytest_cache",
    "__pycache__",
    ".agents",
    ".next",
    "_next",
    "cpanel-build",
}

BINARY_EXTENSIONS = {
    ".zip", ".pdf", ".pptx", ".db", ".sqlite", ".sqlite3", ".pyc", ".pyd",
    ".dll", ".exe", ".so", ".tar.gz", ".tgz", ".png", ".jpg", ".jpeg",
    ".gif", ".ico", ".webp", ".woff", ".woff2", ".ttf", ".eot"
}

matches = []

for root, dirs, files in os.walk(ROOT_DIR):
    # prune ignore dirs in place
    dirs[:] = [d for d in dirs if d not in IGNORE_DIR_NAMES]
    
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in BINARY_EXTENSIONS:
            continue
            
        filepath = os.path.join(root, f)
        rel_path = os.path.relpath(filepath, ROOT_DIR).replace("\\", "/")
        
        # skip our own outputs
        if rel_path.startswith(".agents/"):
            continue

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file_obj:
                for line_idx, line in enumerate(file_obj, 1):
                    if "dbert.online" in line:
                        snip = line.strip()
                        if len(snip) > 200:
                            # find position of dbert.online and take window
                            pos = snip.find("dbert.online")
                            start = max(0, pos - 50)
                            end = min(len(snip), pos + 100)
                            snip = ("..." if start > 0 else "") + snip[start:end] + ("..." if end < len(snip) else "")
                        matches.append((rel_path, line_idx, snip))
        except Exception as e:
            print(f"Error reading {rel_path}: {e}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("FilePath\tLineNumber\tSnippet\n")
    for path, line_no, snippet in matches:
        out.write(f"{path}\t{line_no}\t{snippet}\n")

print(f"Total occurrences found: {len(matches)}")
