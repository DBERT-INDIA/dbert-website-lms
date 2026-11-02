#!/usr/bin/python3
"""
fix_env.cgi — Emergency .env fixer. Upload to cgi-bin, chmod 755, visit once, DELETE immediately.
"""
import sys, os, traceback

print("Content-Type: text/plain\r\n\r\n")
try:
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(app_dir, '.env')
    
    print(f"App dir: {app_dir}")
    print(f".env path: {env_path}")
    print(f".env exists: {os.path.exists(env_path)}")
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            old = f.read()
        print("\n--- OLD .env ---")
        print(old)
    
    new_env = """# ==========================================
# 1. FLASK CORE & SECURITY
# ==========================================
FLASK_ENV=development
FLASK_DEBUG=false
FLASK_SECRET_KEY=hyhyhyhy99089hhhyykjkjk_dbert_portal_2026_xyz_secure_key_extended

# ==========================================
# 2. DATABASE CONFIGURATION - SQLITE (CPANEL)
# ==========================================
REQUIRE_POSTGRES=false
DATABASE_URL=

# ==========================================
# 3. ADMIN CREDENTIALS
# ==========================================
ADMIN_USERNAME=dbert_superadmin
ADMIN_PASSWORD=Gannu@1222
ADMIN_KEY=hyhyhyhy99089hhhyykjkjkhsajhJSHyyyy

# ==========================================
# 4. EMAIL SENDING
# ==========================================
EMAILS_ENABLED=true
EMAIL_PROVIDER=smtp
SMTP_HOST=cdunhncajun5.zevm.mail-manager-smtp.amazonaws.com
SMTP_PORT=587
SMTP_USER=inp-mxpxb2byjeyfd6qiyoathjup
SMTP_PASS=S5Y^j8pWcdegAqytI,m8E2+[R+q*|7m.
FROM_EMAIL=contactus@dbert.in
FROM_NAME=DBERT Support

# ==========================================
# 5. PAYMENT / RAZORPAY
# ==========================================
RAZORPAY_KEY_ID=YOUR_LIVE_RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET=YOUR_LIVE_RAZORPAY_SECRET

# ==========================================
# 6. AI TUTOR
# ==========================================
INTERVIEW_ENABLED=true
"""
    
    with open(env_path, 'w') as f:
        f.write(new_env)
    
    print("\n--- NEW .env WRITTEN ---")
    print(new_env)
    
    # Also remove the old init flags so the DB gets re-initialized
    for flag in ['.db_initialized_v2', '.db_initialized_v3']:
        flag_path = os.path.join(app_dir, flag)
        if os.path.exists(flag_path):
            os.remove(flag_path)
            print(f"Removed: {flag_path}")
    
    print("\n=== SUCCESS! .env updated. DELETE THIS FILE NOW and hard-refresh the site. ===")

except Exception:
    traceback.print_exc(file=sys.stdout)
