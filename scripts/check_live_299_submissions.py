import subprocess
import json

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

res = subprocess.run(
    ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "cat /var/www/dbert-website-lms/data/verification_submissions_299.json"],
    capture_output=True,
    text=True
)

if res.returncode == 0:
    try:
        data = json.loads(res.stdout)
        print(f"Total submissions on EC2: {len(data)}")
        for idx, s in enumerate(data, 1):
            fn = s.get("fullName")
            em = s.get("email")
            cid = s.get("certId")
            st = s.get("status")
            utr = s.get("utrNumber")
            sub_at = s.get("submittedAt")
            print(f"{idx:2d}. {fn} ({em}) | Cert: {cid} | Status: {st} | UTR: {utr} | At: {sub_at}")
    except Exception as e:
        print("JSON parse error:", e)
else:
    print("SSH error:", res.stderr)
