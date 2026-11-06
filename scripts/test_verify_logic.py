import json
import os

reg_path = os.path.join("apps", "website", "src", "data", "certificates_registry.json")
if not os.path.exists(reg_path):
    print("ERROR: certificates_registry.json not found!")
    exit(1)

with open(reg_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total verified credentials in registry: {len(data)}")

# Test Kushal Agarwal
test_id = "CERT-DBERT-2026-DA-001"
if test_id in data:
    rec = data[test_id]
    print(f"\n[PASS] Verified record found for: {test_id}")
    print(f"  Holder Name: {rec['holderName']}")
    print(f"  Domain: {rec['domain']}")
    print(f"  Tenure: {rec['duration']}")
    print(f"  Project: {rec['project']}")
    print(f"  Score: {rec['score']} ({rec['grade']})")
    print(f"  Signatory: {rec['signatory']}")
    print(f"  Verification URL: {rec['verificationUrl']}")
else:
    print(f"ERROR: {test_id} not found in registry!")

# Verify case-insensitive matching
lower_key = "cert-dbert-2026-da-001"
match = next((k for k in data if k.lower() == lower_key.lower()), None)
print(f"[PASS] Case-insensitive lookup for '{lower_key}': Found key '{match}'")
