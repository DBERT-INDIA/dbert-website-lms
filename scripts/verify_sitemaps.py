import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

sitemaps = [
    ("Website Main Sitemap", "https://dbert.in/sitemap.xml"),
    ("LMS Sitemap", "https://lms.dbert.in/sitemap.xml"),
    ("Website LMS Proxy Sitemap", "https://dbert.in/sitemap-lms.xml")
]

for name, url in sitemaps:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, context=ctx, timeout=15)
        body = resp.read().decode("utf-8")
        is_xml = body.startswith("<?xml")
        print(f"{name:26s} | HTTP {resp.status} | Length: {len(body):8d} bytes | Valid XML: {is_xml}")
    except Exception as e:
        print(f"{name:26s} | ERROR: {e}")
