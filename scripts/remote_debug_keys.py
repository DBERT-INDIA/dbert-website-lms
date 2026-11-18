
import os, sys, base64, hashlib, hmac
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")

from app import _fernet, _get_gemini_fernet, _FLASK_SECRET_KEY, get_db

with get_db() as conn:
    cur = conn.cursor()
    cur.execute("SELECT intern_id, encrypted_key FROM user_api_keys LIMIT 5")
    rows = cur.fetchall()
    for intern_id, enc in rows:
        print(f"Intern {intern_id}: {enc}")
        f = _get_gemini_fernet()
        print("  Fernet:", f)
        if f:
            try:
                dec = f.decrypt(enc.encode('utf-8')).decode('utf-8')
                print("  Fernet dec:", dec[:10])
            except Exception as e:
                print("  Fernet dec err:", e)
        # Try base64 urlsafe decode
        try:
            raw = base64.urlsafe_b64decode(enc.encode('utf-8'))
            print("  Base64 len:", len(raw))
        except Exception as e:
            print("  Base64 err:", e)
