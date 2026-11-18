import sys, json, requests
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db, _decrypt_gemini_key

with get_db() as conn:
    key_row = conn.execute("SELECT encrypted_key FROM user_api_keys WHERE intern_id = 5624 ORDER BY id DESC LIMIT 1").fetchone()
    raw_key = _decrypt_gemini_key(key_row['encrypted_key'])

models_to_test = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.5-flash",
    "gemini-3.8-flash"
]

body = {
    "contents": [{"parts": [{"text": "Hello"}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 20}
}

for m in models_to_test:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"
    r = requests.post(url, params={"key": raw_key}, json=body, timeout=10)
    print(f"Model {m}: HTTP {r.status_code} - {r.text[:150]}")
