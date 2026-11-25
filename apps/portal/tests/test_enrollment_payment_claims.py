"""Exercise the manual payment ledger against disposable synthetic records."""

import sqlite3

import pytest

from services.enrollment_payment_claims import (
    PaymentClaimError,
    create_payment_claim_schema,
    review_payment_claim,
    submit_payment_claim,
)


TIMESTAMP = "2026-01-01 01:02:03"
TRACK = "Data Analyst"


@pytest.fixture
def database():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE intern_accounts (
            id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, phone TEXT, college TEXT,
            domain TEXT, password_hash TEXT, password_set INTEGER, is_active INTEGER,
            signup_stage INTEGER, created_at TEXT, updated_at TEXT
        );
        CREATE TABLE enrollments (
            id INTEGER PRIMARY KEY, intern_id INTEGER, timestamp TEXT, name TEXT,
            email TEXT UNIQUE, phone TEXT, college TEXT, domain TEXT,
            payment_status TEXT, product TEXT, amount INTEGER, amount_paid INTEGER,
            deposit_paid INTEGER, balance_paid INTEGER, utr TEXT, utr_number TEXT,
            submission_id TEXT, created_at TEXT, updated_at TEXT
        );
    """)
    create_payment_claim_schema(conn)
    try:
        yield conn
    finally:
        conn.close()


def _claim(**overrides):
    data = {
        "submission_id": "claim-demo-deposit",
        "utr": "DEMO00000001",
        "email": "learner@example.test",
        "name": "Sample Student",
        "phone": "1111111111",
        "college": "Example College",
        "domain": TRACK,
        "payment_type": "deposit",
        "amount": 499,
    }
    return {**data, **overrides}


def _balance(**overrides):
    return _claim(**{
        "submission_id": "claim-demo-balance",
        "utr": "DEMO00000002",
        "payment_type": "balance",
        "amount": 1500,
        **overrides,
    })


def _submit(database, claim):
    with database:
        return submit_payment_claim(
            database, claim, TIMESTAMP, lambda text: TRACK if text == TRACK else None,
        )


def _verify(database, claim):
    with database:
        return review_payment_claim(
            database, claim["submission_id"], "verified", claim["amount"], "1", "Checked settlement", TIMESTAMP,
        )


def test_retried_claim_leaves_an_enrollment_untouched_until_verified(database):
    original, duplicate = _submit(database, _claim())
    assert duplicate is False
    retried, duplicate = _submit(database, _claim(submission_id="other-client-receipt"))
    assert duplicate is True
    assert retried["submission_id"] == original["submission_id"]
    assert retried["status"] == "pending"
    assert database.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0] == 0
    assert database.execute("SELECT COUNT(*) FROM intern_accounts").fetchone()[0] == 0


def test_mismatched_reference_or_price_is_rejected(database):
    _submit(database, _claim())
    with pytest.raises(PaymentClaimError, match="different claim"):
        _submit(database, _claim(email="other@example.test"))
    with pytest.raises(PaymentClaimError, match="price"):
        _submit(database, _balance(amount=499))
    assert database.execute("SELECT COUNT(*) FROM enrollment_payment_claims").fetchone()[0] == 1


def test_verified_payments_credit_once_and_preserve_the_deposit(database):
    _submit(database, _balance())
    with pytest.raises(PaymentClaimError, match="Verify the enrollment deposit"):
        _verify(database, _balance())
    assert database.execute("SELECT status FROM enrollment_payment_claims").fetchone()[0] == "pending"

    _submit(database, _claim())
    assert _verify(database, _claim()) is True
    assert _verify(database, _balance()) is True
    assert _verify(database, _balance()) is False
    enrollment = database.execute(
        "SELECT amount_paid, deposit_paid, balance_paid, payment_status FROM enrollments"
    ).fetchone()
    assert tuple(enrollment) == (1999, 1, 1, "Accepted")
    assert database.execute("SELECT COUNT(*) FROM intern_accounts").fetchone()[0] == 1

    later_balance = _balance(submission_id="different-balance", utr="DEMO00000003")
    _submit(database, later_balance)
    with pytest.raises(PaymentClaimError, match="already credited"):
        _verify(database, later_balance)
    assert database.execute("SELECT amount_paid FROM enrollments").fetchone()[0] == 1999


def test_match_amount_before_review_and_reject_without_credit(database):
    _submit(database, _claim())
    with pytest.raises(PaymentClaimError, match="amount received"):
        with database:
            review_payment_claim(database, _claim()["submission_id"], "verified", 1, "1", "", TIMESTAMP)
    with database:
        assert review_payment_claim(
            database, _claim()["submission_id"], "rejected", None, "1", "No settlement", TIMESTAMP,
        ) is True
    with pytest.raises(PaymentClaimError, match="already been reviewed"):
        _verify(database, _claim())
    assert database.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0] == 0


def test_existing_verified_reference_is_left_intact(database):
    database.execute("""
        INSERT INTO enrollments (email, payment_status, amount_paid, utr_number)
        VALUES (?, 'Accepted', 499, 'DEMO00000001')
    """, (_claim()["email"],))
    _submit(database, _claim())
    with pytest.raises(PaymentClaimError, match="already present"):
        _verify(database, _claim())
    assert database.execute("SELECT amount_paid FROM enrollments").fetchone()[0] == 499
    assert database.execute("SELECT status FROM enrollment_payment_claims").fetchone()[0] == "pending"
    assert database.execute("SELECT COUNT(*) FROM intern_accounts").fetchone()[0] == 0


def test_failed_ledger_write_rolls_back_claim_and_account(database):
    _submit(database, _claim())
    database.executescript("""
        CREATE TRIGGER stop_enrollment_write BEFORE INSERT ON enrollments
        BEGIN SELECT RAISE(ABORT, 'synthetic ledger failure'); END;
    """)
    with pytest.raises(sqlite3.IntegrityError, match="synthetic ledger failure"):
        _verify(database, _claim())
    assert database.execute("SELECT status FROM enrollment_payment_claims").fetchone()[0] == "pending"
    assert database.execute("SELECT COUNT(*) FROM intern_accounts").fetchone()[0] == 0
