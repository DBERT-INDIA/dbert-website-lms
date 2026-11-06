import os
from collections import Counter

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')
scan_path = os.path.join(agent_dir, 'clean_scan.txt')

other_matches = []
with open(scan_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\r\n')
        parts = line.split(':', 2)
        if len(parts) >= 3:
            path, lineno, content = parts[0], parts[1], parts[2]
            if not path.startswith('apps\\website') and not path.startswith('apps/website') and not path.startswith('cpanel_public_html'):
                other_matches.append((path, lineno, content))

print(f"Total other matches: {len(other_matches)}")
counts = Counter(p for p, l, c in other_matches)
for p, c in counts.most_common():
    print(f"{c:4d} : {p}")
