
import sys
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
from app import app, get_or_create_offer_letter, get_intern_active_gemini_context, create_session, get_db

with get_db() as conn:
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'user_api_keys'")
    print("user_api_keys columns:", cur.fetchall())

    cur.execute("SELECT * FROM user_api_keys LIMIT 1")
    print("user_api_keys sample:", cur.fetchone())
