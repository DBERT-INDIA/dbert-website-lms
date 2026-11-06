import json

with open(r'C:\Users\user\.gemini\antigravity\brain\542c2e0b-55d0-41c9-9b46-721bf0724211\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

found_idx = -1
for i, l in enumerate(lines):
    if 'approved send email to ain.sharma.abhinav@gmail.com as test' in l:
        found_idx = i
        break

print(f"Found at line: {found_idx}")
if found_idx != -1:
    for idx in range(found_idx, min(found_idx + 15, len(lines))):
        obj = json.loads(lines[idx])
        src = obj.get('source')
        content = obj.get('content', '')
        if src == 'USER_EXPLICIT':
            print(f"Step {idx} [USER]: {content[:300]}")
        elif src == 'MODEL':
            print(f"Step {idx} [MODEL]: {content[:300]}")
