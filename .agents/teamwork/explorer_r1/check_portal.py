import os

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')
scan_path = os.path.join(agent_dir, 'clean_scan.txt')

portal_matches = []
with open(scan_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\r\n')
        parts = line.split(':', 2)
        if len(parts) >= 3:
            path, lineno, content = parts[0], parts[1], parts[2]
            if path.startswith('apps\\portal') or path.startswith('apps/portal'):
                portal_matches.append((path, lineno, content))

print(f"Total apps/portal matches: {len(portal_matches)}")
with open(os.path.join(agent_dir, 'portal_matches.txt'), 'w', encoding='utf-8') as out:
    for p, l, c in portal_matches:
        out.write(f"{p}:{l}:{c}\n")

for p, l, c in portal_matches:
    # Print short snippet if too long
    snip = c if len(c) < 120 else c[:117] + '...'
    print(f"{p}:{l} -> {snip}")
