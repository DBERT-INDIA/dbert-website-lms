with open('apps/website/src/components/layout/ProgramDetailTemplate.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of ProgramDetailTemplate.tsx:", len(text))
for line in text.splitlines():
    if any(k in line.lower() for k in ['enroll', 'razorpay', 'payment', 'apply', 'button']):
        print(line[:100])
