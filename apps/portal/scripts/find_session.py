with open('apps/portal/app.py', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if 'session.get("intern_id")' in line or "session.get('intern_id')" in line or "current_intern" in line:
            print(f"{i}: {line.strip()[:100]}")
            if i > 2500:
                break
