#!/usr/bin/env python3
"""
scripts/test_persona_routes_on_ec2.py
Automated end-to-end route audit of all 8 seeded personas across their designated
lifecycle stages in accordance with AGENTS.md and GEMINI.md.
Executes on EC2 using Flask's test_client with authenticated session cookies.
"""
import subprocess
import sys

PEM_PATH = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

REMOTE_TEST_CODE = """
import sys
import os
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db, hash_password

client = app.test_client()

TEST_PERSONAS = [
    {
        "role": "Staff Reviewer",
        "email": "mentor_staff@dbert.test",
        "kind": "staff",
        "probes": [
            ("/staff/tasks", 200, "Staff Review Queue"),
            ("/admin/push-broadcast", 200, "Push Notification Broadcast"),
            ("/admin/ambassador-payouts", 200, "Ambassador Payouts")
        ]
    },
    {
        "role": "Super Admin",
        "email": "dbert_admin@dbert.test",
        "kind": "staff",
        "probes": [
            ("/admin", 200, "Admin Overview")
        ]
    },
    {
        "role": "Enrolled Fellow",
        "email": "fellow_enrolled@dbert.test",
        "kind": "intern",
        "probes": [
            ("/portal", 200, "Dashboard Overview"),
            ("/tasks", 200, "Tasks & Bounties"),
            ("/account/notifications", 200, "Notification Settings")
        ]
    },
    {
        "role": "Stipend Ready (Gates 1 & 2 Cleared)",
        "email": "stipend_ready@dbert.test",
        "kind": "intern",
        "probes": [
            ("/stipend/tasks", 200, "Stipend Technical Contribution")
        ]
    },
    {
        "role": "Withdrawable Wallet (5,000 Coins)",
        "email": "stipend_wallet@dbert.test",
        "kind": "intern",
        "probes": [
            ("/account/coins", 200, "Coin Ledger"),
            ("/ambassador", 200, "Ambassador Dashboard & Withdrawals"),
            ("/intern/ambassador/withdraw?format=json", 200, "Withdrawal JSON API")
        ]
    },
    {
        "role": "Gate 1 Locked (Provisional Fellow)",
        "email": "stipend_gate1_locked@dbert.test",
        "kind": "intern",
        "probes": [
            ("/stipend/tasks", 200, "Gate 1 Verification Gating")
        ]
    },
    {
        "role": "Stage 3 Selected Candidate",
        "email": "stage3_selected@dbert.test",
        "kind": "intern",
        "probes": [
            ("/portal", 200, "Candidate Selection Welcome Banner")
        ]
    },
    {
        "role": "Offer Letter Ready to Sign",
        "email": "offer_pending@dbert.test",
        "kind": "intern",
        "probes": [
            ("/portal/offer", 200, "Official Letter of Offer")
        ]
    }
]

print('=' * 75)
print('DBERT Personas & Lifecycle Routes Automated Verification')
print('=' * 75)

all_passed = True

with get_db() as conn:
    for p in TEST_PERSONAS:
        email = p['email']
        role_label = p['role']
        kind = p['kind']
        print(f'\\n[PERSONA] {role_label} ({email})')

        # Check account exists
        if kind == 'staff':
            row = conn.execute("SELECT id, name, email, role FROM staff_accounts WHERE email = ?", (email,)).fetchone()
            if not row:
                print(f'  ❌ Account not found in staff_accounts: {email}')
                all_passed = False
                continue
            role = row['role']
        else:
            row = conn.execute("SELECT id, name, email, domain FROM intern_accounts WHERE email = ?", (email,)).fetchone()
            if not row:
                print(f'  ❌ Account not found in intern_accounts: {email}')
                all_passed = False
                continue
            role = 'intern'

        # Mint authentic session token
        from app import create_session, AUTH_COOKIE
        token = create_session(email, role)
        client.set_cookie('dbert_auth', token)
        client.set_cookie('dbert_session', token)

        with client.session_transaction() as sess:
            sess['_csrf'] = 'test_csrf_token_12345'
            if kind == 'staff':
                sess['staff_id'] = row['id']
                sess['staff_email'] = row['email']
                sess['staff_name'] = row['name']
                sess['role'] = row['role']
                if row['role'] in ('admin', 'superadmin'):
                    sess['admin_id'] = row['id']
            else:
                sess['intern_user'] = {
                    'id': row['id'],
                    'name': row['name'],
                    'email': row['email'],
                    'domain': row['domain'],
                    'role': 'intern'
                }
                sess['user_id'] = row['id']
                sess['role'] = 'intern'

        # Execute probes
        for endpoint, expected_status, label in p['probes']:
            resp = client.get(endpoint, headers={'X-Session-Token': token})
            status_ok = (resp.status_code == expected_status)
            icon = '✓' if status_ok else '❌'
            print(f'  {icon} {label} ({endpoint}) -> HTTP {resp.status_code} (Expected {expected_status})')
            if not status_ok:
                all_passed = False

print('\\n' + '=' * 75)
if all_passed:
    print('ALL 8 PERSONAS & LIFECYCLE ROUTES VERIFIED SUCCESSFULLY! (100% PASS)')
else:
    print('SOME PROBES FAILED - INSPECT LOGS ABOVE')
print('=' * 75)
"""

def main():
    p = subprocess.Popen(
        ["ssh", "-i", PEM_PATH, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = p.communicate(input=REMOTE_TEST_CODE)
    print(stdout)
    if stderr:
        print("[STDERR]", stderr)
    if p.returncode != 0:
        sys.exit(p.returncode)

if __name__ == "__main__":
    main()
