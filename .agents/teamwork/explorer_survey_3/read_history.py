import json

log_path = r'C:\Users\user\.gemini\antigravity\brain\542c2e0b-55d0-41c9-9b46-721bf0724211\.system_generated\logs\transcript.jsonl'
with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
    for i, line in enumerate(f):
        if i < 2400:
            continue
        try:
            data = json.loads(line)
        except Exception:
            continue
        if data.get('source') == 'USER_EXPLICIT':
            text = str(data.get('content', ''))
            print(f"=== Message at line {i} ===")
            print(text)
            print("-" * 50)
