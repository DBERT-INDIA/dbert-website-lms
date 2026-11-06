import json
import time
import psutil
import os
import sys
import subprocess

TRACKING_FILE = "data/dispatch_tracking_409.json"

def log(msg):
    print(msg, flush=True)

def get_stats():
    try:
        with open(TRACKING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        sent = sum(1 for x in data if x.get("status") == "SENT")
        pending = sum(1 for x in data if x.get("status") == "PENDING")
        total = len(data)
        return sent, pending, total
    except Exception as e:
        log(f"Error reading tracking: {e}")
        return 0, 409, 409

def kill_related_processes():
    log("Terminating background dispatcher and watchdog processes...")
    target_scripts = [
        "dispatch_409_provisional.py",
        "quota_watchdog_and_dispatcher.py",
        "remote_exec.py"
    ]
    my_pid = os.getpid()
    killed = 0
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if p.pid == my_pid:
                continue
            name = (p.info['name'] or '').lower()
            if 'python' in name:
                cmdline = " ".join(p.info['cmdline'] or [])
                for target in target_scripts:
                    if target in cmdline:
                        log(f"  Killing PID {p.pid} ({target})...")
                        p.kill()
                        killed += 1
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    log(f"Terminated {killed} processes.")

def main():
    log("Starting completion watcher for 409 provisional candidate emails...")
    while True:
        sent, pending, total = get_stats()
        log(f"Progress: {sent}/{total} SENT ({pending} pending)")
        if pending == 0 and sent >= 409:
            log("\n>>> ALL 409 EMAILS HAVE BEEN DELIVERED SUCCESSFULLY! <<<")
            break
        time.sleep(15)

    log("Waiting 15 seconds for telemetry dispatches to flush...")
    time.sleep(15)

    kill_related_processes()
    log("All processes stopped successfully.")

if __name__ == "__main__":
    main()
