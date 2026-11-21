import sys
import os

sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")

from app import get_db
from services.certificate_service import CertificateService

test_candidates = [
    ("me250003067@iiti.ac.in", "CERT-DBERT-2026-DA-173", "Sakthi P"),
    ("pulluribhargavi30@gmail.com", "CERT-DBERT-2026-DA-048", "Pulluri Bhargavi"),
    ("bhargavi13032007@gmail.com", "CERT-DBERT-2026-FSD-156", "Bhargavi Poola"),
    ("yasharth.poddar24@spit.ac.in", "CERT-DBERT-2026-FSD-046", "Yasharth Poddar"),
    ("radhabhamodkar@gmail.com", "CERT-DBERT-2026-DA-019", "Radha Bhamodkar"),
    ("medisettyshanmukh@gmail.com", "CERT-DBERT-2026-AIML-002", "Shanmukha Sri Saikumar Medisetty"),
    ("shanusrigowtham17@gmail.com", "CERT-DBERT-2026-AIML-013", "Shanu Sri Gowtham"),
    ("kollojumeghana@gmail.com", "CERT-DBERT-2026-DA-049", "Kolloju Meghana"),
    ("chinniprincess842@gmail.com", "CERT-DBERT-2026-DA-117", "M Brahmani"),
    ("bhargavick1@gmail.com", "CERT-DBERT-2026-AIML-020", "Bhargavi C K"),
    ("hey.deepanshu2006@gmail.com", "CERT-DBERT-2026-DA-186", "Deepanshu"),
    ("sivasankar.t1606@gmail.com", "CERT-DBERT-2026-DA-067", "Siva Sankar Thirumalasetty"),
    ("patilsatya004@gmail.com", "CERT-DBERT-2026-DA-109", "Satya Patil"),
    ("kundankumhar966@gmail.com", "CERT-DBERT-2026-FSD-056", "Kundan Kumhar")
]

print("Verifying LMS Gate 1 Status in apps/portal:")
print("=" * 95)
print(f"{'#':<3} | {'Name':<28} | {'Cert ID':<24} | {'Gate 1 (is_verified)':<20} | {'Status'}")
print("-" * 95)

with get_db() as conn:
    for idx, (email, cid, name) in enumerate(test_candidates, 1):
        info = CertificateService.is_intern_verified(conn, email=email)
        is_v = info.get("verified", False)
        status = info.get("status", "UNKNOWN")
        v_str = "PASS (UNLOCKED)" if is_v else "FAIL (LOCKED)"
        print(f"{idx:<3} | {name[:27]:<28} | {cid:<24} | {v_str:<20} | {status}")
