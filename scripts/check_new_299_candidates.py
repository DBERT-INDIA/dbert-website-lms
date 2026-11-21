import subprocess
import json
import os

with open("apps/website/src/data/certificates_registry.json", "r", encoding="utf-8") as f:
    certs = json.load(f)

with open("apps/website/src/data/directory_candidates.json", "r", encoding="utf-8") as f:
    directory = json.load(f)

dir_map = {d.get("certId"): d for d in directory}

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

# Fetch remote submissions from EC2
res = subprocess.run(
    ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "cat /var/www/dbert-website-lms/data/verification_submissions_299.json"],
    capture_output=True,
    text=True
)

if res.returncode != 0:
    print("Failed to fetch from EC2:", res.stderr)
    exit(1)

subs = json.loads(res.stdout)
print(f"Total Submissions on EC2: {len(subs)}")
print("=" * 100)

# Check all submissions from index 18 onwards (Row 19 to 25) and also check status of all 25
for idx, s in enumerate(subs, 1):
    cid = s.get("certId")
    name = s.get("fullName")
    email = s.get("email")
    phone = s.get("phone")
    utr = s.get("utrNumber")
    st = s.get("status")
    sub_at = s.get("submittedAt")

    c = certs.get(cid, {})
    d = dir_map.get(cid, {})

    c_status = c.get("status")
    c_prov = c.get("isProvisional")
    c_score = c.get("score")
    d_ver = d.get("verified")
    d_status = d.get("status")

    is_new = idx >= 19
    tag = ">>> NEW <<<" if is_new else "    OLD    "

    print(f"[{tag}] #{idx:2d} | {cid} | {name} | {email}")
    print(f"       UTR: {utr} | Status in JSON: {st} | SubmittedAt: {sub_at}")
    print(f"       Registry: status={c_status}, isProvisional={c_prov}, score={c_score}")
    print(f"       Directory: in_dir={bool(d)}, verified={d_ver}, status={d_status}")
    print("-" * 100)
