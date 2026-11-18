with open('apps/portal/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def ' in l and 'apply' in l:
        print(f"Line {i+1}: {l.strip()}")
    elif '@app.route' in l and 'apply' in l:
        print(f"Route Line {i+1}: {l.strip()}")
