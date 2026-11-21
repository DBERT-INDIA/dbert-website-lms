#!/usr/bin/env python3
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\user\Desktop\dbert-website-lms")
SCRIPT = PROJECT_ROOT / "scripts" / "execute_dual_whatsapp_dispatch.py"

print("="*70)
print("LAUNCHING DUAL-ACCOUNT WHATSAPP DISPATCH WORKERS IN PARALLEL")
print("="*70)
print("Account 1: 26 messages (13 ₹499 + 13 ₹299)")
print("Account 2: 24 messages (12 ₹499 + 12 ₹299)")
print("Total: 50 targeted high-conversion messages")
print("="*70)

# Launch Account 1 worker
p1 = subprocess.Popen([sys.executable, str(SCRIPT), "--account", "1"])
print(f"[OK] Launched Account 1 Worker (PID {p1.pid})")

# Stagger start by 5 seconds to avoid simultaneous network/display contention
time.sleep(5)

# Launch Account 2 worker
p2 = subprocess.Popen([sys.executable, str(SCRIPT), "--account", "2"])
print(f"[OK] Launched Account 2 Worker (PID {p2.pid})")

print("\nBoth workers are running in parallel.")
print("Monitoring execution until completion...\n")

# Wait for both processes
while True:
    ret1 = p1.poll()
    ret2 = p2.poll()
    
    if ret1 is not None and ret2 is not None:
        print(f"\nWorker 1 finished with exit code: {ret1}")
        print(f"Worker 2 finished with exit code: {ret2}")
        break
    time.sleep(5)

print("\n=== DUAL DISPATCH COMPLETED ===")
