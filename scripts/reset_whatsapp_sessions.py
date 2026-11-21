import os
import shutil
import time
from pathlib import Path

aivara_dir = Path(r"C:\Users\user\Desktop\aivara\aivara")
project_dir = Path(r"C:\Users\user\Desktop\dbert-website-lms")
timestamp = time.strftime("%Y%m%d_%H%M%S")

for acc in [1, 2]:
    session_dir = aivara_dir / f".chrome_session_account{acc}"
    backup_dir = aivara_dir / f".chrome_session_account{acc}_backup_{timestamp}"
    
    if session_dir.exists():
        print(f"Backing up Account {acc} session to {backup_dir.name}...")
        try:
            shutil.move(str(session_dir), str(backup_dir))
            print(f"[OK] Moved {session_dir.name} -> {backup_dir.name}")
        except Exception as e:
            print(f"[!] Could not move, trying copy & remove: {e}")
            shutil.copytree(str(session_dir), str(backup_dir))
            shutil.rmtree(str(session_dir), ignore_errors=True)

    # Recreate fresh empty directory
    session_dir.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Fresh empty session directory created at: {session_dir}")

    # Also clean local project session if exists
    local_session = project_dir / f".chrome_session_account{acc}"
    if local_session.exists():
        local_backup = project_dir / f".chrome_session_account{acc}_backup_{timestamp}"
        try:
            shutil.move(str(local_session), str(local_backup))
        except Exception:
            shutil.rmtree(str(local_session), ignore_errors=True)
        local_session.mkdir(parents=True, exist_ok=True)

print("\n[SUCCESS] Both WhatsApp Account 1 and Account 2 sessions have been completely logged out and reset.")
