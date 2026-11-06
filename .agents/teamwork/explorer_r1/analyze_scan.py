import os
from collections import Counter

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')
scan_path = os.path.join(agent_dir, 'clean_scan.txt')

counts = Counter()
files_lines = {}

with open(scan_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\r\n')
        if not line:
            continue
        parts = line.split(':', 2)
        if len(parts) >= 2:
            relpath = parts[0]
            lineno = parts[1]
            content = parts[2] if len(parts) > 2 else ''
            counts[relpath] += 1
            if relpath not in files_lines:
                files_lines[relpath] = []
            files_lines[relpath].append((lineno, content))

print(f"Total unique files with dbert.online: {len(counts)}")
summary_path = os.path.join(agent_dir, 'files_summary.txt')

with open(summary_path, 'w', encoding='utf-8') as out:
    out.write(f"Total unique files: {len(counts)}\n\n")
    for file, count in counts.most_common():
        out.write(f"{count:4d} : {file}\n")

print(f"Summary written to {summary_path}")
