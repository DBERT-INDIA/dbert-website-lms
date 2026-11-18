#!/usr/bin/env python3
"""
scripts/local_ops_dashboard_server.py

Local Operations Server providing real-time auto-updating synchronization with:
1. EC2 PostgreSQL (task_submissions, intern_articles, intern_accounts, intern_certificates)
2. Google Sheets (gid=1265293201 for ₹299 payments)
3. Local dispatch tracking (discrepancy_roadmap_tracking.json)
4. Local decision recorder (data/dashboard_decisions.json)

Serves:
- http://127.0.0.1:8050/ -> Interactive Generative UI Dashboard
- http://127.0.0.1:8050/api/live_state -> Live JSON state for real-time frontend re-rendering
- http://127.0.0.1:8050/api/save_decision -> Endpoint to record manual review decisions locally
"""

import os
import sys
import json
import time
import threading
import subprocess
import urllib.request
import csv
import io
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
ARTIFACT_DIR = Path(r"C:\Users\user\.gemini\antigravity\brain\db340522-3de4-46ab-8736-005fb1623326")
DECISIONS_FILE = DATA_DIR / "dashboard_decisions.json"
LIVE_STATE_FILE = DATA_DIR / "live_ops_state.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# Shared memory cache for instant responses
GLOBAL_STATE = {
    "last_sync": None,
    "ec2_healthy": False,
    "kpis": {
        "sheet_submissions": 87,
        "sheet_verified": 81,
        "sheet_actionable": 5,
        "stipend_submissions": 19,
        "published_articles": 26,
        "total_interns": 2865,
        "total_emails_sent": 510,
        "discrepancy_emails": 10,
        "roadmap_emails": 500
    },
    "sheet_action_candidates": [],
    "stipend_submissions": [],
    "cohort_d": [],
    "decisions": {}
}

if DECISIONS_FILE.exists():
    try:
        GLOBAL_STATE["decisions"] = json.load(open(DECISIONS_FILE, encoding="utf-8"))
    except Exception:
        GLOBAL_STATE["decisions"] = {}

