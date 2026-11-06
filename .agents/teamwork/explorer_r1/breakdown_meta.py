import os
from collections import Counter

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')

counts = Counter()
with open(os.path.join(agent_dir, 'meta_jsonld_findings.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        file = line.split(':')[0]
        counts[file] += 1

print(f"Unique files with meta/JSON-LD dbert.online: {len(counts)}")
for file, cnt in counts.most_common(40):
    print(f"{cnt:4d} : {file}")
