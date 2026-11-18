with open('apps/portal/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'@csrf\.exempt.*?\n|csrf\.exempt.*?\n', text)
print(matches)
