import sys, os
from dotenv import load_dotenv
load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from services.database.adapter import get_db_adapter

with get_db_adapter() as db:
    admins = db.execute("SELECT id, email, role FROM admin_users").fetchall()
    print("ADMIN USERS:")
    for a in admins:
        print(dict(a))
