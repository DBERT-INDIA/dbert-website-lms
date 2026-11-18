with open('apps/website/src/app/learners/courses/data-analytics/page.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'href=[\'\"][^\'\"]+[\'\"]', text)
print(f"Links in data-analytics/page.tsx ({len(matches)}):")
for m in set(matches):
    print(" -", m)
