with open('apps/portal/templates/portal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(function apiCall|async function apiCall|const res\s*=\s*await fetch\([^\)]+\))', text)
for m in matches[:10]:
    print(m)

# Search for /api/
api_endpoints = re.findall(r'[\'\"`]/[a-zA-Z0-9_\-\/]+[\'\"`]', text)
api_set = sorted(list(set([a for a in api_endpoints if '/api' in a or '/portal' in a or '/intern' in a])))
print(f"APIs in portal.html ({len(api_set)}):")
for a in api_set[:25]:
    print(" -", a)
