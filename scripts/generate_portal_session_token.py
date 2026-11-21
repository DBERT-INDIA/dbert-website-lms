import os, sys, secrets
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

email = sys.argv[1] if len(sys.argv) > 1 else 'bhargavi13032007@gmail.com'
token = secrets.token_hex(32)
expires_at = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

c.execute("""
    INSERT INTO dbert_internship.user_sessions (email, role, session_token, expires_at)
    VALUES (%s, 'intern', %s, %s);
""", (email.lower(), token, expires_at))
conn.commit()

print(f"SESSION_TOKEN:{token}")
