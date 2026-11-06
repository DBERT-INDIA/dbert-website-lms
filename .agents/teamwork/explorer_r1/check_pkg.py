import os

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')
scan_path = os.path.join(agent_dir, 'clean_scan.txt')

pkg_matches = []
with open(scan_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\r\n')
        parts = line.split(':', 2)
        if len(parts) >= 3:
            path, lineno, content = parts[0], parts[1], parts[2]
            if 'dbert-api-package' in path:
                pkg_matches.append((path, lineno, content))

print(f"Total dbert-api-package matches: {len(pkg_matches)}")
with open(os.path.join(agent_dir, 'pkg_matches.txt'), 'w', encoding='utf-8') as out:
    for p, l, c in pkg_matches:
        out.write(f"{p}:{l}:{c}\n")

from collections import Counter
counts = Counter(p for p, l, c in pkg_matches)
for p, c in counts.most_common():
    print(f"{c:4d} : {p}")
