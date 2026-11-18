with open('apps/portal/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '/api/jobs/apply' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(i+45, len(lines))):
            print(lines[j], end="")
        break
