with open('apps/portal/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '@app.route("/api/' in l or "@app.route('/api/" in l:
        print(f"Line {i+1}: {l.strip()}")
        if i > 500: # just sample a few
            break
