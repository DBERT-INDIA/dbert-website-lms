import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')

keywords = ['rakholiya', 'vasu', 'janhvi', 'chandel', 'symbiosis skills', 'chhatrapati shahu']

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.next' in root:
        continue
    for f in files:
        if f.endswith(('.json', '.csv', '.py', '.txt', '.log')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read().lower()
                    for kw in keywords:
                        if kw in content:
                            print(f"Found '{kw}' in {path}")
            except Exception as e:
                pass
