with open('apps/website/src/app/learners/launchpad/page.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of launchpad/page.tsx:", len(text))
for line in text.splitlines()[:50]:
    print(line)
