import subprocess
import sys

PEM_PATH = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

REMOTE_SCRIPT = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, create_session, AUTH_COOKIE
import subprocess

print("===========================================================================")
print("DBERT Screenshot & UTR Digital Voucher Engine Verification")
print("===========================================================================")

# Generate admin session token
token = create_session('dbert_admin@dbert.test', 'admin')

# 1. Test Bhargavi Poola's UTR receipt via curl through Nginx
print("\\n[TEST 1] Testing /admin/screenshot/utr_666501928441.receipt through Nginx:")
cmd = f"curl -s -i -H 'Cookie: {AUTH_COOKIE}={token}' -k https://127.0.0.1/admin/screenshot/utr_666501928441.receipt -H 'Host: lms.dbert.in'"
res = subprocess.getoutput(cmd)

lines = res.splitlines()
status_line = lines[0] if lines else ""
print(f"  Status Line: {status_line}")

header_lines = [l for l in lines if ': ' in l]
headers = {}
for h in header_lines:
    k, v = h.split(': ', 1)
    k_lower = k.lower().strip()
    if k_lower in headers:
        headers[k_lower].append(v.strip())
    else:
        headers[k_lower] = [v.strip()]

print(f"  Content-Type: {headers.get('content-type')}")
print(f"  Content-Disposition: {headers.get('content-disposition')}")
print(f"  X-Frame-Options: {headers.get('x-frame-options')}")
print(f"  X-Content-Type-Options: {headers.get('x-content-type-options')}")

# Check duplicate headers
assert len(headers.get('x-frame-options', [])) == 1, f"Duplicate X-Frame-Options: {headers.get('x-frame-options')}"
assert headers.get('x-frame-options')[0] == "SAMEORIGIN", f"Expected SAMEORIGIN, got {headers.get('x-frame-options')}"
assert "200" in status_line, f"Expected HTTP 200, got {status_line}"
assert "image/svg+xml" in headers.get('content-type', [''])[0], f"Expected image/svg+xml, got {headers.get('content-type')}"

# Check body content
body = res[res.find('\\r\\n\\r\\n') + 4:] if '\\r\\n\\r\\n' in res else res[res.find('\\n\\n') + 2:]
assert "Bhargavi Poola" in body, "Candidate name 'Bhargavi Poola' missing from SVG voucher!"
assert "666501928441" in body, "UTR '666501928441' missing from SVG voucher!"
assert "Data Analyst" in body, "Domain 'Data Analyst' missing from SVG voucher!"
print("  ✓ SVG Vector Voucher generated successfully with 100% data fidelity!")

# 2. Test Missing Physical File Fallback
print("\\n[TEST 2] Testing Missing File Fallback (/admin/screenshot/non_existent_12345.png):")
cmd2 = f"curl -s -i -H 'Cookie: {AUTH_COOKIE}={token}' -k https://127.0.0.1/admin/screenshot/non_existent_12345.png -H 'Host: lms.dbert.in'"
res2 = subprocess.getoutput(cmd2)
lines2 = res2.splitlines()
status_line2 = lines2[0] if lines2 else ""
print(f"  Status Line: {status_line2}")
assert "404" in status_line2, f"Expected HTTP 404, got {status_line2}"
assert "Proof Asset Not Found On Disk" in res2, "Expected styled SVG missing asset fallback!"
print("  ✓ Missing physical file returned graceful vector SVG (no ERR_INVALID_RESPONSE)!")

# 3. Test Unauthenticated Browser Navigation
print("\\n[TEST 3] Testing Unauthenticated Direct Navigation (no cookie, Accept: text/html):")
cmd3 = "curl -s -i -H 'Accept: text/html' -k https://127.0.0.1/admin/screenshot/utr_666501928441.receipt -H 'Host: lms.dbert.in'"
res3 = subprocess.getoutput(cmd3)
lines3 = res3.splitlines()
status_line3 = lines3[0] if lines3 else ""
print(f"  Status Line: {status_line3}")
assert "302" in status_line3 or "401" in status_line3, f"Expected 302 or 401, got {status_line3}"
if "302" in status_line3:
    print(f"  Redirect Location: {[l for l in lines3 if 'location:' in l.lower()]}")
    print("  ✓ Unauthenticated browser redirect to /signin verified!")

print("\\n===========================================================================")
print("ALL SCREENSHOT & VOUCHER TESTS PASSED! (100% SUCCESS)")
print("===========================================================================")
"""

p = subprocess.Popen(
    ["ssh", "-i", PEM_PATH, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
stdout, stderr = p.communicate(input=REMOTE_SCRIPT)
print(stdout)
if stderr:
    print("STDERR:", stderr)

if "ALL SCREENSHOT & VOUCHER TESTS PASSED!" not in stdout:
    sys.exit(1)
