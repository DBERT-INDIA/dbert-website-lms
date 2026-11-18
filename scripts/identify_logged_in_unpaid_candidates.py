import os
import sys
import json
from datetime import datetime

# Script to run locally or query EC2
import subprocess

def main():
    print("=== IDENTIFYING CANDIDATES LOGGED IN AFTER RECEIVING TODAY'S EMAIL ===")
    
    # 1. Load today's sent emails from dispatch_tracking_urgent_kickoff.json
    tracking_file = 'data/dispatch_tracking_urgent_kickoff.json'
    if not os.path.exists(tracking_file):
        print(f"File {tracking_file} does not exist.")
        return

    with open(tracking_file, 'r', encoding='utf-8') as f:
        sent_records = json.load(f)

    # Filter to SENT
    sent_dict = {}
    for r in sent_records:
        if r.get('status') == 'SENT':
            em = r['email'].strip().lower()
            sent_dict[em] = {
                "name": r.get('name', ''),
                "domain": r.get('domain', ''),
                "sent_timestamp": r.get('timestamp', ''),
                "account_sender": r.get('account', '')
            }

    print(f"Total candidates sent today's email: {len(sent_dict)}")

    # 2. Query EC2 PostgreSQL for all user_sessions and attendance today
    ssh_cmd = [
        "ssh", "-i", r"C:\Users\user\.ssh\dbert-production-server.pem",
        "-o", "StrictHostKeyChecking=no",
        "ubuntu@3.26.237.171",
        "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 - << 'EOF'\n"
        "import sys, json\n"
        "sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')\n"
        "from dotenv import load_dotenv\n"
        "load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')\n"
        "from services.database.adapter import get_db_adapter\n"
        "\n"
        "with get_db_adapter() as conn:\n"
        "    sessions = conn.execute(\"\"\"\n"
        "        SELECT id, email, created_at, role\n"
        "        FROM user_sessions\n"
        "        WHERE created_at >= '2026-11-16 00:00:00'\n"
        "        ORDER BY created_at ASC\n"
        "    \"\"\").fetchall()\n"
        "    sess_list = [dict(s) for s in sessions]\n"
        "\n"
        "    # Check attendance\n"
        "    att = conn.execute(\"SELECT email, updated_at FROM attendance WHERE updated_at >= '2026-11-16 06:50:00'\").fetchall()\n"
        "    att_list = [dict(a) for a in att]\n"
        "\n"
        "    # Check check_log\n"
        "    cl = conn.execute(\"SELECT email, timestamp FROM check_log WHERE timestamp >= '2026-11-16 06:50:00'\").fetchall()\n"
        "    cl_list = [dict(c) for c in cl]\n"
        "\n"
        "    # Get phone numbers from applications\n"
        "    apps = conn.execute(\"SELECT email, phone, name, domain, status FROM applications\").fetchall()\n"
        "    app_map = {}\n"
        "    for a in apps:\n"
        "        em = (a['email'] or '').strip().lower()\n"
        "        if em:\n"
        "            app_map[em] = dict(a)\n"
        "\n"
        "    # Check enrollments for paid status\n"
        "    enrs = conn.execute(\"SELECT email, payment_status, utr FROM enrollments\").fetchall()\n"
        "    enr_map = {}\n"
        "    for e in enrs:\n"
        "        em = (e['email'] or '').strip().lower()\n"
        "        if em:\n"
        "            enr_map[em] = dict(e)\n"
        "\n"
        "    print(json.dumps({'sessions': sess_list, 'att': att_list, 'check_log': cl_list, 'apps': app_map, 'enrs': enr_map}, default=str))\n"
        "EOF\n"
    ]

    res = subprocess.run(ssh_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("SSH Error:", res.stderr)
        return

    data = json.loads(res.stdout)
    sessions = data['sessions']
    att = data.get('att', [])
    check_log = data.get('check_log', [])
    app_map = data['apps']
    enr_map = data['enrs']

    print(f"Total sessions on EC2 today: {len(sessions)}")
    print(f"Total attendance updates since 12:20 PM: {len(att)}")
    print(f"Total verification checks since 12:20 PM: {len(check_log)}")

    # Combine all user activities after 12:20 PM IST (06:50 UTC)
    activity_map = {} # email -> latest_ts
    for s in sessions:
        em = (s.get('email') or '').strip().lower()
        if em:
            ts = str(s['created_at'])
            if em not in activity_map or ts > activity_map[em]:
                activity_map[em] = ts

    for a in att:
        em = (a.get('email') or '').strip().lower()
        if em:
            ts = str(a['updated_at'])
            if em not in activity_map or ts > activity_map[em]:
                activity_map[em] = ts

    for c in check_log:
        em = (c.get('email') or '').strip().lower()
        if em:
            ts = str(c['timestamp'])
            if em not in activity_map or ts > activity_map[em]:
                activity_map[em] = ts

    matched_candidates = []
    seen_emails = set()

    for em, login_ts in activity_map.items():
        if em in seen_emails:
            continue
        if em in sent_dict:
            sent_info = sent_dict[em]
            sent_ts = sent_info['sent_timestamp']
            app_info = app_map.get(em, {})
            enr_info = enr_map.get(em, {})
            payment_status = enr_info.get('payment_status')
            is_paid = (payment_status == 'Accepted')

            # Filter to candidates who logged in / active after 06:50 UTC (12:20 IST)
            if '2026-11-16 06:50' <= login_ts or '2026-11-16 07:' in login_ts or '2026-11-16 08:' in login_ts:
                seen_emails.add(em)
                matched_candidates.append({
                    "email": em,
                    "name": app_info.get('name') or sent_info['name'],
                    "phone": app_info.get('phone', ''),
                    "domain": app_info.get('domain') or sent_info['domain'],
                    "sent_timestamp": sent_ts,
                    "login_timestamp": login_ts,
                    "account_sender": sent_info['account_sender'],
                    "app_status": app_info.get('status', ''),
                    "payment_status": payment_status,
                    "is_paid": is_paid
                })

    print(f"\nTotal Candidates who received email today AND logged in: {len(matched_candidates)}")
    unpaid = [c for c in matched_candidates if not c['is_paid']]
    print(f"Candidates who have NOT completed payment: {len(unpaid)}")
    
    print("\nDetailed list of candidates to reach out on WhatsApp:")
    for idx, c in enumerate(unpaid, 1):
        print(f"  #{idx}: {c['name']} | {c['email']} | Phone: {c['phone']} | Login: {c['login_timestamp']} | Sender: {c['account_sender']}")

    # Save to file
    out_file = 'data/whatsapp_followup_logged_in_unpaid.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(unpaid, f, indent=2)
    print(f"\nSaved candidates to {out_file}")

if __name__ == '__main__':
    main()
