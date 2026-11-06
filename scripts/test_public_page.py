import urllib.request

req = urllib.request.Request(
    "https://dbert.in/verify?certid=CERT-DBERT-2026-DA-001",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode("utf-8")
    print("HTTP Status:", resp.status)
    print("Contains 'Kushal Agarwal':", "Kushal Agarwal" in html)
    print("Contains 'MSME':", "MSME" in html)
    print("Contains 'Somya':", "Somya" in html)
    print("Contains '§ 01 — CRYPTOGRAPHIC VERIFICATION':", "CRYPTOGRAPHIC VERIFICATION" in html)
    print("Page Title/Head snippet:", html[:300])
