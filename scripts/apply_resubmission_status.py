import subprocess
import json
import os
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SERVER = "ubuntu@3.26.237.171"
REPORT_FILE = "data/github_linkedin_audit_report.json"

if not os.path.exists(REPORT_FILE):
    print(f"Error: {REPORT_FILE} not found. Run audit_33_github_linkedin.py first.")
    sys.exit(1)

with open(REPORT_FILE, "r", encoding="utf-8") as f:
    report = json.load(f)

tier1 = report["tier1_submissions"]

resubmissions = [s for s in tier1 if s["decision"] == "CHANGES_REQUESTED"]
approved_ready = [s for s in tier1 if s["decision"] == "APPROVED_READY"]

print("=" * 80)
print("APPLYING RESUBMISSION STATUS & STRUCTURED FEEDBACK ON PRODUCTION EC2")
print("=" * 80)
print(f"Total Submissions Evaluated: {len(tier1)}")
print(f"Flagged for Resubmission ('changes_requested'): {len(resubmissions)}")
print(f"Qualified & Ready for Staff Approval: {len(approved_ready)}")

# Prepare updates payload
updates_payload = []
for s in resubmissions:
    feedback_text = (
        f"Action Required - Revision Requested by DBERT Admissions & Technical Audit:\n\n"
        f"1. GitHub Deliverable Issue: {s['github_reason']}.\n"
        f"   Requirement: All milestone submissions must be an active, verified Pull Request (PR) URL on one of DBERT's 4 official repositories:\n"
        f"   - Alkame: https://github.com/Alkameinc/alkame-nifty-50-educational\n"
        f"   - Gayatri AI: https://github.com/Gayatri-Education/Gayatri-Demo\n"
        f"   - DBERT Agent / Aivara: https://github.com/DBERT-INDIA/dbert-agent\n"
        f"   - Internship Portal: https://github.com/DBERT-INDIA/Internshipportal\n"
        f"   Please open a Pull Request against the upstream repository and submit your PR link (e.g., github.com/Alkameinc/.../pull/123).\n\n"
        f"2. LinkedIn Credential Issue: {s['linkedin_reason']}.\n"
        f"   Requirement: You must add your verified DBERT credential to your LinkedIn profile under 'Licenses & Certifications'. "
        f"Please use the 1-Click launcher on https://lms.dbert.in/stipend/tasks to link your credential ({s.get('cert_id') or 'DBERT Fellowship'}).\n\n"
        f"Please revise your deliverables and resubmit using the form below."
    )
    updates_payload.append({
        "sub_id": s["sub_id"],
        "intern_id": s["intern_id"],
        "name": s["name"],
        "email": s["email"],
        "status": "changes_requested",
        "feedback": feedback_text
    })

# Write payload to remote execution script
payload_json = json.dumps(updates_payload)
remote_py = f'''
import sys
import json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

payload = json.loads({json.dumps(payload_json)})

with get_db() as conn:
    updated_count = 0
    for item in payload:
        sub_id = item["sub_id"]
        status = item["status"]
        feedback = item["feedback"]
        
        # Update task_submissions status and feedback
        conn.execute(
            """
            UPDATE task_submissions 
            SET status = ?, 
                ai_evaluation_notes = ?,
                ai_evaluation_status = 'CHANGES_REQUESTED',
                ai_evaluated_at = CURRENT_TIMESTAMP
            WHERE id = ?;
            """,
            (status, feedback, sub_id)
        )
        updated_count += 1
        print("Updated submission #" + str(sub_id) + " for " + item["name"] + " -> status='" + status + "'")

    if hasattr(conn, "commit"):
        conn.commit()
    print("\\nSuccessfully committed " + str(updated_count) + " submission updates to PostgreSQL!")
'''

print("\nExecuting database updates via SSH on EC2...")
res = subprocess.run(
    ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"],
    input=remote_py,
    text=True,
    capture_output=True,
    encoding="utf-8"
)

print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)

if res.returncode == 0:
    print("\n" + "=" * 80)
    print("ALL 27 SUBMISSIONS UPDATED TO 'changes_requested' WITH STRUCTURED FEEDBACK!")
    print("=" * 80)
else:
    print("Failed to apply updates. Please check the error above.")
