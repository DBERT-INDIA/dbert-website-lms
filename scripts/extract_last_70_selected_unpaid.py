import os
import sys
import json
import re
import subprocess

def clean_phone(raw_phone: str) -> str:
    if not raw_phone:
        return ""
    digits = re.sub(r"\D", "", str(raw_phone))
    if digits.startswith("91") and len(digits) == 12:
        return digits
    if len(digits) == 10:
        return f"91{digits}"
    if len(digits) > 10 and digits.startswith("0"):
        digits = digits.lstrip("0")
        if len(digits) == 10:
            return f"91{digits}"
    return digits

def main():
    print("=== EXTRACTING LAST 70 SELECTED UNPAID INTERNS FROM EC2 ===")

    # Load already messaged emails from previous followups
    already_messaged = set()
    for log_path in ['data/whatsapp_followup_sent_log.json']:
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                for r in json.load(f):
                    em = (r.get('email') or '').strip().lower()
                    if em:
                        already_messaged.add(em)
    print(f"Already messaged in previous task: {len(already_messaged)} candidates")

    ssh_cmd = [
        "ssh", "-i", r"C:\Users\user\.ssh\dbert-production-server.pem",
        "-o", "StrictHostKeyChecking=no",
        "ubuntu@3.26.237.171",
        "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 - << 'EOF'\n"
        "import sys, json\n"
        "sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')\n"
        "from dotenv import load_dotenv\n"
        "load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')\n"
        "from services.database.adapter import get_db_adapter\n"
        "\n"
        "with get_db_adapter() as conn:\n"
        "    # Query latest Selected candidates where payment is NOT Accepted\n"
        "    rows = conn.execute(\"\"\"\n"
        "        SELECT a.id, a.name, a.email, a.phone, a.domain, a.college, a.status, a.created_at, a.updated_at\n"
        "        FROM applications a\n"
        "        WHERE a.status = 'Selected'\n"
        "          AND a.email NOT IN (\n"
        "              SELECT email FROM enrollments WHERE payment_status = 'Accepted'\n"
        "          )\n"
        "        ORDER BY a.id DESC\n"
        "        LIMIT 150\n"
        "    \"\"\").fetchall()\n"
        "    res = [dict(r) for r in rows]\n"
        "    print(json.dumps(res, default=str))\n"
        "EOF\n"
    ]

    proc = subprocess.run(ssh_cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("SSH Error:", proc.stderr)
        return

    data = json.loads(proc.stdout)
    print(f"Fetched {len(data)} latest Selected unpaid candidates from EC2.")

    filtered_70 = []
    seen_emails = set()
    seen_phones = set()

    for r in data:
        em = (r.get('email') or '').strip().lower()
        raw_phone = r.get('phone', '')
        phone = clean_phone(raw_phone)
        name = (r.get('name') or '').strip()

        if not em or em in seen_emails or em in already_messaged:
            continue
        if not phone or len(phone) < 12 or phone in seen_phones:
            continue

        seen_emails.add(em)
        seen_phones.add(phone)

        filtered_70.append({
            "id": r['id'],
            "name": name,
            "email": em,
            "phone": phone,
            "raw_phone": raw_phone,
            "domain": (r.get('domain') or 'Applied Engineering').strip(),
            "college": (r.get('college') or '').strip(),
            "created_at": str(r.get('created_at', '')),
            "updated_at": str(r.get('updated_at', ''))
        })

        if len(filtered_70) == 70:
            break

    print(f"Extracted exactly {len(filtered_70)} clean, deduplicated candidates with valid WhatsApp phone numbers!")

    out_file = 'data/whatsapp_last_70_selected_unpaid.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_70, f, indent=2, ensure_ascii=False)
    print(f"Saved to {out_file}")

    print("\nFirst 5 candidates:")
    for c in filtered_70[:5]:
        print(f"  #{c['id']}: {c['name']} | {c['email']} | Phone: {c['phone']} | {c['domain']}")

    print("\nLast 5 candidates:")
    for c in filtered_70[-5:]:
        print(f"  #{c['id']}: {c['name']} | {c['email']} | Phone: {c['phone']} | {c['domain']}")

if __name__ == '__main__':
    main()
