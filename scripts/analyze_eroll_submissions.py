import subprocess
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = """
import json, re, glob
from collections import Counter

# 1. Read balance_enrollments_1500.json
json_path = "/var/www/dbert-website-lms/data/balance_enrollments_1500.json"
submissions = []
try:
    with open(json_path, "r", encoding="utf-8") as f:
        submissions = json.load(f)
except Exception as e:
    print(f"Error reading JSON: {e}")

print("="*75)
print("  OFFICIAL BALANCE ENROLLMENTS (1500 PORTAL) DATABASE AUDIT")
print("="*75)
print(f"Total Submissions in Database: {len(submissions)}")

real_candidates = []
test_submissions = []

for s in submissions:
    is_test = False
    if "python-requests" in str(s.get("userAgent", "")):
        is_test = True
    if is_test:
        test_submissions.append(s)
    else:
        real_candidates.append(s)

print(f"\\n1. Real Candidate Submissions: {len(real_candidates)}")
for idx, r in enumerate(real_candidates, 1):
    print(f"\\n  Candidate #{idx}:")
    print(f"    Submission ID:   {r.get('id')}")
    print(f"    Full Name:       {r.get('fullName')}")
    print(f"    Email:           {r.get('email')}")
    print(f"    Phone:           {r.get('phone')}")
    print(f"    Domain Track:    {r.get('domain')}")
    print(f"    Certificate ID:  {r.get('certId') or 'N/A'}")
    print(f"    UTR Number:      {r.get('utrNumber')}")
    print(f"    Amount Paid:     INR {r.get('amountPaid')}")
    print(f"    Submitted At:    {r.get('submittedAt')}")
    print(f"    IP Address:      {r.get('ipAddress')}")
    print(f"    User-Agent:      {r.get('userAgent')}")
    print(f"    Status:          {r.get('status')}")

print(f"\\n2. Verification Test Records: {len(test_submissions)}")
for t in test_submissions:
    print(f"  - [{t.get('id')}] {t.get('fullName')} ({t.get('email')}) | UTR: {t.get('utrNumber')} | Status: {t.get('status')}")

# 2. Audit Nginx access logs for traffic to /eroll, /enroll, and /enroll/1999
print("\\n" + "="*75)
print("  TRAFFIC & VISITOR ANALYSIS FOR /eroll AND /enroll")
print("="*75)

log_pattern = re.compile(r'(\\d+\\.\\d+\\.\\d+\\.\\d+) - - \\[([^\\]]+)\\] "(GET|POST) (/(?:enroll|eroll)[^ ]*) HTTP/[0-9.]+" (\\d+) \\d+ "([^"]*)" "([^"]*)"')

hits = []
for f in glob.glob("/var/log/nginx/access.log*"):
    try:
        with open(f, "r", errors="ignore") as log:
            for line in log:
                m = log_pattern.search(line)
                if m:
                    hits.append(m.groups())
    except:
        pass

print(f"Total Raw HTTP Requests to /eroll or /enroll routes: {len(hits)}")

paths = Counter(h[3].split("?")[0] for h in hits)
print("Route Breakdown:")
for p, count in paths.most_common():
    print(f"  {p}: {count} requests")

# Non-bot visitors
unique_ips = Counter()
non_bot_hits = []
for h in hits:
    ip, ts, method, path, status, ref, ua = h
    if "python-requests" not in ua and "DBERT-Verification-Bot" not in ua:
        unique_ips[ip] += 1
        non_bot_hits.append(h)

print(f"\\nDistinct Real User IPs Visiting the Portal: {len(unique_ips)}")
for ip, count in unique_ips.most_common(20):
    print(f"  IP {ip}: {count} hits")

print(f"\\nDetailed Log of Real User Interactions ({len(non_bot_hits)}):")
for h in non_bot_hits:
    ip, ts, method, path, status, ref, ua = h
    ua_short = "Mobile/Android" if "Android" in ua else ("iPhone/iOS" if "iPhone" in ua else "Desktop/Windows/Mac")
    print(f"  [{ts}] {ip} | {method} {path} ({status}) | Ref: {ref[:45]} | Device: {ua_short}")
"""

b64 = base64.b64encode(remote_script.encode("utf-8")).decode("utf-8")
ssh_cmd = [
    "ssh",
    "-i", PEM_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "BatchMode=yes",
    REMOTE_HOST,
    f"python3 -c \"import base64; exec(base64.b64decode('{b64}').decode())\""
]

res = subprocess.run(ssh_cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
