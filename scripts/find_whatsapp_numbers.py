import os
import re

dirs_to_check = [
    'apps/portal/templates',
    'apps/portal',
    'apps/website/src',
    'scripts'
]

patterns = [
    re.compile(r'wa\.me/(\d+)', re.IGNORECASE),
    re.compile(r'whatsapp.*?(?:(\+91[\s\-]?[0-9]{5}[\s\-]?[0-9]{5}|\+91[0-9]{10}|91[0-9]{10}))', re.IGNORECASE),
    re.compile(r'(?:admissions|support|concierge|helpline).*?(?:(\+91[\s\-]?[0-9]{5}[\s\-]?[0-9]{5}|\+91[0-9]{10}|91[0-9]{10}))', re.IGNORECASE)
]

found = set()

for d in dirs_to_check:
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith(('.py', '.html', '.tsx', '.ts', '.md', '.json', '.env')):
                p = os.path.join(root, f)
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                        for idx, line in enumerate(fp, 1):
                            if 'wa.me' in line or 'whatsapp' in line.lower() or 'admissions' in line.lower():
                                for pat in patterns:
                                    m = pat.search(line)
                                    if m:
                                        found.add((m.group(0), line.strip()[:100], f"{f}:{idx}"))
                except Exception:
                    pass

print("=== FOUND WHATSAPP REFERENCES ===")
for num, line, loc in sorted(found):
    print(f"[{loc}] -> {num} | {line}")
