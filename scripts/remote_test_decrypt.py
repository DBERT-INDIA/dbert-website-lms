
import sys
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
from app import _decrypt_gemini_key, get_db

with get_db() as conn:
    cur = conn.cursor()
    cur.execute("SELECT id, intern_id, encrypted_key FROM user_api_keys WHERE intern_id = 5042")
    row = cur.fetchone()
    print("Row:", row)
    enc = row[2]
    dec = _decrypt_gemini_key(enc)
    print("Decrypted key:", dec[:10] if dec else dec)
