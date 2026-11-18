import os
import sys
import json
from datetime import datetime, timedelta

# Set path to import from apps/portal
sys.path.insert(0, os.path.abspath('apps/portal'))

from app import app, get_db, get_intern_flow_state, INTERNAL_SYNC_SECRET

def run_tests():
    print("==================================================")
    print("TEST SUITE: Dead-End Remediation & Real-Time Sync")
    print("==================================================")

    client = app.test_client()

    # TEST 1: Internal sync API unauthorized check
    res = client.post("/api/internal/enrollment-sync", json={})
    assert res.status_code == 401, f"Expected 401 Unauthorized, got {res.status_code}"
    print("✓ Test 1 Passed: Unauthorized calls to /api/internal/enrollment-sync rejected (401).")

    # TEST 2: Internal sync API with valid secret and fresh candidate
    test_email = f"test_funnel_{int(datetime.now().timestamp())}@dbert.test"
    payload = {
        "fullName": "Aarav Sharma",
        "email": test_email,
        "phone": "9876543210",
        "college": "Delhi Technological University",
        "domain": "Data Analyst",
        "amount": 499,
        "payment_type": "deposit",
        "utr": "UTR499TEST001",
        "submission_id": "DBERT-CRS-TEST-001"
    }

    res2 = client.post(
        "/api/internal/enrollment-sync",
        headers={"X-DBERT-Internal-Secret": INTERNAL_SYNC_SECRET},
        json=payload
    )
    assert res2.status_code == 200, f"Expected 200 OK, got {res2.status_code}: {res2.data}"
    data2 = res2.get_json()
    assert data2["status"] == "success", f"Expected success status, got {data2}"
    print("✓ Test 2 Passed: /api/internal/enrollment-sync successfully synchronized ₹499 seat deposit.")

    # TEST 3: Verify flow state for the synced candidate
    with get_db() as conn:
        flow_st = get_intern_flow_state(conn, test_email)
        assert flow_st["is_accepted"] == True, f"Expected is_accepted=True, got {flow_st['is_accepted']}"
        assert flow_st["has_paid_deposit"] == True, f"Expected has_paid_deposit=True, got {flow_st['has_paid_deposit']}"
        assert flow_st["has_paid_balance"] == False, f"Expected has_paid_balance=False (deposit only), got {flow_st['has_paid_balance']}"
        assert flow_st["balance_due"] == 1500, f"Expected balance_due=1500, got {flow_st['balance_due']}"
    print("✓ Test 3 Passed: get_intern_flow_state correctly identifies Confirmed status with ₹1,500 balance due.")

    # TEST 4: Sync balance completion for the same candidate (₹1,500 balance)
    payload_bal = {
        "fullName": "Aarav Sharma",
        "email": test_email,
        "phone": "9876543210",
        "domain": "Data Analyst",
        "amount": 1500,
        "payment_type": "balance",
        "utr": "UTR1500TEST002",
        "submission_id": "DBERT-ENR-TEST-002"
    }

    res4 = client.post(
        "/api/internal/enrollment-sync",
        headers={"X-DBERT-Internal-Secret": INTERNAL_SYNC_SECRET},
        json=payload_bal
    )
    assert res4.status_code == 200, f"Expected 200 OK, got {res4.status_code}: {res4.data}"
    
    with get_db() as conn:
        flow_st_bal = get_intern_flow_state(conn, test_email)
        assert flow_st_bal["has_paid_balance"] == True, f"Expected has_paid_balance=True, got {flow_st_bal['has_paid_balance']}"
        assert flow_st_bal["balance_due"] == 0, f"Expected balance_due=0, got {flow_st_bal['balance_due']}"
    print("✓ Test 4 Passed: Balance payment (₹1,500) unlocks has_paid_balance=True with zero remaining balance.")

    print("\n==================================================")
    print("ALL 4 TESTS PASSED! Local verification complete.")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
