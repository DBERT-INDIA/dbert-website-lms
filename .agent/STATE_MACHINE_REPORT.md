# Application & Enrollment State Machines Report

**Date:** 2026-09-26  
**Project:** DBERT LMS  
**Target:** State Machine Graph & Status Transition Validation

---

## 1. State Machine Invariants

- **Application State Machine (`services/application_service.py`):**
  - Canonical Statuses: `Apply Pending`, `Under Review`, `On Hold`, `Selected`, `Enrollment Pending`, `Enrolled`, `Accepted`, `Rejected`, `Paid-Enrolled`.
  - Enforces explicit permitted transition paths (`VALID_APP_TRANSITIONS`), actor role permissions (`INTERN`, `MENTOR`, `ADMIN`), optimistic concurrency control (`version` column), and event outbox notifications on state change.
- **Enrollment State Machine (`services/enrollment_service.py`):**
  - Canonical Statuses: `pending`, `active`, `completed`, `dropped`, `refunded`, `cancelled`.
  - Enforces explicit transition graphs and zero-row error protection.

---

## 2. Test Verification Summary

- **State Machine Test Suites (`tests/test_application_state_machine.py`, `tests/test_enrollment_state_machine.py`):**
  - Valid transition execution & audit logging.
  - Invalid transition block.
  - Role-based transition authorization.
  - Zero-row / Non-existent record protection.
- **Pass Status:** `14 passed in 0.06s`.
