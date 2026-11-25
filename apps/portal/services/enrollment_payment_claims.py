"""Persist manual UPI claims separately from verified enrollment payments."""

import re
import secrets

from werkzeug.security import generate_password_hash


PAYMENT_AMOUNTS = {"deposit": 499, "balance": 1500}
CLAIM_STATUSES = ("pending", "verified", "rejected")
ENROLLMENT_PAYMENT_COLUMNS = (
    ("intern_id", "INTEGER"),
    ("utr", "TEXT"),
    ("amount_paid", "INTEGER DEFAULT 0"),
    ("utr_number", "TEXT"),
    ("deposit_paid", "INTEGER DEFAULT 0"),
    ("balance_paid", "INTEGER DEFAULT 0"),
    ("submission_id", "TEXT"),
)


class PaymentClaimError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def create_payment_claim_schema(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS enrollment_payment_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id TEXT NOT NULL UNIQUE,
            utr_number TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            college TEXT NOT NULL,
            domain TEXT NOT NULL,
            certificate_reference TEXT,
            intern_reference TEXT,
            submission_note TEXT,
            payment_type TEXT NOT NULL CHECK (payment_type IN ('deposit', 'balance')),
            amount INTEGER NOT NULL CHECK (amount > 0),
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'verified', 'rejected')),
            submitted_at TEXT NOT NULL,
            reviewed_at TEXT,
            reviewer_id TEXT,
            review_note TEXT
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_payment_claim_status_submitted
        ON enrollment_payment_claims (status, submitted_at, id)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_payment_claim_email
        ON enrollment_payment_claims (email, submitted_at, id)
    """)


def _field(data, *keys, limit):
    for key in keys:
        value = data.get(key)
        if value is not None:
            if not isinstance(value, str):
                raise PaymentClaimError(f"{keys[0]} must be text.")
            value = value.strip()
            if len(value) > limit:
                raise PaymentClaimError(f"{keys[0]} is too long.")
            if value:
                return value
    return ""


def submit_payment_claim(conn, data, now, normalize_domain):
    """Insert a claim or return the existing receipt for an equivalent retry."""
    if not isinstance(data, dict):
        raise PaymentClaimError("Send a JSON payment claim.")
    email = _field(data, "email", limit=254).lower()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise PaymentClaimError("A valid email address is required.")
    utr = _field(data, "utr", "utrNumber", "utr_number", limit=64).upper()
    if not re.fullmatch(r"[A-Z0-9]{6,64}", utr):
        raise PaymentClaimError("Enter a valid UPI transaction reference.")
    submission_id = _field(data, "submission_id", "id", limit=80)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{5,79}", submission_id):
        raise PaymentClaimError("A valid submission reference is required.")
    payment_type = _field(data, "payment_type", limit=16).lower()
    amount = PAYMENT_AMOUNTS.get(payment_type)
    requested_amount = data.get("amount")
    if amount is None or type(requested_amount) is not int or requested_amount != amount:
        raise PaymentClaimError("The submission does not match the enrollment price.")
    domain = normalize_domain(_field(data, "domain", "track", limit=100))
    if not domain:
        raise PaymentClaimError("Select a valid enrollment track.")
    full_name = _field(data, "name", "fullName", limit=120)
    phone = _field(data, "phone", limit=32)
    college = _field(data, "college", limit=160)
    certificate_reference = _field(data, "cert_id", limit=80)
    intern_reference = _field(data, "intern_reference", limit=80)
    submission_note = _field(data, "remarks", limit=400)
    if not full_name:
        raise PaymentClaimError("A full name is required.")

    inserted = conn.execute("""
        INSERT INTO enrollment_payment_claims
        (submission_id, utr_number, email, full_name, phone, college, domain,
         certificate_reference, intern_reference, submission_note, payment_type, amount, submitted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT DO NOTHING
    """, (
        submission_id, utr, email, full_name, phone, college, domain, certificate_reference,
        intern_reference, submission_note, payment_type, amount, now,
    ))
    exact_id = conn.execute("""
        SELECT * FROM enrollment_payment_claims WHERE submission_id=?
    """, (submission_id,)).fetchone()
    row = exact_id or conn.execute("""
        SELECT * FROM enrollment_payment_claims WHERE utr_number=?
    """, (utr,)).fetchone()
    if row is None or (
        row["utr_number"], row["email"], row["payment_type"], row["amount"]
    ) != (utr, email, payment_type, amount):
        raise PaymentClaimError("This payment reference is already associated with a different claim.", 409)
    return row, inserted.rowcount != 1


def review_payment_claim(conn, submission_id, decision, verified_amount, actor_id, note, now):
    """Persist an admin decision and apply a newly verified payment atomically."""
    if decision not in ("verified", "rejected"):
        raise PaymentClaimError("Select Verify or Reject.")
    if len(note) > 400 or (decision == "rejected" and not note):
        raise PaymentClaimError("Provide a review note of up to 400 characters.")
    claim = conn.execute("""
        SELECT * FROM enrollment_payment_claims WHERE submission_id=?
    """, (submission_id,)).fetchone()
    if claim is None:
        raise PaymentClaimError("Payment submission not found.", 404)
    if claim["status"] == decision:
        return False
    if claim["status"] != "pending":
        raise PaymentClaimError("This submission has already been reviewed.", 409)
    if decision == "verified" and verified_amount != claim["amount"]:
        raise PaymentClaimError("The amount received must match the amount shown.")

    reviewed = conn.execute("""
        UPDATE enrollment_payment_claims
        SET status=?, reviewed_at=?, reviewer_id=?, review_note=?
        WHERE id=? AND status='pending'
    """, (decision, now, actor_id, note, claim["id"]))
    if reviewed.rowcount != 1:
        raise PaymentClaimError("Another reviewer already processed this submission. Refresh the queue.", 409)
    if decision == "verified":
        _credit_verified_claim(conn, claim, now)
    return True


def _credit_verified_claim(conn, claim, now):
    email = claim["email"]
    is_balance = claim["payment_type"] == "balance"
    if not is_balance:
        account = conn.execute("""
            SELECT id FROM intern_accounts WHERE LOWER(email)=? ORDER BY id LIMIT 1
        """, (email,)).fetchone()
        if not account:
            conn.execute("""
                INSERT INTO intern_accounts
                (name, email, phone, college, domain, password_hash, password_set,
                 is_active, signup_stage, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, 0, 1, 3, ?, ?)
                ON CONFLICT(email) DO NOTHING
            """, (
                claim["full_name"], email, claim["phone"], claim["college"],
                claim["domain"], generate_password_hash(secrets.token_urlsafe(24)), now, now,
            ))

    row_lock = " FOR UPDATE" if getattr(conn, "dialect", "") == "postgres" else ""
    account = conn.execute(
        "SELECT id FROM intern_accounts WHERE LOWER(email)=? ORDER BY id LIMIT 1" + row_lock,
        (email,),
    ).fetchone()
    enrollment = conn.execute(
        """SELECT id, payment_status, amount_paid, amount, utr, utr_number, submission_id,
                  deposit_paid, balance_paid
           FROM enrollments WHERE LOWER(email)=? ORDER BY id DESC LIMIT 1""" + row_lock,
        (email,),
    ).fetchone()
    existing_reference = conn.execute("""
        SELECT id FROM enrollments
        WHERE payment_status IN ('Accepted', 'Verified')
          AND (UPPER(utr_number)=? OR UPPER(utr)=? OR submission_id=?)
        LIMIT 1
    """, (claim["utr_number"], claim["utr_number"], claim["submission_id"])).fetchone()
    if existing_reference:
        raise PaymentClaimError("This reference is already present in the verified enrollment ledger.", 409)

    prior_amount = 0
    deposit_verified = False
    balance_verified = False
    if enrollment:
        prior_amount = enrollment["amount_paid"] or 0
        if enrollment["payment_status"] in ("Accepted", "Verified"):
            prior_amount = prior_amount or enrollment["amount"] or 0
        deposit_verified = bool(enrollment["deposit_paid"]) or prior_amount >= PAYMENT_AMOUNTS["deposit"]
        balance_verified = bool(enrollment["balance_paid"]) or prior_amount >= sum(PAYMENT_AMOUNTS.values())
    if is_balance and (not account or not deposit_verified):
        raise PaymentClaimError("Verify the enrollment deposit before approving the balance.", 409)
    if (is_balance and balance_verified) or (not is_balance and deposit_verified):
        raise PaymentClaimError("This part of the enrollment is already credited. Check the settlement ledger.", 409)

    total = prior_amount + claim["amount"]
    if enrollment:
        conn.execute("""
            UPDATE enrollments
            SET intern_id=COALESCE(intern_id, ?), payment_status='Accepted',
                amount_paid=?, deposit_paid=1, balance_paid=?, utr_number=?,
                submission_id=?, updated_at=?
            WHERE id=?
        """, (
            account["id"], total, int(is_balance), claim["utr_number"],
            claim["submission_id"], now, enrollment["id"],
        ))
    else:
        conn.execute("""
            INSERT INTO enrollments
            (intern_id, timestamp, name, email, phone, college, domain, payment_status,
             product, amount, amount_paid, deposit_paid, balance_paid, utr_number,
             submission_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Accepted', 'free_deposit', ?, ?, 1, 0, ?, ?, ?, ?)
        """, (
            account["id"], now, claim["full_name"], email, claim["phone"], claim["college"],
            claim["domain"], claim["amount"], total, claim["utr_number"],
            claim["submission_id"], now, now,
        ))
