import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db, get_intern_flow_state, get_or_create_offer_letter

with app.app_context():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'intern_offer_letters'")
    print("intern_offer_letters columns:", [r[0] for r in cur.fetchall()])

    print("\n=== SEARCHING FOR INTERN ACCOUNT 5624 OR 5166 OR abhinav.sharma@dbert.vom ===")
    cur.execute("""
        SELECT id, name, email, phone, college, domain, course, signup_stage, is_active, created_at
        FROM intern_accounts 
        WHERE email LIKE '%abhinav.sharma%' OR id IN (5624, 5166) OR email LIKE '%dbert.vom%'
    """)
    accounts = cur.fetchall()
    for r in accounts:
        print(f"Account: ID={r[0]} | Name={r[1]} | Email={r[2]} | Phone={r[3]} | College={r[4]} | Domain={r[5]} | Course={r[6]} | Stage={r[7]}")
        
        # Check Application
        cur.execute("SELECT id, email, status, domain, college, course FROM applications WHERE email = %s OR id = %s", (r[2], r[0]))
        apps = cur.fetchall()
        for a in apps:
            print(f"  -> App: ID={a[0]} | Email={a[1]} | Status={a[2]} | Domain={a[3]} | College={a[4]}")
            
        # Check Enrollment
        cur.execute("SELECT id, intern_id, email, payment_status, deposit_paid, balance_paid, amount, joining_date FROM enrollments WHERE email = %s OR intern_id = %s", (r[2], r[0]))
        enrs = cur.fetchall()
        for e in enrs:
            print(f"  -> Enrollment: ID={e[0]} | InternID={e[1]} | Email={e[2]} | PayStatus={e[3]} | DepositPaid={e[4]} | BalancePaid={e[5]} | Join={e[7]}")
            
        # Check Offer Letter by SELECT *
        cur.execute("SELECT * FROM intern_offer_letters WHERE email = %s OR intern_id = %s", (r[2], r[0]))
        offers = cur.fetchall()
        for o in offers:
            print(f"  -> Offer Record: {o}")
            
        # Flow State
        fs = get_intern_flow_state(conn, r[2])
        print(f"  -> get_intern_flow_state:")
        print(f"       stage_num: {fs.get('stage_num')} ({fs.get('stage_name')})")
        print(f"       is_accepted: {fs.get('is_accepted')}")
        print(f"       label: {fs.get('label')}")
        print(f"       has_paid_deposit: {fs.get('has_paid_deposit')}")
        print(f"       has_paid_balance: {fs.get('has_paid_balance')}")
        print(f"       balance_due: {fs.get('balance_due')}")
        print(f"       balance_grace_expired: {fs.get('balance_grace_expired')}")
        
        # Check get_or_create_offer_letter
        ol = get_or_create_offer_letter(r[2])
        print(f"  -> get_or_create_offer_letter:")
        print(f"       ref_id: {ol.get('ref_id')}")
        print(f"       status: {ol.get('status')}")
        print(f"       is_signed: {ol.get('is_signed')}")
        print(f"       requires_deposit: {ol.get('requires_deposit')}")
        print(f"       pdf_unlocked: {ol.get('pdf_unlocked')}")
        print(f"       caution_deposit_status: {ol.get('caution_deposit_status')}")
