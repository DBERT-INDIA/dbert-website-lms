import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "portal")))
os.environ["TESTING"] = "true"

from app import app, get_db, credit_intern_coins, create_session, AUTH_COOKIE

def test_flow():
    conn = get_db()
    conn.execute("DELETE FROM intern_accounts WHERE id = 999 OR email = 'test.intern999@dbert.in'")
    conn.execute("DELETE FROM user_sessions WHERE email = 'test.intern999@dbert.in'")
    conn.execute("DELETE FROM coin_ledger_mirror WHERE intern_id = 999")
    conn.execute("DELETE FROM coin_perk_redemptions WHERE intern_id = 999")
    conn.commit()

    conn.execute("INSERT INTO intern_accounts (id, name, email, phone, domain, is_active) VALUES (999, 'Test Intern', 'test.intern999@dbert.in', '9999999999', 'Full Stack Web Development', 1)")
    conn.commit()

    token = create_session("test.intern999@dbert.in", "intern")

    with app.test_client() as client:
        headers = {
            "X-Session-Token": token,
            "X-CSRF-Token": "test_token"
        }
        with client.session_transaction() as sess:
            sess["_csrf"] = "test_token"

        # 1. Check with 0 balance -> Insufficient balance error
        r1 = client.post("/api/coins/redeem", json={"perk_slug": "ai_ats_scanner"}, headers=headers)
        data1 = r1.get_json()
        print("1. Insufficient balance test:", r1.status_code, data1["message"])

        # 2. Credit 250 task coins
        credit_intern_coins(conn, 999, 250, "Sprint Pass Reward", ref_id="test_unit_999", email="test.intern999@dbert.in")
        conn.commit()

        # 3. Redeem 100 coins for ai_ats_scanner
        r2 = client.post("/api/coins/redeem", json={"perk_slug": "ai_ats_scanner"}, headers=headers)
        data2 = r2.get_json()
        print("2. Redemption response:", r2.status_code, data2["message"])
        print("   Voucher code:", data2["redemption_code"])
        print("   Coins spent:", data2["coins_spent"])
        print("   New balance:", data2["new_balance"])

        # 4. Check /api/coins/perks
        r3 = client.get("/api/coins/perks", headers=headers)
        data3 = r3.get_json()
        print("3. Perks API check:")
        print("   Active perks available:", len(data3["perks"]))
        print("   Current task balance:", data3["task_balance"])
        print("   Redemption records:", len(data3["my_redemptions"]))

        # 5. Redeem another perk: ai_mock_interview (100 coins)
        r4 = client.post("/api/coins/redeem", json={"perk_slug": "ai_mock_interview"}, headers=headers)
        data4 = r4.get_json()
        print("4. Second redemption response:", r4.status_code, data4["message"])
        print("   Remaining balance:", data4["new_balance"])

        # 6. Clean up test records
        conn.execute("DELETE FROM coin_perk_redemptions WHERE intern_id = 999")
        conn.execute("DELETE FROM coin_ledger_mirror WHERE intern_id = 999")
        conn.execute("DELETE FROM intern_accounts WHERE id = 999")
        conn.execute("DELETE FROM user_sessions WHERE email = 'test.intern999@dbert.in'")
        conn.commit()
        conn.close()
        print("5. Test clean-up completed.")

if __name__ == "__main__":
    test_flow()
