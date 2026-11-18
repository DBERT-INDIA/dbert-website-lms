with open('apps/portal/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'def.*csrf.*?\n|.*csrf.*=.*?\n', text, re.IGNORECASE)
for m in matches[:15]:
    print(m.strip())
