import urllib.request
import urllib.parse
import ssl

ctx = ssl.create_default_context()

def check_url(url, follow_redirect=True):
    print(f"\nChecking: {url}")
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            if not follow_redirect:
                return None
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    opener = urllib.request.build_opener(NoRedirect()) if not follow_redirect else urllib.request.build_opener()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = opener.open(req, timeout=10)
        body = resp.read().decode('utf-8', errors='ignore')
        print(f"Status: {resp.status}")
        print(f"Final URL: {resp.url}")
        print(f"Body length: {len(body)} chars")
        return resp.status, body
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")
        if not follow_redirect and e.code in (301, 302, 307, 308):
            print(f"Location header: {e.headers.get('Location')}")
        return e.code, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Test 1: Redirect /eroll?email=bhargavi13032007@gmail.com without following
check_url("https://dbert.in/eroll?email=bhargavi13032007@gmail.com", follow_redirect=False)

# Test 2: Full fetch of /eroll?email=bhargavi13032007@gmail.com (with redirect)
status, body = check_url("https://dbert.in/eroll?email=bhargavi13032007@gmail.com", follow_redirect=True)
if body:
    print("Page includes 'Bhargavi':", 'Bhargavi' in body)
    print("Page includes 'Monday, 9 Nov 2026':", 'Monday, 9 Nov 2026' in body)
    print("Page includes countdown container:", 'countdown' in body.lower())

# Test 3: Verification route for Bhargavi
status_v, body_v = check_url("https://dbert.in/verify/CERT-DBERT-2026-FSD-156", follow_redirect=True)
if body_v:
    print("Verification page includes 'Bhargavi Poola':", 'Bhargavi Poola' in body_v)