def sync_live_data():
    """Background sync routine polling EC2 and Google Sheet every 25 seconds."""
    while True:
        try:
            # 0. Reload decisions from disk
            if DECISIONS_FILE.exists():
                try:
                    GLOBAL_STATE["decisions"] = json.load(open(DECISIONS_FILE, encoding="utf-8"))
                except Exception:
                    pass

            # 1. Read dispatch tracking
            tracking_file = DATA_DIR / "discrepancy_roadmap_tracking.json"
            if tracking_file.exists():
                tr = json.load(open(tracking_file, encoding="utf-8"))
                GLOBAL_STATE["kpis"]["total_emails_sent"] = len(tr)
                GLOBAL_STATE["kpis"]["discrepancy_emails"] = sum(1 for v in tr.values() if v.get("type") == "DISCREPANCY")
                GLOBAL_STATE["kpis"]["roadmap_emails"] = sum(1 for v in tr.values() if v.get("type") == "ROADMAP")

            # 2. Poll Google Sheet 299 Payments
            sheet_url = 'https://docs.google.com/spreadsheets/d/1yacGLZGiTD_8GLOUHMphbdfsORqc8u_DrjvpVRSEDgs/export?format=csv&gid=1265293201'
            req = urllib.request.Request(sheet_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('utf-8')
                rows = list(csv.reader(io.StringIO(content)))
                
            reg_file = ROOT_DIR / "apps" / "website" / "src" / "data" / "certificates_registry.json"
            local_reg = json.load(open(reg_file, encoding="utf-8")) if reg_file.exists() else {}
            
            verified_emails = set(
                c.get("email", "").strip().lower() 
                for c in local_reg.values() 
                if (c.get("verified") is True or c.get("status") == "VERIFIED") and not c.get("isProvisional", False)
            )

            action_candidates = []
            for idx, r in enumerate(rows[1:], start=2):
                email = r[1].strip().lower() if len(r) > 1 else ''
                domain = r[3].strip() if len(r) > 3 else ''
                batch = r[2].strip() if len(r) > 2 else ''
                name = r[5].strip() if len(r) > 5 else ''
                proof = r[9].strip() if len(r) > 9 else ''
                
                if email and email not in verified_emails:
                    action_candidates.append({
                        "row": idx,
                        "timestamp": r[0],
                        "email": email,
                        "name": name,
                        "domain": domain,
                        "batch": batch,
                        "proof_url": proof,
                        "is_provisional": any(c.get("email", "").strip().lower() == email for c in local_reg.values())
                    })

            GLOBAL_STATE["sheet_action_candidates"] = action_candidates
            GLOBAL_STATE["kpis"]["sheet_submissions"] = len(rows) - 1
            GLOBAL_STATE["kpis"]["sheet_actionable"] = len(action_candidates)
            GLOBAL_STATE["kpis"]["sheet_verified"] = (len(rows) - 1) - len(action_candidates)

            # 3. Query EC2 PostgreSQL for Task Submissions & Articles
            remote_py = """
import sys, json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db
conn = get_db()
c = conn.cursor()

c.execute(\"\"\"
    SELECT ts.id, ts.intern_id, ts.email, ts.github_repo_url, ts.live_demo_url, ts.status,
           ts.created_at, ts.ai_evaluation_score, ts.ai_evaluation_notes,
           ia.name, ia.domain, ia.upi_id_encrypted, ia.linkedin_url, ia.linkedin_verified,
           ia.stipend_verified, ia.stipend_release_date
    FROM task_submissions ts
    JOIN intern_accounts ia ON ts.intern_id = ia.id
    WHERE ts.task_category = 'stipend_milestone'
    ORDER BY ts.id DESC
\"\"\")
subs = []
for r in c.fetchall():
    subs.append({
        'sub_id': r[0],
        'intern_id': r[1],
        'email': r[2],
        'github_repo_url': r[3],
        'live_demo_url': r[4],
        'sub_status': r[5],
        'created_at': str(r[6]),
        'ai_score': r[7],
        'ai_notes': r[8],
        'name': r[9],
        'domain': r[10],
        'has_upi': bool(r[11]),
        'linkedin_url': r[12],
        'linkedin_verified': bool(r[13]),
        'stipend_verified': bool(r[14]),
        'stipend_release_date': str(r[15])
    })

c.execute("SELECT status, count(*) FROM intern_articles GROUP BY status")
art_stats = dict(c.fetchall())

c.execute("SELECT count(*) FROM intern_accounts")
tot_interns = c.fetchone()[0]

print(json.dumps({
    'subs': subs,
    'published_articles': art_stats.get('PUBLISHED', 0),
    'pending_articles': art_stats.get('PENDING_REVIEW', 0),
    'total_interns': tot_interns
}))
"""
            cmd = [
                "ssh",
                "-i", r"C:\Users\user\.ssh\dbert-production-server.pem",
                "-o", "StrictHostKeyChecking=no",
                "ubuntu@3.26.237.171",
                "/var/www/dbert-website-lms/apps/portal/.venv/bin/python",
                "-"
            ]
            res = subprocess.run(cmd, input=remote_py, capture_output=True, text=True, timeout=25)
            if res.returncode == 0:
                ec2_data = json.loads(res.stdout)
                GLOBAL_STATE["stipend_submissions"] = ec2_data.get("subs", [])
                GLOBAL_STATE["kpis"]["stipend_submissions"] = len(ec2_data.get("subs", []))
                GLOBAL_STATE["kpis"]["published_articles"] = ec2_data.get("published_articles", 26)
                GLOBAL_STATE["kpis"]["total_interns"] = ec2_data.get("total_interns", 2865)
                GLOBAL_STATE["ec2_healthy"] = True
            
            GLOBAL_STATE["last_sync"] = time.strftime("%Y-%m-%d %H:%M:%S")

            # Persist local snapshot
            with open(LIVE_STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(GLOBAL_STATE, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"[SYNC-ERROR] {e}")

        time.sleep(25)

class OpsHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == "/api/live_state":
            self._set_headers("application/json")
            self.wfile.write(json.dumps(GLOBAL_STATE).encode("utf-8"))
        elif self.path in ["/", "/dashboard", "/dashboard.html"]:
            self._set_headers("text/html; charset=utf-8")
            html_file = ARTIFACT_DIR / "dashboard.html"
            if html_file.exists():
                self.wfile.write(open(html_file, "rb").read())
            else:
                self.wfile.write(b"<h1>Dashboard loading... please refresh in 5 seconds.</h1>")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/save_decision":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode("utf-8"))
                key = payload.get("key")
                if key:
                    GLOBAL_STATE["decisions"][key] = {
                        "action": payload.get("action"),
                        "notes": payload.get("notes", ""),
                        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    with open(DECISIONS_FILE, "w", encoding="utf-8") as f:
                        json.dump(GLOBAL_STATE["decisions"], f, indent=2, ensure_ascii=False)
                self._set_headers("application/json")
                self.wfile.write(json.dumps({"status": "success", "recorded": GLOBAL_STATE["decisions"]}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

def main():
    print("=" * 80)
    print("DBERT REAL-TIME OPS & GATE DECISION LOCAL SERVER")
    print("Serving at: http://127.0.0.1:8050")
    print("=" * 80)

    # Start background synchronization worker
    t = threading.Thread(target=sync_live_data, daemon=True)
    t.start()

    server = HTTPServer(("127.0.0.1", 8050), OpsHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()

if __name__ == "__main__":
    main()
