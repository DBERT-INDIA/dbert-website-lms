import urllib.request

req = urllib.request.Request(
    "https://dbert.in/verify/CERT-DBERT-2026-DA-001",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode("utf-8")
    print("SSR Route /verify/CERT-DBERT-2026-DA-001:")
    print("HTTP Status:", resp.status)
    print("Contains 'Kushal Agarwal':", "Kushal Agarwal" in html)
    print("Contains 'Gayatri AI':", "Gayatri AI" in html)
    print("Contains 'July to September':", "July to September" in html)
