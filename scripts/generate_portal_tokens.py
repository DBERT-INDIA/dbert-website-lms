import os
import sys

sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
os.chdir("/var/www/dbert-website-lms/apps/portal")

from app import get_db, create_session

def generate():
    with get_db() as conn:
        prov = conn.execute("""
            SELECT a.email 
            FROM intern_accounts a 
            LEFT JOIN intern_certificates c ON a.id = c.intern_id AND c.tier = 'verified'
            WHERE c.id IS NULL AND a.is_active = 1
            LIMIT 1
        """).fetchone()
        prov_email = prov["email"] if prov else "provisional@dbert.test"
        
        tokens = {
            "provisional_intern": {
                "email": prov_email,
                "token": create_session(prov_email, "intern")
            }
        }
        import json
        print(json.dumps(tokens, indent=2))

if __name__ == "__main__":
    generate()
