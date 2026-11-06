import os
import sys
from pathlib import Path

ROOT_DIR = Path(".").resolve()
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
sys.path.insert(0, str(PORTAL_DIR))

from services.delivery_service import EmailDeliveryService, EmailPacer

service = EmailDeliveryService()

print("--- Scenario 1: Malformed and Injection Emails ---")
for bad_email in ["", "   ", "plainaddress", "@domain.com", "user@", "user@example.com", "user@sample.com", "user@test.dbert.test"]:
    res = service.send_email(to=bad_email, subject="Test", html_content="<p>Test</p>", dry_run=True)
    assert res.success is False
    assert res.provider == "hard_bounce_guard"
    print(f"  Passed for '{bad_email}': {res.error}")

print("\n--- Scenario 2: Suspended Domains ---")
assert service.is_domain_suspended("dbert.info") is True
assert service.is_domain_suspended("mail.dbert.info") is True
assert service.is_domain_suspended("user@dbert.info") is True
assert service.is_domain_suspended("dbert.in") is False
print("  Suspended domain detection passed!")

print("\n--- Scenario 3: Pacer Concurrency ---")
import threading
pacer = EmailPacer(default_interval=0.05)
errors = []
def worker(id):
    try:
        pacer.wait_and_record(f"user{id}@dbert.in", dry_run=True)
    except Exception as e:
        errors.append(e)

threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
for t in threads: t.start()
for t in threads: t.join()
assert len(errors) == 0
print("  Pacer concurrency test (20 threads) passed!")

print("\nAll adversarial scenarios PASSED successfully!")
