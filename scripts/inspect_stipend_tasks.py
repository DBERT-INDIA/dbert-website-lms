with open('apps/portal/templates/stipend_tasks.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<div class=[\'\"].*?gate.*?[\'\"]>|is_provisional|isProvisional|balance', text, re.IGNORECASE)
print(f"Matches in stipend_tasks.html ({len(matches)}):")
for m in matches[:15]:
    print(m)
