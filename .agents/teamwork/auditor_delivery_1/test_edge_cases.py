import os
import sys
from pathlib import Path

ROOT_DIR = Path(".").resolve()
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
sys.path.insert(0, str(PORTAL_DIR))

from services.delivery_service import EmailDeliveryService, EmailPacer

service = EmailDeliveryService()

print("Testing edge cases:")
for addr in ["", "  ", "no-at", "user@example.com", "user@sample.com", "user@test.dbert.test", "user@mailinator.com"]:
    res = service.send_email(to=addr, subject="Test", html_content="<p>Test</p>", dry_run=True)
    print(f"  Addr: '{addr}' -> Success: {res.success}, Provider: {res.provider}, Error: {res.error}")

print("\nTesting valid addresses in dry-run:")
for addr in ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com", "test@dbert.in"]:
    res = service.send_email(to=addr, subject="Test", html_content="<p>Test</p>", dry_run=True)
    print(f"  Addr: '{addr}' -> Success: {res.success}, Provider: {res.provider}, Msg-ID: {res.message_id}")
