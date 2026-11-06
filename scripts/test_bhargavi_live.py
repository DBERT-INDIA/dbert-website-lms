import urllib.request
import json
import ssl

ctx = ssl.create_default_context()

print("Testing https://dbert.in/api/enroll/lookup?email=bhargavi13032007@gmail.com ...")
try:
    req = urllib.request.Request(
        "https://dbert.in/api/enroll/lookup?email=bhargavi13032007@gmail.com",
        headers={"User-Agent": "DBERT-Verification/1.0"}
    )
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        print("Status code:", resp.status)
        print("Response JSON:")
        print(json.dumps(data, indent=2))
except Exception as e:
    print("Error:", e)
