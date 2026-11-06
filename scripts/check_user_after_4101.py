import json

with open(r'C:\Users\user\.gemini\antigravity\brain\542c2e0b-55d0-41c9-9b46-721bf0724211\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(4101, len(lines)):
    obj = json.loads(lines[idx])
    src = obj.get('source')
    content = obj.get('content', '')
    if src == 'USER_EXPLICIT':
        print(f"\n--- Line {idx} [USER] ---")
        print(content)
