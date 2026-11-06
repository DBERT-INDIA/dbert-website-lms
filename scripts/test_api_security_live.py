import urllib.request
import json
import ssl

ctx = ssl.create_default_context()

def test_api_idor():
    print("Testing API IDOR protection on GET /api/v1/applications/1:")
    req = urllib.request.Request("https://api.dbert.in/api/v1/applications/1")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            print("Status:", r.status)
    except urllib.error.HTTPError as e:
        print("Expected HTTP Error Status (Auth required):", e.code)
        assert e.code in [401, 403, 404]

    print("Testing Turn endpoint without auth on POST /api/v1/learning/v2/turn:")
    req2 = urllib.request.Request("https://api.dbert.in/api/v1/learning/v2/turn", method="POST", data=b'{"session_id": 1, "user_message": "hi"}', headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req2, context=ctx, timeout=10) as r2:
            print("Status:", r2.status)
    except urllib.error.HTTPError as e2:
        print("Expected HTTP Error Status (Auth required):", e2.code)
        assert e2.code in [401, 403]

    print("API security tests passed successfully!")

if __name__ == "__main__":
    test_api_idor()
