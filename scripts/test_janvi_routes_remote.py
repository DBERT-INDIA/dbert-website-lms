import subprocess

remote_code = r"""
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, create_session

email = 'janvibamane61@gmail.com'
token = create_session(email, 'intern')
print('Created session token:', token[:8] + '...')

with app.test_client() as client:
    headers = {'X-Session-Token': token}
    
    # 1. Test /portal/offer
    resp = client.get('/portal/offer', headers=headers)
    print('GET /portal/offer status:', resp.status_code)
    html = resp.get_data(as_text=True)
    print('Contains "Download Official Signed PDF":', 'Download Official Signed PDF' in html)
    print('Contains "Reconciled":', 'Reconciled' in html)
    print('Contains "DBERT-OFR-2026-AIML-5180":', 'DBERT-OFR-2026-AIML-5180' in html)
    print('Contains "Janvi Bamane":', 'Janvi Bamane' in html)

    # 2. Test /portal/offer/print
    resp_print = client.get('/portal/offer/print', headers=headers)
    print('GET /portal/offer/print status:', resp_print.status_code)
    html_print = resp_print.get_data(as_text=True)
    print('Print page length:', len(html_print))
    print('Print contains Janvi Bamane:', 'Janvi Bamane' in html_print)
    print('Print contains Accepted & Digitally Signed:', 'Accepted &amp; Digitally Signed' in html_print or 'Accepted & Digitally Signed' in html_print)

    # Save print html to a temporary file on remote
    with open('/tmp/janvi_offer_print.html', 'w', encoding='utf-8') as f:
        f.write(html_print)
    print('Saved /tmp/janvi_offer_print.html')
"""

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

res = subprocess.run(
    ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"],
    input=remote_code,
    text=True,
    capture_output=True
)
print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
