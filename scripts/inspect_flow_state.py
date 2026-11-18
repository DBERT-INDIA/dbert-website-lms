with open('apps/portal/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def get_intern_flow_state' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(i+60, len(lines))):
            print(lines[j], end="")
        break
