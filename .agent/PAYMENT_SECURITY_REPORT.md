# Payment Security & State Machine Report

**Date:** 2026-09-26  
**Project:** DBERT LMS  
**Target:** Server-Authoritative Pricing & Razorpay Signature Verification

---

## 1. Security Invariants Verified

- **Server-Authoritative Pricing:** Enforced in `services/payment_service.py` (`determine_pricing`). Client-supplied amounts are ignored; prices are resolved server-side based on `product_type` and database course entries.
- **HMAC Signature Verification:** Timing-safe signature checks (`verify_payment_signature` and `verify_webhook_signature`) via `services/razorpay_client.py`.
- **Payment Idempotency:** Recorded in `payment_events` table (`is_payment_processed`). Replayed order verifications are safely detected and rejected.

---

## 2. Test Verification Summary

- **Payment Security Test Suite (`tests/test_payment_razorpay.py`):**
  - Server-authoritative pricing validation.
  - Razorpay order creation and receipt generation.
  - Invalid signature rejection.
  - Webhook signature authentication.
  - Replay prevention.
- **Pass Status:** `11 passed in 0.80s`.
