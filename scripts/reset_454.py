import sys, os
from dotenv import load_dotenv
load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from services.database.adapter import get_db_adapter

with get_db_adapter() as db:
    db.execute("UPDATE enrollments SET payment_status='Pending Verification' WHERE id=454")
    db.commit()
    r = db.execute("SELECT id, name, payment_status FROM enrollments WHERE id=454").fetchone()
    print("Reset enrollment 454:", dict(r))
