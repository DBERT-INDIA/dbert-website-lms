import os
from collections import Counter

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')
cpanel_file = os.path.join(agent_dir, 'cpanel_matches.txt')

patterns = Counter()
samples = {}

with open(cpanel_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\r\n')
        parts = line.split(':', 2)
        if len(parts) >= 3:
            path, lineno, content = parts[0], parts[1], parts[2]
            # Identify pattern
            if 'internship.dbert.online' in content:
                pat = 'internship.dbert.online link/ref'
            elif 'contactus@dbert.online' in content:
                pat = 'contactus@dbert.online email/schema'
            elif 'https://dbert.online' in content:
                pat = 'https://dbert.online URL/schema'
            elif 'dbert.online' in content:
                pat = 'dbert.online text/comment'
            else:
                pat = 'other'
            patterns[pat] += 1
            if pat not in samples:
                samples[pat] = []
            if len(samples[pat]) < 5:
                samples[pat].append((path, lineno, content[:120]))

with open(os.path.join(agent_dir, 'cpanel_breakdown.txt'), 'w', encoding='utf-8') as out:
    out.write("CPanel Matches Pattern Breakdown:\n")
    for pat, cnt in patterns.most_common():
        out.write(f"\n[{pat}]: {cnt} occurrences\n")
        for p, l, c in samples[pat]:
            out.write(f"  {p}:{l} -> {c}\n")

print("Wrote cpanel_breakdown.txt")
