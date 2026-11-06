import os, re

patterns = [r'smtp', r'passw', r'secret', r'gmail', r'app_pass']
for root, dirs, files in os.walk('.'):
    if any(x in root for x in ['.git', 'node_modules', '.next', 'outputs', 'venv']):
        continue
    for f in files:
        if f.endswith(('.env', '.py', '.json', '.yaml', '.yml', '.txt', '.sh', '.md')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    for line in content.splitlines():
                        if any(re.search(pat, line, re.I) for pat in patterns) and ('=' in line or ':' in line):
                            clean = line.strip()
                            if len(clean) < 120 and not clean.startswith('//') and not clean.startswith('/*'):
                                if any(x in clean.lower() for x in ['smtp_user', 'smtp_pass', 'mail_user', 'mail_pass', 'gmail']):
                                    print(f"{p}: {clean}")
            except:
                pass
