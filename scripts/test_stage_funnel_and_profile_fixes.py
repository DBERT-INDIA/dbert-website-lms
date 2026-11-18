import subprocess
import json

PEM_PATH = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

REMOTE_TEST_CODE = """
import sys
import json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db

app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False
client = app.test_client()

test_email = "test_funnel_applicant_99@dbert.test"
test_phone = "9876543299"
csrf_val = "test_csrf_token_99"

with get_db() as conn:
    conn.execute("DELETE FROM user_sessions WHERE LOWER(email)=?", (test_email,))
    conn.execute("UPDATE intern_accounts SET application_id=NULL WHERE LOWER(email)=?", (test_email,))
    conn.execute("DELETE FROM intern_accounts WHERE LOWER(email)=?", (test_email,))
    conn.execute("DELETE FROM applications WHERE LOWER(email)=?", (test_email,))
    conn.commit()

# Establish session with CSRF token
with client.session_transaction() as sess:
    sess["_csrf"] = csrf_val

print("--- Test 1: Stage 1 Signup with domain slug & target internship lead ---")
stage1_payload = {
    "name": "Funnel Test Candidate",
    "email": test_email,
    "phone": test_phone,
    "password": "SecurePassword123!",
    "terms_accepted": True,
    "domain": "python-automation",
    "next": "/internships/python-automation-api-intern-at-zoho-pyt-220?apply=1",
    "visitor_id": "test_vis_99",
    "company_website": "",
    "_ts": "valid",
    "_csrf": csrf_val
}

headers = {"X-CSRF-Token": csrf_val}
r1 = client.post("/signup/stage1", json=stage1_payload, headers=headers)
print(f"Stage 1 Status Code: {r1.status_code}")
d1 = r1.get_json()
print(f"Stage 1 Response: {d1}")

assert r1.status_code == 200, f"Expected 200, got {r1.status_code}: {d1}"
assert d1.get("stage") == 1, f"Expected stage 1, got {d1.get('stage')}"
assert d1.get("next") == 2, f"Expected next 2, got {d1.get('next')}"
assert "redirect" not in d1, f"Did NOT expect redirect at stage 1! Got: {d1.get('redirect')}"

with get_db() as conn:
    app_row = conn.execute("SELECT * FROM applications WHERE LOWER(email)=?", (test_email,)).fetchone()
    assert app_row is not None, "Application row was not created!"
    assert app_row["domain"] == "Python Automation", f"Expected domain 'Python Automation', got '{app_row['domain']}'"
    assert app_row["college"] == "Pending Profile", f"Expected 'Pending Profile', got '{app_row['college']}'"
    assert app_row["status"] == "Apply Pending", f"Expected 'Apply Pending', got '{app_row['status']}'"
    
    sess_row = conn.execute("SELECT * FROM user_sessions WHERE LOWER(email)=?", (test_email,)).fetchone()
    assert sess_row is not None, "Session row was not created!"
    assert sess_row["next_url"] == "/internships/python-automation-api-intern-at-zoho-pyt-220?apply=1", f"Wrong next_url: {sess_row['next_url']}"
    print("SUCCESS: Stage 1 database state verified perfectly!")

print("\\n--- Test 2: Check /intern/me before Stage 2 (needs_academic_profile) ---")
r_me1 = client.get("/intern/me")
d_me1 = r_me1.get_json()
assert d_me1["intern"]["needs_academic_profile"] == True, f"Expected needs_academic_profile=True, got {d_me1['intern']['needs_academic_profile']}"
print(f"SUCCESS: /intern/me correctly flagged needs_academic_profile={d_me1['intern']['needs_academic_profile']}")

print("\\n--- Test 3: Stage 2 Academics Submission ---")
stage2_payload = {
    "city": "Bengaluru",
    "college": "BMS College of Engineering",
    "course": "B.Tech",
    "semester": "6th Semester",
    "year_of_passing": "2026",
    "domain": "Python Automation",
    "_csrf": csrf_val
}
r2 = client.post("/signup/stage2", json=stage2_payload, headers=headers)
print(f"Stage 2 Status Code: {r2.status_code}")
d2 = r2.get_json()
print(f"Stage 2 Response: {d2}")

assert r2.status_code == 200, f"Expected 200, got {r2.status_code}: {d2}"
assert d2.get("stage") == 2, f"Expected stage 2, got {d2.get('stage')}"
assert d2.get("redirect") == "/internships/python-automation-api-intern-at-zoho-pyt-220?apply=1", f"Expected redirect to lead URL, got {d2.get('redirect')}"

with get_db() as conn:
    app_row2 = conn.execute("SELECT * FROM applications WHERE LOWER(email)=?", (test_email,)).fetchone()
    assert app_row2["college"] == "BMS College of Engineering", f"Expected BMS College, got '{app_row2['college']}'"
    assert app_row2["status"] == "Under Review", f"Expected 'Under Review', got '{app_row2['status']}'"
    
    acct_row = conn.execute("SELECT * FROM intern_accounts WHERE LOWER(email)=?", (test_email,)).fetchone()
    assert acct_row["college"] == "BMS College of Engineering", f"Expected BMS College in intern_accounts, got '{acct_row['college']}'"
    assert acct_row["signup_stage"] == 2, f"Expected signup_stage 2, got {acct_row['signup_stage']}"
    print("SUCCESS: Stage 2 database state verified perfectly! College saved and status promoted to 'Under Review'!")

print("\\n--- Test 4: Check /intern/me after Stage 2 (needs_academic_profile) ---")
r_me2 = client.get("/intern/me")
d_me2 = r_me2.get_json()
assert d_me2["intern"]["needs_academic_profile"] == False, f"Expected needs_academic_profile=False, got {d_me2['intern']['needs_academic_profile']}"
print(f"SUCCESS: /intern/me correctly cleared needs_academic_profile={d_me2['intern']['needs_academic_profile']}")

# Cleanup
with get_db() as conn:
    conn.execute("DELETE FROM user_sessions WHERE LOWER(email)=?", (test_email,))
    conn.execute("UPDATE intern_accounts SET application_id=NULL WHERE LOWER(email)=?", (test_email,))
    conn.execute("DELETE FROM intern_accounts WHERE LOWER(email)=?", (test_email,))
    conn.execute("DELETE FROM applications WHERE LOWER(email)=?", (test_email,))
    conn.commit()
print("\\n=== ALL 4 AUTOMATED VERIFICATION TESTS PASSED (100%) ===")
"""

p = subprocess.Popen(
    ["ssh", "-i", PEM_PATH, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
out, err = p.communicate(input=REMOTE_TEST_CODE)
print(out)
if err:
    print("ERR:", err)
