# End-to-End User Journeys Report

**Date:** 2026-09-26  
**Project:** DBERT LMS  
**Target:** 15-Step Golden Applicant Lifecycle & 5-Stage User Workflows

---

## 1. Journey Steps & Lifecycles Verified

- **15-Step Golden Applicant Journey (`tests/test_golden_journey.py`):**
  1. Public Discovery (`/`, `/jobs`, `/internships`)
  2. Account Registration (`/signup/stage1`)
  3. SOP Submission (`/apply`)
  4. Authentication & Session Cookie issuing
  5. Portal Status View (`/portal` Under Review)
  6. Admin Review & Selection (`STATUS_UNDER_REVIEW` $\to$ `STATUS_SELECTED`)
  7. Selection View & Payment Unlock
  8. Enrollment & Receipt Submission (`/enroll`)
  9. Payment Acceptance & Application Approval (`STATUS_ACCEPTED`)
  10. Active Internship & Domain Course Auto-Enrollment
  11. Task Exploration & Capstone Assignment View
  12. Task Solution Submission (`/tasks/submit`)
  13. Mentor/Staff Capstone Evaluation & Coin Awarding
  14. Certificate Issuance (`intern_certificates`)
  15. Public Certificate Verification (`/portal/certificate/<cert_id>`)

- **5-Stage Lifecycle Workflows (`tests/test_5_stage_lifecycle.py`):**
  - Verified user stage transitions (`STAGE_APP_REQUIRED` $\to$ `STAGE_UNDER_REVIEW` $\to$ `STAGE_SELECTED` $\to$ `STAGE_PAYMENT_PENDING` $\to$ `STAGE_CONFIRMED`).

---

## 2. Test Verification Summary

- **E2E Golden Journey & Lifecycle Test Suite:** **5 passed in 2.38s**.
