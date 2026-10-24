with open('apps/portal/app.py', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if '@app.route("/internships' in line:
            print(f"{i}: {line.strip()}")
