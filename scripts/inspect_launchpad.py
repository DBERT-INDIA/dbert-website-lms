with open('apps/website/src/app/learners/launchpad/LaunchpadClient.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of LaunchpadClient.tsx:", len(text))
for line in text.splitlines()[:40]:
    print(line)
