with open('apps/portal/templates/job_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'external|applyUrl|external_url|application_url|apply', text, re.IGNORECASE)
print(f"Matches in job_detail.html ({len(matches)}):")
for line in text.splitlines():
    if any(k in line.lower() for k in ['applyurl', 'external', 'redirect', 'modal', 'post_apply']):
        print(line[:100])
