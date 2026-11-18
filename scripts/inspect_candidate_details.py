import sys
from pathlib import Path

if Path("/var/www/dbert-website-lms").exists():
    sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "apps" / "portal"))

from app import get_db

conn = get_db()
cur = conn.cursor()

emails = ["gurkavinay22@gmail.com", "sakthi220107@gmail.com", "aryanbhakuni2006@gmail.com", "sjha0940@gmail.com", "medisettyshanmukh@gmail.com", "priyanshukalondia@gmail.com"]

for em in emails:
    print(f"\n--- {em} ---")
    cur.execute("SELECT id, name, email, linkedin_url, github_url, upi_id_encrypted FROM intern_accounts WHERE LOWER(email)=%s", (em.lower(),))
    row = cur.fetchone()
    print("intern_accounts:", row)
    
    cur.execute("SELECT id, cert_id, tier FROM intern_certificates WHERE LOWER(email)=%s", (em.lower(),))
    cert = cur.fetchall()
    print("intern_certificates:", cert)
    
    if row:
        cur.execute("SELECT id, title, status FROM intern_articles WHERE intern_id=%s", (row[0],))
        arts = cur.fetchall()
        print("intern_articles:", arts)
        cur.execute("SELECT * FROM task_submissions WHERE intern_id=%s", (row[0],))
        subs = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        print("task_submissions colnames:", colnames)
        print("task_submissions rows:", subs)
