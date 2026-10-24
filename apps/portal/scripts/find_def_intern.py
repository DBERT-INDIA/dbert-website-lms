with open('apps/portal/app.py', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if 'def current_intern' in line:
            print(f"Line {i}: {line.strip()}")
            break
