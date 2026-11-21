import sys
import os
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
os.chdir('/var/www/dbert-website-lms/apps/portal')
from app import get_db
with get_db() as conn:
    row = conn.execute("SELECT * FROM intern_offer_letters WHERE email = ?", ("stage3_selected@dbert.test",)).fetchone()
    print("OFFER ROW:", dict(row) if row else None)
    acc = conn.execute("SELECT * FROM intern_accounts WHERE email = ?", ("stage3_selected@dbert.test",)).fetchone()
    print("ACCOUNT ROW:", dict(acc) if acc else None)
    enr = conn.execute("SELECT * FROM enrollments WHERE email = ?", ("stage3_selected@dbert.test",)).fetchone()
    print("ENROLLMENT ROW:", dict(enr) if enr else None)
    app_row = conn.execute("SELECT * FROM applications WHERE email = ?", ("stage3_selected@dbert.test",)).fetchone()
    print("APPLICATION ROW:", dict(app_row) if app_row else None)
