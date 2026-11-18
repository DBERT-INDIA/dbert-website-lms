import sys, json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db, _decrypt_gemini_key, _gemini_stream_byok_call

with get_db() as conn:
    key_row = conn.execute("SELECT encrypted_key, available_models_json FROM user_api_keys WHERE intern_id = 5624 ORDER BY id DESC LIMIT 1").fetchone()
    raw_key = _decrypt_gemini_key(key_row['encrypted_key'])
    user_models = json.loads(key_row['available_models_json'])
    print("Decrypted key starts with: " + raw_key[:10] + "...")
    print("User models count: " + str(len(user_models)))
    
    # Test streaming call with a simple prompt
    prompt = "Explain the CIA Triad in cybersecurity in 2 sentences."
    print("Testing _gemini_stream_byok_call...")
    chunks = []
    err_found = None
    for chunk, err in _gemini_stream_byok_call(prompt, api_key=raw_key, user_models=user_models):
        if err:
            err_found = err
            print("Error during stream: " + str(err))
            break
        if chunk:
            chunks.append(chunk)
    
    print("Total chunks received: " + str(len(chunks)))
    if chunks:
        print("Generated text:")
        print("".join(chunks))
    if err_found:
        print("Encountered error: " + str(err_found))
