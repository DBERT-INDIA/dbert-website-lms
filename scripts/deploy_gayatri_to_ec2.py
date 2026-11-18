"""
scripts/deploy_gayatri_to_ec2.py
Automated production deployment daemon for Gayatri AI Platform (gayatrieducation.tech).
Transfers sanitized codebase, configures Python venv, SQLite WAL persistence,
systemd service (gayatri.service on port 5002), and Nginx reverse proxy.
"""

import os
import sys
import tarfile
import tempfile
import subprocess
import time

LOCAL_DIR = r"C:\Users\user\Desktop\gayatri\gayatrieducation.tech"
SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
EC2_HOST = "ubuntu@3.26.237.171"
REMOTE_APP_DIR = "/var/www/gayatri"
REMOTE_LOG_DIR = "/var/log/gayatri"

def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def should_exclude(tarinfo):
    name = tarinfo.name.replace("\\", "/")
    basename = os.path.basename(name)
    
    # Exclude zip and docx files
    if basename.endswith(".zip") or basename.endswith(".docx") or basename.endswith(".bak"):
        return None
    
    # Exclude heavy directories
    parts = name.split("/")
    for p in parts:
        if p in ["__pycache__", ".git", "venv", "cpanel", "gayatrieducation_info_cpanel", "scratch", "outputs"]:
            return None
    return tarinfo

def run_ssh_command(cmd, desc=""):
    if desc:
        log(f"Executing: {desc}")
    full_cmd = [
        "ssh",
        "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        EC2_HOST,
        cmd
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        log(f"[ERROR] Failed {desc} (code {res.returncode}):\n{res.stderr}\n{res.stdout}")
        return False, res.stdout, res.stderr
    return True, res.stdout, res.stderr

def main():
    log("=" * 70)
    log("GAYATRI AI PLATFORM — PRODUCTION EC2 DEPLOYMENT (gayatrieducation.tech)")
    log("=" * 70)
    log(f"Local Source: {LOCAL_DIR}")
    log(f"Remote Target: {EC2_HOST}:{REMOTE_APP_DIR}")
    log(f"Internal Port: 127.0.0.1:5002")
    log("=" * 70)

    # 1. Package sanitized archive
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tf:
        tar_path = tf.name

    log(f"Creating sanitized archive at {tar_path} ...")
    with tarfile.open(tar_path, "w:gz") as tar:
        for item in os.listdir(LOCAL_DIR):
            item_path = os.path.join(LOCAL_DIR, item)
            tar.add(item_path, arcname=item, filter=should_exclude)

    archive_size_mb = os.path.getsize(tar_path) / (1024 * 1024)
    log(f"Archive packaged successfully: {archive_size_mb:.2f} MB")

    # 2. Upload archive via SCP
    remote_archive = "/tmp/gayatri.tar.gz"
    log(f"Uploading archive to {EC2_HOST}:{remote_archive} ...")
    scp_cmd = [
        "scp",
        "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        tar_path,
        f"{EC2_HOST}:{remote_archive}"
    ]
    res = subprocess.run(scp_cmd, capture_output=True, text=True)
    try:
        os.remove(tar_path)
    except Exception:
        pass

    if res.returncode != 0:
        log(f"[ERROR] SCP upload failed: {res.stderr}")
        sys.exit(1)
    log("Upload complete.")

    # 3. Remote provisioning & extraction
    remote_script = f"""
    set -e
    echo "[1/7] Creating application and log directories..."
    sudo mkdir -p {REMOTE_APP_DIR}
    sudo mkdir -p {REMOTE_LOG_DIR}
    sudo mkdir -p {REMOTE_APP_DIR}/instance
    sudo mkdir -p {REMOTE_APP_DIR}/uploads

    echo "[2/7] Extracting codebase..."
    sudo tar -xzf {remote_archive} -C {REMOTE_APP_DIR}
    sudo rm -f {remote_archive}

    echo "[3/7] Setting up Python virtual environment..."
    if [ ! -d "{REMOTE_APP_DIR}/venv" ]; then
        sudo python3 -m venv {REMOTE_APP_DIR}/venv
    fi

    echo "[4/7] Installing production Python dependencies..."
    sudo {REMOTE_APP_DIR}/venv/bin/pip install --upgrade pip wheel
    sudo {REMOTE_APP_DIR}/venv/bin/pip install 'setuptools<70'
    sudo {REMOTE_APP_DIR}/venv/bin/pip install -r {REMOTE_APP_DIR}/requirements.txt

    echo "[5/7] Configuring SQLite WAL mode & permissions..."
    if [ -f "{REMOTE_APP_DIR}/instance/gayatri.db" ]; then
        sudo python3 -c "import sqlite3; con = sqlite3.connect('{REMOTE_APP_DIR}/instance/gayatri.db'); con.execute('PRAGMA journal_mode=WAL;'); con.close(); print('WAL mode enabled on instance/gayatri.db')"
    fi
    sudo chown -R ubuntu:ubuntu {REMOTE_APP_DIR}
    sudo chown -R ubuntu:ubuntu {REMOTE_LOG_DIR}
    sudo chmod -R 775 {REMOTE_APP_DIR}/instance
    sudo chmod -R 775 {REMOTE_APP_DIR}/uploads

    echo "[6/7] Installing systemd service (gayatri.service)..."
    sudo cp {REMOTE_APP_DIR}/deploy/gayatri.service /etc/systemd/system/gayatri.service
    sudo systemctl daemon-reload
    sudo systemctl enable gayatri.service
    sudo systemctl restart gayatri.service

    echo "[7/7] Configuring Nginx reverse proxy..."
    sudo cp {REMOTE_APP_DIR}/deploy/nginx.conf /etc/nginx/sites-available/gayatri.conf
    sudo ln -sf /etc/nginx/sites-available/gayatri.conf /etc/nginx/sites-enabled/gayatri.conf
    sudo nginx -t
    sudo systemctl reload nginx
    """

    ok, out, err = run_ssh_command(remote_script, "Remote Provisioning and Service Setup")
    if not ok:
        log("[ERROR] Remote provisioning encountered an error.")
        sys.exit(1)
    print(out)

    # 4. Verification checks
    time.sleep(3)
    log("Verifying service health and listening ports...")
    check_script = """
    echo "=== Service Status ==="
    sudo systemctl is-active gayatri.service
    
    echo "=== Port 5002 Probe ==="
    curl -I -s http://127.0.0.1:5002/ | head -n 5
    
    echo "=== Nginx Port 80 Probe (Host: gayatrieducation.tech) ==="
    curl -I -s -H "Host: gayatrieducation.tech" http://127.0.0.1/ | head -n 5

    echo "=== Existing Ecosystem Health Probes ==="
    echo -n "DBERT Main Website (3001): " && curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3001/
    echo -n "DBERT LMS Portal (5001):   " && curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5001/
    echo -n "DBERT REST API (8000):     " && curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/docs
    """
    ok, out, err = run_ssh_command(check_script, "Post-Deployment Health Probe")
    print(out)

    log("=" * 70)
    log("✓ GAYATRI AI PLATFORM SUCCESSFULLY DEPLOYED TO AWS EC2!")
    log("=" * 70)
    log("Next Action: Point gayatrieducation.tech DNS A-Record to: 3.26.237.171")
    log("SSL Provisioning Command (Run after DNS propagation):")
    log("  ssh -i <key> ubuntu@3.26.237.171 'sudo certbot --nginx -d gayatrieducation.tech -d www.gayatrieducation.tech'")
    log("=" * 70)

if __name__ == "__main__":
    main()
