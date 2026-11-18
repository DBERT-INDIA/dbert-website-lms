with open('apps/website/src/components/launchpad/LaunchpadDomainView.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of LaunchpadDomainView.tsx:", len(text))
for line in text.splitlines()[:50]:
    print(line)
