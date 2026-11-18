import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db, get_intern_flow_state, verify_password, _email_sig, EMAIL_SITE

with app.app_context():
    conn = get_db()
    cur = conn.cursor()
    
    # 1. Check distinct statuses in applications
    cur.execute("SELECT status, count(*) FROM applications GROUP BY status ORDER BY count(*) DESC")
    print("\n--- APPLICATION STATUS COUNTS IN POSTGRESQL ---")
    for row in cur.fetchall():
        print(f"Status: {row[0]} | Count: {row[1]}")

    # 2. Check distinct payment statuses in enrollments
    cur.execute("SELECT payment_status, count(*) FROM enrollments GROUP BY payment_status ORDER BY count(*) DESC")
    print("\n--- ENROLLMENT PAYMENT STATUSES ---")
    for row in cur.fetchall():
        print(f"Payment Status: {row[0]} | Count: {row[1]}")

    # 3. Representative accounts across each user lifecycle stage
    test_emails = [
        # Stage 1: Applied / New
        "stage1_apply@dbert.test",
        # Stage 2: Under Review
        "stage2_review@dbert.test",
        # Stage 3: Selected / Deposit Pending
        "stage3_selected@dbert.test",
        # Stage 4: Deposit Paid / Verifying
        "stage4_pending@dbert.test",
        # Stage 5: Confirmed Intern (Within 7-day balance grace)
        "stage5_enrolled@dbert.test",
        # Stage 5 Overdue: Confirmed Intern (Grace expired)
        "stage5_grace_expired@dbert.test",
        # Stage 5 Fully Paid: ₹1,999 Completed
        "fellow_paid_1999@dbert.test",
        # Stipend Stages
        "stipend_gate1_locked@dbert.test",
        "stipend_ready@dbert.test",
        "stipend_wallet@dbert.test",
        # Admin / Staff
        "admin@dbert.test",
        "staff@dbert.test"
    ]

    print("\n=========================================================================================")
    print("DETAILED USER FLOW & LIFECYCLE REVENUE STAGES:")
    print("=========================================================================================")
    
    for email in test_emails:
        cur.execute("""
            SELECT i.id, i.name, i.email, i.domain, a.status as app_status,
                   e.payment_status, e.deposit_paid, e.balance_paid, e.joining_date,
                   (SELECT count(*) FROM intern_certificates c WHERE c.email = i.email) as cert_count
            FROM intern_accounts i
            LEFT JOIN applications a ON a.email = i.email
            LEFT JOIN enrollments e ON e.email = i.email
            WHERE i.email = %s
        """, (email,))
        r = cur.fetchone()
        if r:
            intern_id = r[0]
            flow_state = get_intern_flow_state(conn, email)
            print(f"\n[ACCOUNT] ID: {r[0]} | Name: {r[1]} | Email: {r[2]}")
            print(f"   Domain: {r[3]}")
            print(f"   App Status: {r[4]} | Payment Status: {r[5]}")
            print(f"   Deposit Paid: {r[6]} | Balance Paid: {r[7]} | Joining: {r[8]}")
            print(f"   Cert Count: {r[9]}")
            print(f"   Calculated Flow State:")
            print(f"     -> stage_num: {flow_state.get('stage_num')} ({flow_state.get('stage_name')})")
            print(f"     -> has_paid_deposit: {flow_state.get('has_paid_deposit')}")
            print(f"     -> has_paid_balance: {flow_state.get('has_paid_balance')}")
            print(f"     -> balance_due: ₹{flow_state.get('balance_due')}")
            print(f"     -> days_since_joining: {flow_state.get('days_since_joining')}")
            print(f"     -> balance_grace_expired: {flow_state.get('balance_grace_expired')}")
            print(f"     -> certificate_locked: {flow_state.get('certificate_locked')}")
            print(f"     -> stipend_locked: {flow_state.get('stipend_locked')}")
            print(f"     -> is_verified_alumnus: {flow_state.get('is_verified_alumnus')}")
            print(f"     -> is_provisional_alumnus: {flow_state.get('is_provisional_alumnus')}")
            
            # Check password & generate 1-click URL
            cur.execute("SELECT password_hash, password_set FROM intern_accounts WHERE email = %s", (email,))
            ph_row = cur.fetchone()
            ph = ph_row[0] if ph_row else ""
            pw_set = ph_row[1] if ph_row else 0
            is_valid = verify_password(ph, "TestPass123!")
            sig = _email_sig("activate", email)
            login_url = f"https://lms.dbert.in/auth/activate?e={email}&t={sig}&next=/portal"
            offer_url = f"https://lms.dbert.in/auth/activate?e={email}&t={sig}&next=/portal/offer"
            stipend_url = f"https://lms.dbert.in/auth/activate?e={email}&t={sig}&next=/stipend/tasks"
            print(f"     -> Password 'TestPass123!' valid: {is_valid} (password_set: {pw_set})")
            print(f"     -> 1-Click Portal: {login_url}")
            print(f"     -> 1-Click Offer:  {offer_url}")
            print(f"     -> 1-Click Stipend: {stipend_url}")
