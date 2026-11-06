import urllib.request
import json
import ssl
import sys

ctx = ssl.create_default_context()

def test_url(name, url, method="GET", data=None, headers=None, expected_status=None):
    print(f"\n--- Testing: {name} ---")
    print(f"URL: {url}")
    req = urllib.request.Request(url, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    if data:
        req.data = json.dumps(data).encode("utf-8")
        req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
            print(f"Status: {status}")
            try:
                parsed = json.loads(body)
                print(f"Response JSON: {json.dumps(parsed, indent=2)[:500]}")
            except Exception:
                print(f"Response text (first 300 chars): {body[:300]}")
            if expected_status and status != expected_status:
                print(f"FAIL: Expected {expected_status}, got {status}")
                return False
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTPError Status: {e.code}")
        try:
            parsed = json.loads(body)
            print(f"Response JSON: {json.dumps(parsed, indent=2)}")
        except Exception:
            print(f"Response text: {body[:300]}")
        if expected_status and e.code != expected_status:
            print(f"FAIL: Expected {expected_status}, got {e.code}")
            return False
        return True
    except Exception as e:
        print(f"Connection Exception: {e}")
        return False

def main():
    success = True
    # 1. Main Website
    success &= test_url("DBERT Website Main Page", "https://dbert.in", expected_status=200)

    # 2. Directory
    success &= test_url("Candidate Directory", "https://dbert.in/verify/directory", expected_status=200)

    # 3. Certificate Verification API
    success &= test_url("Verify Certificate API", "https://dbert.in/api/verify?certid=CERT-DBERT-2026-AIML-092", expected_status=200)

    # 4. Lookup API (Approved candidate Bhargavi Poola)
    success &= test_url("Lookup Bhargavi Poola", "https://dbert.in/api/enroll/lookup?email=bhargavi13032007@gmail.com", expected_status=200)

    # 5. Lookup API (DA-057)
    success &= test_url("Lookup CERT-DBERT-2026-DA-057", "https://dbert.in/api/enroll/lookup?certid=CERT-DBERT-2026-DA-057", expected_status=200)

    # 6. Lookup API (Unknown candidate - must return 404, not fake data)
    success &= test_url("Lookup Non-Existent User", "https://dbert.in/api/enroll/lookup?email=nonexistent9999@example.com", expected_status=404)

    # 7. Payment Create Order - Price Tampering Defense (amount manipulated to 100)
    success &= test_url(
        "Payment Create Order Tampering (Amount manipulated to 100)",
        "https://dbert.in/api/payments/create-order",
        method="POST",
        data={"programId": "fullstack", "amount": 100, "currency": "INR"},
        expected_status=400
    )

    # 8. Sensitive Files Block (Nginx .env block)
    success &= test_url("Block .env access", "https://dbert.in/.env", expected_status=404)
    success &= test_url("Block SQLite db access", "https://dbert.in/users.db", expected_status=404)

    # 9. LMS Portal
    success &= test_url("LMS Portal Index", "https://lms.dbert.in/", expected_status=200)
    success &= test_url("LMS Portal Admin Login Page", "https://lms.dbert.in/admin-login", expected_status=200)

    # 10. API Docs
    success &= test_url("API Docs Page", "https://api.dbert.in/docs", expected_status=200)

    print("\n==========================================")
    if success:
        print("ALL LIVE VERIFICATION TESTS PASSED SUCCESSFULLY!")
    else:
        print("SOME TESTS FAILED - REVIEW OUTPUT ABOVE.")
    print("==========================================")

if __name__ == "__main__":
    main()
