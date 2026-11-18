with open('apps/portal/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'def send_.*?email.*?\n', text)
print(matches)

matches2 = re.findall(r'from services\.email.*?import.*?\n', text)
print(matches2)
