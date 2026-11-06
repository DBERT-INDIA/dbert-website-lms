import os

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')

with open(os.path.join(agent_dir, 'portal_matches.txt'), 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(os.path.join(agent_dir, 'portal_summary.txt'), 'w', encoding='utf-8') as out:
    for i, l in enumerate(lines, 1):
        parts = l.split(':', 2)
        path = parts[0]
        lineno = parts[1]
        content = parts[2][:120].strip() if len(parts) > 2 else ''
        out.write(f"{i:2d}: {path}:{lineno} -> {content}\n")

print(f"Wrote {len(lines)} portal matches to portal_summary.txt")
