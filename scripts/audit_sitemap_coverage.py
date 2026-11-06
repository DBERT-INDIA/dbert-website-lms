import os
import re

app_dir = r'c:\Users\user\Desktop\dbert-website-lms\apps\website\src\app'
pages = []
for root, dirs, files in os.walk(app_dir):
    if any(f.startswith('page.') for f in files):
        rel = os.path.relpath(root, app_dir).replace('\\', '/')
        route = '' if rel == '.' else '/' + rel
        pages.append(route)

with open(r'c:\Users\user\Desktop\dbert-website-lms\apps\website\src\data\seo.config.ts', 'r', encoding='utf-8') as f:
    seo_text = f.read()

# Extract keys like '/...': {
matches = re.findall(r"['\"](/[^'\"]*)['\"]\s*:\s*\{", seo_text)
seo_keys = set(matches)

missing_in_seo = [p for p in pages if p not in seo_keys and not p.startswith('/_admin') and not p.startswith('/admin') and '[' not in p]
print('=== Real Pages Missing in seoConfig ===')
for p in sorted(missing_in_seo):
    print(p)

print('\n=== Configured in seoConfig but not a physical page ===')
for k in sorted(seo_keys):
    if k not in pages and '[' not in k:
        print(k)
