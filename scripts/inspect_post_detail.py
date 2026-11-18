with open('apps/portal/templates/post_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Length of post_detail.html:", len(text))
for line in text.splitlines():
    if any(k in line.lower() for k in ['apply', 'modal', 'external', 'comment', 'submit']):
        print(line[:100])
