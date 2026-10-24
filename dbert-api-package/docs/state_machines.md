# DBERT State Machine Specifications

This document defines the strict finite state machines governing Applications and Enrollments, ported directly from `services/application_service.py` and `services/enrollment_service.py`.

---

## 1. Application State Machine

### 1.1 Valid Statuses
- `Apply Pending`: Initial state when user completes stage 1/2/3 signup or submits raw application.
- `Under Review`: Staff or mentor reviewing profile and test/interview results.
- `On Hold`: Applicant requires further information or cooling window.
- `Selected`: Applicant cleared interview and is approved for enrollment.
- `Enrollment Pending`: Offer extended; waiting for deposit / enrollment confirmation.
- `Enrolled`: Security deposit or fee received; active intern onboarding.
- `Accepted`: Fully verified and placed into team/batch.
- `Rejected`: Application denied.
- `Paid-Enrolled`: Parallel direct-paid track (₹1599).

### 1.2 Transition Matrix
```
Apply Pending ──> Under Review ──> Selected ──> Enrollment Pending ──> Enrolled ──> Accepted
      │                 │               │               │                  │
      └──> Rejected     └──> On Hold    └──> Rejected   └──> Rejected      └──> Rejected
                              │
                              └──> Selected / Rejected
```

### 1.3 Transition Rules
1. Any transition must record an audit entry in `application_status_history` (`app_id`, `old_status`, `new_status`, `changed_by`, `reason`, `created_at`).
2. Concurrent modifications must be prevented via versioning / optimistic locking (`updated_at` check).
3. Max 3 active applications per person (`MAX_APPLICATIONS_PER_PERSON`).

---

## 2. Enrollment State Machine

### 2.1 Valid Statuses
- `Pending Review`: Deposit proof or payment received, awaiting admin verification.
- `Verified`: Payment verified by admin or Razorpay webhook.
- `Active`: Intern actively attending and participating.
- `Completed`: Intern successfully completed program and tasks.
- `Refunded`: Security deposit returned after program completion.
- `Forfeited`: Intern violated terms / dropped out without notice.
- `Rejected`: Deposit proof invalid or duplicate.

### 2.2 Transition Rules
1. State changes are audited in `enrollment_status_history`.
2. Financial reconciliation updates both `enrollments` and `security_deposits` tables.
