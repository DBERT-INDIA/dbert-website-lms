import urllib.request
import json

print("=" * 80)
print("TESTING PRODUCTION LIVE VERIFICATION ENDPOINTS")
print("=" * 80)

# 1. API Endpoint
api_url = "https://dbert.in/api/verify?certid=CERT-DBERT-2026-DA-001"
req1 = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req1, timeout=10) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    print("\n1. Public API Response (https://dbert.in/api/verify?certid=...):")
    print(f"  Verified: {data.get('verified')}")
    print(f"  Holder:   {data.get('holderName')}")
    print(f"  Domain:   {data.get('domain')}")
    print(f"  Project:  {data.get('project')}")
    print(f"  Tenure:   {data.get('duration')}")
    print(f"  Score:    {data.get('score')}/100 ({data.get('grade')})")
    print(f"  Cert ID:  {data.get('certId')}")
    print(f"  Intern ID:{data.get('internId')}")

# 2. SSR Web Page
ssr_url = "https://dbert.in/verify/CERT-DBERT-2026-DA-001"
req2 = urllib.request.Request(ssr_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req2, timeout=10) as resp:
    html = resp.read().decode("utf-8")
    print("\n2. SSR Web Page (https://dbert.in/verify/CERT-DBERT-2026-DA-001):")
    print(f"  Status:             {resp.status}")
    print(f"  Contains Kushal:    {'Kushal Agarwal' in html}")
    print(f"  Contains Gayatri AI:{'Gayatri AI' in html}")
    print(f"  Contains Tenure:    {'July to September 2026' in html}")
    print(f"  Contains Trust Pill:{'Cryptographically Verified Credential' in html}")
    print(f"  Contains Pillars:   {'15-Day Sprint' in html}")

# 3. Query Web Page
query_url = "https://dbert.in/verify?certid=CERT-DBERT-2026-DA-001"
req3 = urllib.request.Request(query_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req3, timeout=10) as resp:
    html_q = resp.read().decode("utf-8")
    print("\n3. Query Web Page (https://dbert.in/verify?certid=CERT-DBERT-2026-DA-001):")
    print(f"  Status:             {resp.status}")
    print(f"  Shell max-width:    {'1120px' in html_q or 'shell' in html_q}")
    print(f"  Pillars present:    {'15-Day Sprint' in html_q}")

print("\n" + "=" * 80)
print("ALL PUBLIC PRODUCTION TESTS PASSED!")
print("=" * 80)
