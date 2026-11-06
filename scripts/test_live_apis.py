import subprocess
import json

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
server = "ubuntu@3.26.237.171"

# 1. Test Next.js API on 3001
res1 = subprocess.run([
    "ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    server, "curl -s 'http://127.0.0.1:3001/api/verify?certid=CERT-DBERT-2026-DA-001'"
], capture_output=True)
out1 = res1.stdout.decode("utf-8", errors="ignore")
print("1. Next.js API (port 3001):")
try:
    print(json.dumps(json.loads(out1), indent=2))
except Exception as e:
    print("Raw output:", out1)

# 2. Test LMS Flask API on 5001
res2 = subprocess.run([
    "ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    server, "curl -s 'http://127.0.0.1:5001/api/verify?certId=CERT-DBERT-2026-DA-001'"
], capture_output=True)
out2 = res2.stdout.decode("utf-8", errors="ignore")
print("\n2. LMS Flask API (port 5001):")
try:
    print(json.dumps(json.loads(out2), indent=2))
except Exception as e:
    print("Raw output:", out2)

# 3. Test Public Website through Cloudflare/Nginx: https://dbert.in/api/verify?certid=CERT-DBERT-2026-DA-001
import urllib.request
try:
    req = urllib.request.Request(
        "https://dbert.in/api/verify?certid=CERT-DBERT-2026-DA-001",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        public_data = json.loads(resp.read().decode("utf-8"))
        print("\n3. Public API (https://dbert.in/api/verify?certid=...):")
        print(json.dumps(public_data, indent=2))
except Exception as e:
    print("\n3. Public API error:", e)
