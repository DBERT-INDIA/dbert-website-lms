import urllib.request
import re

req = urllib.request.Request('http://127.0.0.1:5000/internships')
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')
    print('HTTP Code:', resp.status)
    domains = re.findall(r'<div class="meta">\s*<span class="pill">([^<]+)</span>', html)
    print('Domains in first 8 cards:', domains[:8])
    summary = re.search(r'Page <strong>1</strong> of <strong>(\d+)</strong> \((\d+) total', html)
    if summary:
        print(f'Summary: Page 1 of {summary.group(1)} ({summary.group(2)} total opportunities)')
    print('Refresh feed link present:', '/internships/refresh-feed' in html)
