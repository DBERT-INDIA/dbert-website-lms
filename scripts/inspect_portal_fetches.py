with open('apps/portal/templates/portal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'fetch\([\'\"/][^\'\"]+[\'\"]\)', text)
unique_fetches = sorted(list(set(matches)))
print(f"Total unique fetch calls in portal.html: {len(unique_fetches)}")
for u in unique_fetches:
    print(" -", u)
