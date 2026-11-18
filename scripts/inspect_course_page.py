with open('apps/website/src/app/learners/courses/data-analytics/page.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

print('Length:', len(text))
for line in text.splitlines()[:50]:
    print(line)
