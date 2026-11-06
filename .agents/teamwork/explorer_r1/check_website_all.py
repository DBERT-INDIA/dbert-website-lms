import os

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')
scan_path = os.path.join(agent_dir, 'clean_scan.txt')

website_matches = []
with open(scan_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\r\n')
        parts = line.split(':', 2)
        if len(parts) >= 3:
            path, lineno, content = parts[0], parts[1], parts[2]
            if path.startswith('apps\\website') or path.startswith('apps/website'):
                website_matches.append((path, lineno, content))

print(f"Total apps/website matches: {len(website_matches)}")
with open(os.path.join(agent_dir, 'website_matches.txt'), 'w', encoding='utf-8') as out:
    for p, l, c in website_matches:
        out.write(f"{p}:{l}:{c}\n")

from collections import Counter
counts = Counter(p for p, l, c in website_matches)
for p, c in counts.most_common():
    print(f"{c:4d} : {p}")
