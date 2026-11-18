import psutil

for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    if p.info['name'] and 'chrome' in p.info['name'].lower():
        print(f"PID: {p.info['pid']} | Cmd: {' '.join(p.info['cmdline'] or [])[:120]}")
