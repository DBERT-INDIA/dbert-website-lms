import json

log_path = r'C:\Users\user\.gemini\antigravity\brain\542c2e0b-55d0-41c9-9b46-721bf0724211\.system_generated\logs\transcript.jsonl'
out_path = r'c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_survey_3\transcript_summary.txt'

with open(log_path, 'r', encoding='utf-8', errors='replace') as f, open(out_path, 'w', encoding='utf-8') as out:
    for i, line in enumerate(f):
        if i < 2800:
            continue
        try:
            data = json.loads(line)
        except Exception:
            continue
        src = data.get('source')
        if src in ('USER_EXPLICIT', 'USER'):
            text = str(data.get('content', ''))
            out.write(f"\n=== User message at line {i} ===\n{text}\n")
        elif src == 'MODEL':
            # check if model discussed email results
            text = str(data.get('content', ''))
            if any(k in text.lower() for k in ['delivery', 'test 5', 'inbox', 'spam', 'ain.sharma', 'ajnatechrpa']):
                out.write(f"\n--- Model mention at line {i} ---\n{text[:600]}\n...\n")

print("Done writing transcript_summary.txt")
