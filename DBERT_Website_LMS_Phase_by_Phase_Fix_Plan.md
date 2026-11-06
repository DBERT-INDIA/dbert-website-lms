# DBERT Website & LMS — Phase-by-Phase Remediation and Fix Plan

**Repository:** [DBERT-INDIA/dbert-website-lms](https://github.com/DBERT-INDIA/dbert-website-lms)  
**Audit baseline:** `main` at `0e33ce86aad3959ea8578311f05147adaddd3bc2` (6 November 2026)  
**Related QA report:** `DBERT_Website_LMS_QA_Report_2026-11-06.pdf` / `.docx`  
**Document purpose:** Engineering implementation plan for closing the audit findings and obtaining a fresh release sign-off.  
**Status:** Proposed remediation plan — not a record of fixes already implemented.

---

## 1. Executive direction

The QA audit identified release-significant problems in authorization, payment reconciliation, enrollment persistence, password recovery, token lifecycle, data privacy, and production configuration. The first task is not to rewrite the platform. It is to establish which service actually owns each production workflow, close the security and financial-integrity defects, and then prove the repaired journeys on the exact release commit.

**Do not treat the 26 September 2026 release approval as current approval for the 6 November 2026 source tree.** The release artifact names an older verified commit (`cfc7e95`), whereas the reviewed `main` HEAD is `0e33ce86...` and includes later website, enrollment and deployment changes.

### Release decision

**Current status: NOT APPROVED for a new production release or new real-money payment flow until all P0 gates in this plan pass.**

This is a code-remediation recommendation. It is not a statement that every listed endpoint is currently exposed on the public production host. The repository's checked-in unified Nginx configuration shows three service paths:

| Host | Checked-in upstream | Application |
|---|---|---|
| `dbert.in` | `127.0.0.1:3001` | Next.js public website |
| `lms.dbert.in` | `127.0.0.1:5001` | Flask / Gunicorn LMS |
| `api.dbert.in` | `127.0.0.1:8000` | FastAPI REST API |

Confirm the actual deployed Nginx configuration, running processes, DNS and frontend API base URLs before assigning a defect to the live student path. Do not silently assume that the new FastAPI package has replaced the Flask LMS.

---

## 2. Severity and execution rules

- **P0 — release blocker:** student/applicant data exposure, broken session ownership, payment integrity, loss or false confirmation of enrollment/payment records, or unsafe production secrets.
- **P1 — must close before broad cohort use:** password recovery, token lifecycle, status consistency, mail delivery, persistence migration, tutor functionality and deployment correctness.
- **P2 — quality and operational hardening:** public-form abuse controls, UX, accessibility, monitoring, performance and documentation.

Implement each phase on a separate branch or pull request. A phase is not complete merely because code was changed. It is complete only when its tests pass, acceptance criteria are met, and evidence is attached to the pull request.

### Evidence required for every fix

1. Source diff and a short explanation of the defect.
2. Automated regression test that failed before the fix and passes after it.
3. Test output with commit SHA, environment and date.
4. For UI changes: desktop and mobile screenshots plus browser-console check.
5. For database changes: migration output, before/after row counts, constraints and rollback/restore evidence.
6. For payments: Razorpay test-mode order/payment IDs, webhook event IDs, database state and idempotency results. Never use real money for QA.

---

## 3. Finding-to-phase mapping

| Finding | Summary | Severity in QA report | Planned phase |
|---|---|---:|---|
| DBERT-001 | Application detail API has no authentication/ownership check | Critical | 2 |
| DBERT-002 | Learning-turn endpoint has no auth/session ownership check | Critical | 3 |
| DBERT-003 | Enrollment/application sync exception is swallowed | High | 6 |
| DBERT-004 | Website payment verification returns success despite DB update failure | Critical | 4 |
| DBERT-005 | Password reset does not enforce expiry or dispatch a token | High | 7 |
| DBERT-006 | FastAPI has known default signing/admin/cron secrets | Critical if deployed defaults are active | 8 |
| DBERT-007 | Website order amount is client-controlled | High | 4 |
| DBERT-008 | Payment is not strictly bound to its enrollment/order | High | 4 |
| DBERT-009 | FastAPI webhook records event but does not reconcile enrollment | High | 4 |
| DBERT-010 | Refresh permits token absent from server-side token store | Medium | 7 |
| DBERT-011 | Logout returns success without revoking the token | Medium | 7 |
| DBERT-012 | JSON balance-enrollment storage can lose/corrupt submissions | High | 5 |
| DBERT-013 | UTR submission is recorded as the full amount paid before verification | High | 5 |
| DBERT-014 | Public enrollment lookup exposes personal/payment data | High | 9 |
| DBERT-015 | Lookup inserts fallback certificate and intern IDs | Medium | 9 |
| DBERT-016 | Balance status values differ between submission and lookup | Medium | 9 |
| DBERT-017 | New guided-learning API returns a canned answer | High | 10 |
| DBERT-018 | SQLite remains an accepted runtime URL despite PostgreSQL-only claim | High | 8 |
| DBERT-019 | Email defaults do not match the mailer-only architecture claim | Medium | 8 |
| DBERT-020 | Public intake APIs have thin validation/abuse controls | Medium | 11 |
| ARCH-001 | Production source of truth is ambiguous | Architecture risk | 1 and 12 |
| ARCH-002 | Release evidence is stale relative to current HEAD | Architecture risk | 1 and 12 |
| ARCH-003 | Main branch protection/CI evidence is inadequate | Architecture risk | 12 |

---

# 4. Phase-by-phase implementation plan

## Phase 0 — Establish a reproducible baseline and protect production data

**Priority:** P0 foundation  
**Primary owner:** Tech lead / DevOps  
**Goal:** Know exactly what is running before changing code or data.

### Work items

1. Freeze the reviewed baseline SHA in the issue tracker and create a remediation branch, for example `qa/remediation-nov-2026`.
2. Capture the current production deployment state:
   - `nginx -T` output (redact host-specific secrets and certificates where appropriate).
   - Running systemd services and process commands for Flask, Next.js and FastAPI.
   - Listening ports and health endpoints.
   - Actual `.env` variable names and whether required values are present; never print or attach secret values.
   - Current DNS records and canonical redirects.
   - Current database engine, schema revision, backup status and upload directory/volume.
3. Draw a workflow ownership matrix. For every operation, name one authoritative backend and database:
   - application submit / review;
   - student login / sessions;
   - enrollment submit / approve;
   - Razorpay create / verify / webhook;
   - certificate issue / verify;
   - email and notification dispatch;
   - guided learning, assignments and progress.
4. Inspect website API calls and environment configuration to discover whether the browser calls Flask, FastAPI or Next.js route handlers for each workflow.
5. Take a verified database backup and test restoring it to an isolated staging database before schema migrations.
6. Establish synthetic test accounts: anonymous visitor, Student A, Student B, staff, mentor and admin. Do not use real student PII in test fixtures.

### Acceptance criteria

- A signed-off architecture map identifies the active service for every workflow.
- The exact production commit SHA and deployment configuration are recorded.
- A restorable backup exists and restore has been demonstrated.
- Test credentials are isolated from production accounts.
- No code or database migration begins until a rollback path is documented.

---

## Phase 1 — Stabilize service boundaries and API contracts

**Priority:** P0 foundation / P1 architecture  
**Primary owner:** Backend lead + frontend lead  
**Goal:** Stop maintaining multiple conflicting implementations of the same workflow without a contract.

### Work items

1. Decide whether the near-term LMS remains Flask (`apps/portal`) with FastAPI as a separate API, or whether a planned migration to FastAPI is actively underway. Record the decision in `docs/architecture.md`.
2. For each frontend workflow, define the canonical API base URL and route. Do not hardcode a mix of `lms.dbert.in`, `api.dbert.in`, old `internship.dbert.online` endpoints and same-origin Next.js routes without an explicit adapter.
3. Publish versioned request/response contracts for application, enrollment, payment, certificate and auth APIs. Include field types, status enums, amount units, error responses and retry semantics.
4. Normalize payment amount units. The website currently describes `amount` as paise, while the FastAPI order route multiplies its request amount by 100. Choose one contract (recommended: send a whole-rupee integer to an internal order service, convert to paise only at the Razorpay boundary) and reject ambiguous values.
5. Declare a single source of truth for payment and enrollment records. If Next.js temporarily owns a workflow, make it explicit and prohibit FastAPI/Flask from writing competing state for that same record.
6. Review Nginx variants: `deploy/dbert-unified-nginx.conf`, `deploy/dbert-website-nginx.conf` and `deploy/dbert-portal-nginx.conf`. Declare which file is active and remove or mark superseded examples clearly.

### Acceptance criteria

- One documented authoritative write path for each workflow.
- One documented API contract per workflow, including amount and status enums.
- Website-to-backend base URL is environment-driven and validated at startup.
- The active Nginx config matches the deployment runbook.
- Smoke tests verify that all links and redirects reach the intended service.

---

## Phase 2 — Fix application authorization and IDOR (DBERT-001)

**Priority:** P0 — release blocker  
**File:** `dbert-api-package/backend/api/v1/applications/router.py`  
**Goal:** Prevent anonymous and cross-user access to application records.

### Work items

1. Add an authentication dependency to `GET /api/v1/applications/{app_id}`.
2. Implement a centralized authorization helper rather than repeating ad-hoc checks:
   - admin/staff can access records within their permitted scope;
   - an applicant can access only their own application(s);
   - unrelated students, companies and mentors cannot access the record unless explicitly authorized by policy.
3. The current application submit schema is public and does not necessarily bind an application to a logged-in user. Do not assume email equality alone proves identity. For public applicants, issue a cryptographically random, high-entropy tracking token at submission, store only its hash, and use it for limited public status lookup. Do not expose a sequential database ID as a bearer credential.
4. Return a minimal public DTO for status tracking. Do not return phone, full email, CV, private answers, internal notes or admin-only fields.
5. Use a consistent 404 or 403 policy that does not reveal whether another person's application ID exists.
6. Apply the same policy to application attachments, CV links, exports and any route that accepts `app_id`.

### Regression tests

- Anonymous request to a private application: rejected.
- Student A requests Student B's application: rejected.
- Student A requests Student A's application: allowed only for permitted fields.
- Staff/admin access: allowed according to role.
- Random/expired tracking token: rejected.
- Sequential ID enumeration: reveals no private fields.

### Acceptance criteria

No unauthenticated route returns private applicant fields. Cross-account authorization tests pass for every application read/update path.

---

## Phase 3 — Fix learning-session authorization and ownership (DBERT-002)

**Priority:** P0 — release blocker  
**File:** `dbert-api-package/backend/api/v1/learning/router.py`  
**Goal:** A learner can read/write only their own learning sessions and turns.

### Work items

1. Add `current_user = Depends(require_intern)` to `POST /learning/v2/turn`.
2. After loading the session, compare `session.intern_id` with `int(current_user["sub"])`. Reject cross-user access with 403 or privacy-preserving 404.
3. Verify session status is `active` before accepting a new turn.
4. Apply equivalent ownership checks to session detail, session history, mastery/progress endpoints and concept/assignment endpoints where student-specific data is returned.
5. Validate message length, request shape and content type. Apply per-user rate limits and request IDs.
6. Keep turn insertion and mastery updates transactional. Do not award mastery merely because a request was submitted.

### Regression tests

- Anonymous turn submission: 401.
- Student A writes to A's session: success.
- Student A writes to B's session: 403/404.
- Closed session: rejected.
- Oversized/empty message: 422/400.
- Replayed request: no duplicate turn unless explicitly intended.

### Acceptance criteria

All learner session operations enforce authenticated ownership. Cross-user tests pass. Mastery is derived from a real assessment/evaluation result rather than a constant delta.

---

## Phase 4 — Make payments server-authoritative and transactionally reconcilable (DBERT-004, 007, 008, 009)

**Priority:** P0 — release blocker; highest financial risk  
**Files:**
- `apps/website/src/app/api/payments/create-order/route.ts`
- `apps/website/src/app/api/payments/verify/route.ts`
- `apps/website/src/app/api/payments/webhook/route.ts`
- `dbert-api-package/backend/api/v1/payments/router.py`
- `dbert-api-package/backend/services/razorpay_client.py`

**Goal:** Every captured payment is associated with the correct student, product, order and amount, and no API claims success before the result is durably recorded.

### 4.1 Order creation

1. Accept a trusted product/plan identifier and enrollment/application reference. Do not accept a trusted price from the browser.
2. Derive amount, currency, product and discount from a server-side catalogue/configuration. Validate eligibility and active pricing.
3. Create or reserve the local payment/enrollment record before returning an order to the browser. Persist the expected amount, currency, user/enrollment ID, product, and an idempotency key.
4. Call Razorpay with the server-calculated amount. Persist the returned Razorpay order ID against the same local payment record.
5. If Razorpay succeeds but local persistence fails, do not return a normal successful checkout response. Record an operational exception if possible, retry safely, and provide a controlled recovery path for the orphan order.
6. Set a unique constraint on the Razorpay order ID and local idempotency key.

### 4.2 Payment verification

1. Validate required payment fields and compare HMAC using a timing-safe comparison.
2. Load the local payment record by order ID. Confirm that:
   - the order exists locally;
   - the order belongs to the supplied enrollment/application;
   - the expected amount and currency match;
   - the payment ID has not already been applied to another transaction;
   - the payment is actually captured/authorized according to the selected gateway verification strategy.
3. Do not update an enrollment selected only by a client-supplied ID.
4. Update payment, enrollment and application states in one database transaction.
5. If persistence fails, return a non-success error or a specifically defined “payment received, confirmation pending” state only when the payment is independently verified and a durable retry/reconciliation record exists. Never return ordinary `success` while the only database write was swallowed.
6. Make verification idempotent: repeat the same valid callback without duplicating ledger entries or notifications.

### 4.3 Webhook processing

1. Verify the signature against the exact raw request body.
2. Use Razorpay's event identifier as the unique idempotency key. Do not substitute a generic request ID that can differ across retries.
3. Store event as `RECEIVED`/`PROCESSING`; process the payment/enrollment transition; set `PROCESSED` only after the business update commits.
4. Implement explicit handlers for captured, failed, refunded and other supported payment events.
5. Prevent stale/out-of-order `payment.failed` callbacks from downgrading a payment already marked captured/paid. Use a guarded state machine and gateway timestamps/status.
6. The FastAPI webhook currently only inserts a `PaymentEvent`; add the actual lookup and reconciliation for the matching payment/enrollment, or disable that endpoint until it is implemented.
7. For transient DB errors, return a retryable failure so the gateway retries, or place the verified event into a durable outbox before acknowledging it.

### 4.4 Financial audit trail

Maintain a payment ledger with at least: local payment ID, student/enrollment ID, product, order ID, payment ID, amount, currency, state, verification source, webhook event ID, created/updated timestamps, idempotency key and failure reason. Do not store API secrets in the ledger.

### Regression tests

- Tamper browser amount to ₹1: server still uses correct catalogue price or rejects.
- Use order A signature with enrollment B: rejected.
- Unknown enrollment/order: rejected; no success response.
- Valid payment + successful DB write: one paid transition.
- Valid payment + DB outage: no false success; recoverable reconciliation record.
- Duplicate verify callback: idempotent.
- Duplicate webhook: one state transition.
- Failed event after captured event: cannot downgrade paid state.
- Invalid webhook signature: 403/400; no DB mutation.
- Wrong currency/amount/order ID: rejected.

### Acceptance criteria

Payment amount is server-authoritative, each payment belongs to exactly one local enrollment, webhook effects are idempotent, and every success response is backed by durable records. All tests run using Razorpay test mode only.

---

## Phase 5 — Replace JSON balance-enrollment storage with PostgreSQL (DBERT-012, 013)

**Priority:** P0 — financial/data-integrity blocker  
**File:** `apps/website/src/app/api/enroll/balance/route.ts` and `apps/website/src/app/api/enroll/lookup/route.ts`  
**Goal:** Prevent lost UTR submissions and distinguish a claimed payment from a verified payment.

### Work items

1. Add a Prisma model/migration for balance-payment submissions. Suggested fields:
   - `id` (UUID or secure opaque ID);
   - `fullName`, normalized `email`, `phone`, `college`, `domain`;
   - `certificateId` / `internId` (nullable, validated against authoritative registry);
   - `utrNumberNormalized` with a database-level unique constraint;
   - `amountExpected`, `amountClaimed`, `amountVerified`;
   - `status` with one canonical enum: `SUBMITTED`, `UNDER_REVIEW`, `VERIFIED`, `REJECTED`;
   - `submittedAt`, `reviewedAt`, `reviewedBy`, `reviewNotes`;
   - `source`, `createdAt`, `updatedAt`.
2. Never populate `amountVerified` or mark a payment as paid solely because a user entered a UTR. A submission is a claim pending verification.
3. Normalize UTR before checking uniqueness. Enforce uniqueness in PostgreSQL, not only in application code.
4. Use a transaction for record creation and audit event. Handle duplicate UTR with a clear 409 response, not success for a previous user's record.
5. Add an authenticated admin review endpoint. Only authorized admins can move a record to VERIFIED/REJECTED. Store who reviewed it and when.
6. Stop writing new production submissions to `balance_enrollments_1500.json` after the migration is verified.
7. Backfill legacy JSON records into a staging table first. Generate a reconciliation report: source row count, imported row count, duplicate UTR count, malformed rows and mismatches. Review duplicates before production import.
8. Keep a read-only copy of the original JSON as a rollback artifact until post-migration validation is complete. Do not keep two writable sources.
9. Remove or redact full phone, email and UTR from operational text logs. Use opaque submission IDs and partial masking.

### Concurrency tests

- Submit two different UTRs simultaneously: both saved.
- Submit the same UTR simultaneously: exactly one record created; the other receives duplicate response.
- Database unavailable: API returns error; submission is not reported as saved.
- Invalid/corrupt legacy JSON: migration reports the error; it must not silently treat the source as an empty dataset.

### Acceptance criteria

No financial submission relies on local JSON file read-modify-write. Every submitted UTR starts pending, every verified amount has an auditable reviewer/source, and concurrent submission tests pass.

---

## Phase 6 — Make enrollment and application state changes atomic (DBERT-003)

**Priority:** P0/P1  
**File:** `dbert-api-package/backend/api/v1/enrollments/router.py`, plus application/enrollment state-machine services  
**Goal:** Enrollment, application status and their history records cannot disagree after a successful response.

### Work items

1. Remove the `except Exception: pass` block around `transition_application`.
2. Review intermediate `commit()` calls. The current route commits the enrollment before creating history and synchronizing the application. Refactor so all related writes occur within one transaction where possible.
3. Validate `application_id` exists and belongs to the same applicant (matching verified identity, not merely a client-supplied ID).
4. Validate requested product, amount, payment status and application state transition. Do not assume enrollment submission means payment accepted.
5. Define state transitions explicitly. Example:
   - application: `APPLIED -> UNDER_REVIEW -> SELECTED -> ENROLLED`;
   - enrollment: `DRAFT -> SUBMITTED -> PAYMENT_PENDING -> PAYMENT_VERIFIED -> CONFIRMED`;
   - manual UTR process: `SUBMITTED -> UNDER_REVIEW -> VERIFIED/REJECTED`.
   Adjust names to the existing business rules, but document one authoritative state graph.
6. Write history for every transition in the same transaction as the state change.
7. Use optimistic concurrency/version checks for admin review so two admins cannot silently overwrite each other's decisions.
8. Return structured errors with request/correlation ID. Log the underlying exception without exposing stack traces or PII to the user.

### Regression tests

- Valid enrollment with linked application: both transition and history created.
- Invalid application ID: no enrollment is persisted.
- Injected application transition failure: full transaction rolled back.
- Duplicate enrollment request: idempotent or rejected by business rule.
- Concurrent admin review: one valid transition; stale update rejected.

### Acceptance criteria

An API success means the enrollment, linked application state and audit history are all consistent. No broad exception suppression remains in this business flow.

---

## Phase 7 — Repair password reset, refresh and logout lifecycle (DBERT-005, 010, 011)

**Priority:** P1 — close before broad release  
**File:** `dbert-api-package/backend/api/v1/auth/router.py`, auth models and mailer service  
**Goal:** Password recovery and token revocation behave as advertised.

### Work items

1. **Forgot password:**
   - Generate a high-entropy, one-time token.
   - Store only a hash of the token if feasible; set a UTC expiry.
   - Dispatch a reset link through the approved DBERT Mailer, not a generic success message without actually sending.
   - Return the same generic response whether or not the account exists to prevent account enumeration.
   - Apply IP/email rate limits and audit events.
2. **Reset password:**
   - Query by token hash, `used = false` and `expires_at > now`.
   - Lock or atomically consume the reset token so two concurrent requests cannot both succeed.
   - Update the correct account table according to `account_type` (intern, company, mentor, staff if supported).
   - Invalidate outstanding sessions/refresh tokens after password change.
   - Enforce a reasonable password policy and reject weak/reused values according to policy.
3. **Refresh token:**
   - Require exactly one active, unexpired, non-revoked token record.
   - Reject unknown tokens; never generate a new token pair when the DB record is absent.
   - Use a generic token model for all roles or explicitly restrict this endpoint to interns. Current non-intern login routes must not issue refresh tokens that cannot be validated.
   - Rotate atomically: revoke old token and insert new token in the same transaction.
4. **Logout:**
   - Revoke the presented refresh token/session record.
   - If access-token revocation is required, maintain a denylist/session version or use appropriately short access-token TTL plus session revocation checks.
   - Do not return success unless the token/session was invalidated according to the contract.

### Regression tests

- Forgot password: message delivery success and failure are observable.
- Unknown email: no account enumeration.
- Expired token: rejected.
- Replayed token: rejected.
- Token for company/mentor: correctly supported or explicitly rejected.
- Refresh token not in DB: rejected.
- Revoked refresh token: rejected.
- Two simultaneous refresh calls: only one rotation succeeds.
- Logout followed by refresh: rejected.

### Acceptance criteria

A password reset works end-to-end through the configured mailer; expiry and replay checks pass; refresh and logout truly revoke sessions.

---

## Phase 8 — Harden production configuration, database policy and mail transport (DBERT-006, 018, 019)

**Priority:** P0 if defaults are deployed; otherwise P1  
**Files:**
- `dbert-api-package/backend/core/config.py`
- `dbert-api-package/backend/core/database.py`
- `dbert-api-package/.env.example`
- `dbert-api-package/docker-compose.yml`
- email service and deployment files

### Work items

1. Add a production configuration validator. When `ENVIRONMENT=production`, fail startup if:
   - `SECRET_KEY` is absent, too short or equal to any repository/template default;
   - admin credentials are defaulted or missing secure provisioning;
   - `CRON_SECRET` is missing/defaulted;
   - allowed CORS origins are wildcard when credentials are enabled;
   - payment secrets are missing while payments are enabled;
   - required mailer API credentials are absent while email is enabled.
2. Remove usable secret/password defaults from runtime code. Keep clearly fake placeholders only in `.env.example`, and ensure they cannot pass production validation.
3. Rotate any default credentials that may ever have been used in a reachable production deployment. Do not log secrets during diagnostics.
4. Enforce PostgreSQL-only runtime in production. If `ENVIRONMENT=production` and `DATABASE_URL` is SQLite, crash at startup. Allow SQLite only under an explicit `testing` environment if test fixtures require it.
5. Add database startup and readiness checks. `/health` should remain a liveness check; `/ready` should verify the database and critical dependencies without returning raw connection exception details to the public.
6. Reconcile email architecture. The QA release docs claim 100% DBERT Mailer usage, but FastAPI config defaults `EMAIL_PROVIDER=smtp` and includes SMTP settings. Choose the approved transport and either remove direct SMTP fallback or explicitly test and document a controlled fallback.
7. Ensure email failures are persisted and retried. Do not mark notifications as sent before delivery acceptance.
8. Review Docker Compose defaults and `.env.example`. Use strong generated local-only placeholders, required production environment injection and non-root containers where practical.

### Regression tests

- Production startup with missing/default SECRET_KEY: fails closed.
- Production startup with SQLite URL: fails closed.
- Testing environment with explicit SQLite: allowed only if intended.
- CORS rejects unapproved origins.
- Missing mailer API key with email enabled: visible readiness/startup error.
- Mailer timeout: queued retry/dead-letter with traceable error; no false sent state.

### Acceptance criteria

No known production secrets are accepted as defaults, no SQLite runtime is possible in production, and all outbound mail follows the documented and tested transport.

---

## Phase 9 — Protect certificate and enrollment lookup privacy/data correctness (DBERT-014, 015, 016)

**Priority:** P0/P1  
**Files:**
- `apps/website/src/app/api/enroll/lookup/route.ts`
- `apps/website/src/app/api/verify/route.ts`
- `apps/website/src/app/verify/directory/DirectoryClient.tsx`
- certificate registry data files and related admin flows

**Goal:** Public verification should prove credential authenticity without exposing unnecessary personal or payment data.

### Work items

1. Split certificate verification from enrollment/account lookup. These are different purposes and should not share one endpoint that returns a full candidate record.
2. Public certificate response should contain only the minimum intended public fields: certificate status, certificate ID, holder display name (subject to policy), program/domain, issue date and issuer. Never return phone, full email, UTR, payment details or private submission ID.
3. Do not allow email, phone or UTR as unrestricted public search keys for records containing personal/financial data. Require a secure candidate-specific verification mechanism for enrollment status.
4. Remove fabricated fallback IDs such as a hardcoded certificate ID or intern ID when source fields are missing. Return `null`/omit the field and report incomplete data internally.
5. Fix status enum mismatch. The submission route defines `VERIFIED`, while the lookup route checks `APPROVED`. Establish a single enum and migration mapping for legacy statuses.
6. Ensure `SUBMITTED`/`UNDER_REVIEW` never displays as approved or verified. Provisional certificates must be labelled provisional in both API and UI.
7. Validate that static registries and database records are reconciled. Avoid multiple independent registries that disagree on whether a certificate is valid.
8. Ensure directory search is limited to approved public fields and does not serialize hidden candidate contact data into client props.
9. Add cache policy suitable for personal data. Public credential status may be cached briefly; authenticated enrollment data must not be shared-cacheable.

### Regression tests

- Lookup by known email does not expose phone/UTR.
- Lookup by UTR does not expose another candidate's details.
- Pending record is not shown as verified.
- Missing certificate ID stays missing; no default IDs appear.
- `VERIFIED` state is recognized consistently.
- Provisional, revoked, corrected and unknown certificate states render correctly.

### Acceptance criteria

Public certificate verification reveals only approved fields. No endpoint returns raw UTR or full applicant contact details to an anonymous caller. All status values are canonical and tested.

---

## Phase 10 — Repair guided learning and disable misleading behavior until complete (DBERT-017)

**Priority:** P1  
**File:** `dbert-api-package/backend/api/v1/learning/router.py` and learning service layer  
**Goal:** The tutor must either deliver a real response or clearly report that the feature is unavailable; it must not simulate progress.

### Work items

1. The current `/learning/v2/turn` returns a fixed sentence about production microservices regardless of the learner's message. Replace it with the intended tutor/service integration and course-context retrieval.
2. If AI integration/RAG is not ready, disable the endpoint or return a clear `feature_unavailable` response. Do not fake an AI answer.
3. Connect the tutor to the correct course/concept material. Persist model/provider, prompt version, retrieved source IDs and response metadata where appropriate for audit/debugging.
4. Do not award constant `mastery_delta=0.1`. Mastery must be computed by a defined rubric/assessment and stored transactionally.
5. Add provider timeout, rate-limit and quota handling. Return a recoverable user message, retain the learner's unsent input where safe, and log the provider error with a request ID.
6. Apply the Phase 3 ownership restrictions and ensure the turn endpoint has no way to access another learner's context.

### Regression tests

- Different questions produce relevant, context-grounded responses or a clear disabled response.
- Provider timeout/quota: no fabricated answer or fake mastery increment.
- RAG source unavailable: fallback behavior is explicit and logged.
- Session ownership tests pass.
- Turn save failure: response does not claim the turn was saved.

### Acceptance criteria

No canned response is presented as a live AI tutor answer. No mastery is awarded without evidence from the scoring logic.

---

## Phase 11 — Harden public website forms and intake APIs (DBERT-020)

**Priority:** P2/P1 depending on exposure  
**Files:**
- `apps/website/src/app/api/cohorts/apply/route.ts`
- `apps/website/src/app/api/contact/route.ts`
- `apps/website/src/app/api/demo-request/route.ts`
- `apps/website/src/app/api/consultation/route.ts`
- `apps/website/src/app/api/startups/register/route.ts`

### Work items

1. Validate request body type/size before field validation. Reject malformed JSON, arrays where objects are expected and oversized payloads.
2. Normalize email, phone and URLs. Validate maximum lengths and reject control characters or unexpected objects.
3. Apply IP and per-email rate limits. Add bot mitigation (honeypot, Turnstile or equivalent) where appropriate, without blocking accessibility users.
4. Confirm that the form's required fields match server requirements. Do not require family background or other sensitive/nonessential fields unless there is a clear business and privacy basis.
5. Validate consent server-side and store its version/timestamp. Do not treat a truthy arbitrary string as sufficient consent.
6. Avoid returning internal exception messages. Use stable error codes that the frontend can display with a recovery action.
7. Add duplicate submission handling using a unique idempotency key or a carefully chosen duplicate-detection rule.
8. Add retention and deletion policy for contact, CV and cohort data. Restrict admin export access and log downloads.

### Acceptance criteria

Abuse tests are rate-limited; malformed data is rejected; valid submissions are saved once; forms show actionable errors; PII has a defined access/retention policy.

---

## Phase 12 — Add CI, full regression testing, staging UAT and final release gate

**Priority:** P0/P1 release gate  
**Owners:** QA lead + all engineering owners  
**Goal:** Replace historical self-reported sign-off with repeatable evidence on the exact deployment commit.

### 12.1 CI requirements

Create GitHub Actions workflows if none are configured. Require these checks on every pull request to `main`:

**Website (`apps/website`):**

```bash
npm ci
npm run lint
npm run build
```

Also run TypeScript checking explicitly if it is not already enforced during build:

```bash
npx tsc --noEmit
```

**Flask LMS (`apps/portal`):**

```bash
python -m pip install -r requirements.txt
pytest -q
```

Use the actual portal requirements filename verified in the repo and provision the expected test database/services in CI. Do not run tests against production data.

**FastAPI (`dbert-api-package`):**

```bash
python -m pip install -r backend/requirements.txt
pytest -q
```

Add a dedicated API test suite if the package currently has no maintained test suite. Include auth, IDOR, state transitions, payment, webhook, password reset and migration tests.

**Deployment/static checks:**

- Validate Nginx config syntax in a staging/container job.
- Build Docker image.
- Check for secrets in tracked files and accidental `.env` commits.
- Check migrations apply to a disposable PostgreSQL database and rollback/restore is documented.
- Fail the pipeline on lint, type, test, migration or security failures.

### 12.2 Browser end-to-end acceptance matrix

Run the cases below using synthetic accounts and Razorpay test mode. Capture request IDs, response codes, DB results and screenshots.

| Test | Journey | Pass criteria | Gate |
|---|---|---|---|
| QA-01 | Public website pages and navigation | No 5xx, blank sections, broken primary links or console errors | P1 |
| QA-02 | Legacy domain redirects | One canonical redirect; path/query retained; no loop | P1 |
| QA-03 | Student login/logout/session | Login, refresh and logout are consistent; protected pages stay protected | P0 |
| QA-04 | Multi-step signup | Progress persists; duplicate email handled; validation actionable | P1 |
| QA-05 | Application submit/review | Correct application and history records; admin decisions persist | P1 |
| QA-06 | Application IDOR | Anonymous and Student A cannot read Student B's private data | P0 |
| QA-07 | Admin review | Only permitted roles see/modify queue; history and notification match | P1 |
| QA-08 | Payment tampering | Client amount/order/enrollment changes are rejected | P0 |
| QA-09 | Payment + database outage | No false success; verified payment reconciles after recovery | P0 |
| QA-10 | Failed/late/duplicate webhook | Idempotent; paid state cannot be downgraded by stale failure | P0 |
| QA-11 | UTR submission and review | Pending until verified; concurrent writes do not lose records | P0 |
| QA-12 | Password recovery | Email received; expired and replayed tokens rejected | P1 |
| QA-13 | Learning isolation | No anonymous/cross-user session access; tutor answer is real or explicitly disabled | P0 |
| QA-14 | Tasks and uploads | Ownership, file validation and task state transitions work | P1 |
| QA-15 | Certificate issue/verify | Correct state and candidate; no fabricated IDs or private data | P1 |
| QA-16 | Transactional email | Correct recipient/template; retries and failures observable | P1 |
| QA-17 | Responsive/accessibility | Mobile, tablet, keyboard and error states usable | P2 |
| QA-18 | Operational recovery | DB/provider outage produces unhealthy readiness, logs and recovery | P1 |

### 12.3 Staging UAT

1. Deploy the release candidate to staging using production-like Nginx, database, mailer and environment configuration.
2. Use test-mode payment credentials only.
3. Run all QA-01 through QA-18 cases.
4. Test from a network that can resolve the real domains and confirm external DNS/TLS/redirects.
5. Test with realistic but synthetic cohort data and concurrent form submissions.
6. Verify backup and restore, upload persistence, log rotation and restart recovery.
7. Fix every P0 and P1 issue. Retest the full impacted workflow, not only the changed function.

### 12.4 Release gate

A release can be approved only when all of the following are true:

- DBERT-001, DBERT-002 and DBERT-004 are fixed and security regression tests pass.
- DBERT-007, DBERT-008 and DBERT-009 are fixed and payment sandbox cases pass.
- DBERT-003, DBERT-012 and DBERT-013 are fixed and enrollment/data-integrity tests pass.
- DBERT-014 through DBERT-016 are fixed and public privacy/status tests pass.
- DBERT-005, DBERT-006, DBERT-010 and DBERT-011 are fixed or explicitly disabled by a documented secure policy.
- DBERT-018 and DBERT-019 are resolved for the active runtime.
- Active website/LMS/API routing is documented and matches production.
- Required CI checks are green and `main` branch protection is enabled.
- Fresh UAT is complete against the same SHA that will be deployed.
- Restore drill, monitoring and rollback have been demonstrated.
- QA and engineering sign off with commit SHA, evidence links and known residual risks.

---

# 5. Suggested pull-request sequence

Use small, reviewable PRs. Do not combine payment redesign, database migration and UI redesign in one large change.

| PR | Scope | Must depend on |
|---|---|---|
| PR-00 | Baseline evidence, architecture map, protected remediation branch | None |
| PR-01 | API contract and active-service ownership documentation | PR-00 |
| PR-02 | Application authorization + IDOR tests | PR-01 |
| PR-03 | Learning session authorization + ownership tests | PR-01 |
| PR-04 | Payment service, order binding, webhook reconciliation and sandbox tests | PR-01 |
| PR-05 | Balance enrollment DB schema, backfill and admin verification | PR-01; coordinate with PR-04 |
| PR-06 | Atomic enrollment/application transitions | PR-01 and schema agreement |
| PR-07 | Password reset, refresh rotation and logout revocation | PR-01 |
| PR-08 | Production config validation, Postgres-only guard and mail transport | PR-00 |
| PR-09 | Lookup privacy, certificate status and registry cleanup | PR-01 and PR-05 |
| PR-10 | Real tutor integration or disablement; no fake mastery | PR-03 |
| PR-11 | Public form validation, abuse protection and consent | PR-01 |
| PR-12 | CI, staging UAT, release gate and deployment runbook | All applicable PRs |

---

# 6. Rollback and data migration strategy

### Code rollback

- Keep each phase deployable as a discrete commit/PR.
- Tag the last known-good deployment before release.
- Keep the previous Nginx/systemd configuration and application artifact available until smoke tests pass.
- Do not rollback a database schema destructively just because an application deployment failed. Use backward-compatible expand/contract migrations.

### PostgreSQL migration for balance submissions

1. Create the new table and indexes without deleting the old JSON file.
2. Backfill into staging; generate row-count and duplicate reports.
3. Validate sample records against the source and resolve duplicate UTRs.
4. Deploy dual-read or controlled read compatibility only if necessary; do not allow two writable sources for long.
5. Switch writes to PostgreSQL.
6. Compare totals and admin queue results.
7. Make JSON read-only and retain it securely as a rollback artifact.
8. After the agreed retention window and verified backups, remove legacy file reads/writes in a later release.

### Payment recovery

- Never delete payment events or ledger rows during rollback.
- If the application is rolled back, retain the reconciliation worker/data model so captured payments can still be mapped to enrollments.
- Reconcile unknown/orphaned Razorpay orders from gateway records before reopening checkout.

---

# 7. Operational monitoring after release

Track and alert on:

- payment order created but no local payment row;
- captured payment with enrollment still pending;
- duplicate/replayed webhook count;
- payment amount/order/enrollment mismatch;
- pending UTR submissions older than the review SLA;
- enrollment/application state mismatch;
- login failures, refresh failures and password reset failures;
- cross-user authorization denials and abnormal ID enumeration;
- email outbox age, retries and dead-letter count;
- database readiness and connection pool failures;
- API 4xx/5xx rate, p95 latency and frontend route errors.

Every operational event should contain a correlation/request ID and opaque record ID. Do not place passwords, tokens, full UTRs, CV contents or unnecessary PII in logs.

---

# 8. Definition of done

The remediation project is done when:

1. Each P0/P1 finding has a linked fix PR and a regression test.
2. All 18 QA journeys pass on staging.
3. Payment, enrollment, certificate, identity and student-session states are consistent across the authoritative database and all user-facing views.
4. No critical or high finding remains open without an explicitly accepted risk owner and mitigation.
5. The production deployment SHA is the same SHA that passed UAT.
6. A rollback and database restore are proven.
7. QA, engineering and operations approve the release with evidence.

**Final principle:** a successful HTTP response is not proof that a business transaction succeeded. A user-facing success message must correspond to a durable, authorized and auditable state change.

---

## 9. Source files to review while implementing

- [Application router](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/dbert-api-package/backend/api/v1/applications/router.py)
- [Enrollment router](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/dbert-api-package/backend/api/v1/enrollments/router.py)
- [Learning router](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/dbert-api-package/backend/api/v1/learning/router.py)
- [FastAPI payment router](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/dbert-api-package/backend/api/v1/payments/router.py)
- [FastAPI auth router](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/dbert-api-package/backend/api/v1/auth/router.py)
- [FastAPI configuration](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/dbert-api-package/backend/core/config.py)
- [FastAPI database setup](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/dbert-api-package/backend/core/database.py)
- [Website order creation](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/apps/website/src/app/api/payments/create-order/route.ts)
- [Website payment verification](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/apps/website/src/app/api/payments/verify/route.ts)
- [Website payment webhook](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/apps/website/src/app/api/payments/webhook/route.ts)
- [Balance enrollment submission](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/apps/website/src/app/api/enroll/balance/route.ts)
- [Balance enrollment lookup](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/apps/website/src/app/api/enroll/lookup/route.ts)
- [Certificate verification API](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/apps/website/src/app/api/verify/route.ts)
- [Unified Nginx configuration](https://github.com/DBERT-INDIA/dbert-website-lms/blob/0e33ce86aad3959ea8578311f05147adaddd3bc2/deploy/dbert-unified-nginx.conf)
- [Existing QA/release artifacts](https://github.com/DBERT-INDIA/dbert-website-lms/tree/0e33ce86aad3959ea8578311f05147adaddd3bc2/.agent)

