import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path("apps/portal").resolve()))

# Load .env
env_file = Path("apps/portal/.env")
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

from services.delivery_service import EmailDeliveryService

svc = EmailDeliveryService(
    smtp_host=os.environ.get("SMTP_HOST"),
    smtp_port=int(os.environ.get("SMTP_PORT", "465")),
    smtp_user=os.environ.get("SMTP_USER"),
    smtp_pass=os.environ.get("SMTP_PASS"),
    from_email=os.environ.get("FROM_EMAIL"),
    from_name="Abhinav Sharma",
    reply_to=os.environ.get("FROM_EMAIL")
)

print(f"Connecting to SMTP {svc.smtp_host}:{svc.smtp_port} as {svc.smtp_user}...")
res = svc.send_email(
    to="ain.sharma.abhinav@gmail.com",
    subject="DBERT SMTP Quota Test Probe",
    html_content="<p>DBERT SMTP Quota Test Probe at 23:25</p>",
    text_content="DBERT SMTP Quota Test Probe at 23:25",
    dry_run=False
)

print("Delivery success:", res.success)
print("Provider:", res.provider)
print("Message ID:", res.message_id)
print("Error:", res.error)
