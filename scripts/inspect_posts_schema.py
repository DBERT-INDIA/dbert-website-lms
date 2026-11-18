with open('apps/portal/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'CREATE TABLE IF NOT EXISTS posts.*?\);', text, re.IGNORECASE | re.DOTALL)
if m:
    print(m.group(0))
