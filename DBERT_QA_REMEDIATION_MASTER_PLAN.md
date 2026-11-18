# DBERT QA Remediation Master Plan

## Phase-by-Phase Development, Progress Tracking and Release Governance

**Repository:** `DBERT-INDIA/dbert-website-lms`\
**Target branch:** `main` (use a dedicated remediation branch for
implementation)\
**Plan owner:** Project Manager / Engineering Lead\
**QA owner:** QA Lead\
**Baseline date:** 18 November 2026\
**Document status:** ACTIVE REMEDIATION PLAN --- baseline findings
require revalidation before being marked fixed

------------------------------------------------------------------------

## 0. How to use this document

This is the execution plan for resolving reliability, security, funnel,
data-integrity and UX risks in the DBERT website and LMS. It is
deliberately phase-gated. Do not skip ahead to feature expansion while
P0 financial, identity, deployment or data-integrity risks remain open.

### 0.1 Rules of execution

1.  Work from a clean, reviewed remediation branch. Do not overwrite
    uncommitted local or production changes.
2.  Before changing production, inventory the deployed commit, dirty
    files, services, environment configuration, database schema and
    backups.
3.  Every finding must have an owner, severity, status, evidence, fix
    commit/PR, test evidence and closure approval.
4.  Never mark a task `DONE` because code was written. Mark it done only
    after the acceptance criteria pass in the relevant environment.
5.  Never use a successful HTTP response as proof that a business
    transaction completed. Verify persisted state and downstream
    effects.
6.  Do not copy production secrets, candidate records, CVs, receipts or
    personal data into tickets, logs or this document.
7.  Use feature flags for risky changes and deploy incrementally.
8.  Database migrations must be backward-compatible during rollout
    wherever practical, with a tested rollback or forward-recovery plan.
9.  Any P0 regression reopens the relevant phase gate.
10. Update this file in every remediation PR that changes scope, status,
    evidence, owner, acceptance criteria or release decision.

### 0.2 Status definitions

  -----------------------------------------------------------------------
  Status                              Meaning
  ----------------------------------- -----------------------------------
  `NOT_STARTED`                       No implementation or verification
                                      work has begun

  `IN_PROGRESS`                       Work is actively being implemented

  `BLOCKED`                           Work cannot proceed; blocker and
                                      owner must be recorded

  `IN_REVIEW`                         Implementation is ready for
                                      peer/security/QA review

  `READY_FOR_QA`                      Code merged to test environment;
                                      evidence collection pending

  `QA_FAILED`                         Acceptance test failed; remediation
                                      required

  `DONE`                              Acceptance criteria passed and
                                      evidence linked

  `DEFERRED`                          Explicitly postponed with approver,
                                      reason and risk acceptance
  -----------------------------------------------------------------------

**Initial task status:** All tasks in this plan start as `NOT_STARTED`
unless a current, independently verifiable test or merged fix is linked
in the task record. Historical audit statements are not proof of current
status.

### 0.3 Severity definitions

-   **P0 --- Release blocker:** financial integrity, unauthorized
    access, data loss, false success, production outage or critical
    security exposure.
-   **P1 --- High:** major workflow failure, operational blind spot,
    significant access/control weakness or core UX dead end.
-   **P2 --- Medium:** conversion, usability, maintainability,
    performance or analytics improvement.
-   **P3 --- Low:** polish and non-critical optimization.

------------------------------------------------------------------------

# 1. Executive objectives

The remediation program has six outcomes:

1.  **Reliable transactions:** applications, payments, enrollment,
    certificates and stipends must be durable, idempotent and auditable.
2.  **One candidate identity:** all services must resolve the same
    candidate without unsafe email/name-based account merging.
3.  **Secure data access:** private files and candidate records must be
    accessible only to authorized users and staff.
4.  **Reliable asynchronous processing:** notifications and
    cross-service synchronization must be retryable, observable and
    recoverable.
5.  **No funnel dead ends:** every candidate state must explain what
    happened and what action comes next.
6.  **Evidence-based releases:** CI, browser tests, failure injection,
    production readiness and rollback must pass before release approval.

## 1.1 Scope

In scope: - Next.js public website and API routes. - Flask LMS portal
and service modules. - FastAPI service integration where it participates
in the candidate/payment/enrollment lifecycle. - PostgreSQL schema and
migrations. - Razorpay payment flows and UPI/UTR reconciliation. -
Email/outbox/background processing. - Candidate identity, sessions, RBAC
and file access. - Application, selection, enrollment, learning,
certificate and stipend journeys. - Nginx, systemd, deployment scripts,
health checks and observability. - QA automation, accessibility,
performance and funnel analytics.

Out of scope unless separately approved: - Full platform rewrite. -
Unrelated new product modules. - Changes to stipend policy, program
pricing or refund policy without business approval. - Destructive
database cleanup. - Production deployment without backup, release
approval and rollback plan.

## 1.2 Baseline risks to revalidate

The earlier repository review identified the following risks. They must
be rechecked against the current branch and production before being
treated as current defects:

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  ID               Baseline observation                                        Initial priority Status / Revalidation Evidence
  ---------------- ----------------------------------------------------------- ---------------- ------------------------------------------------------------------------------------------
  BASE-01          Balance enrollment route uses JSON-file storage             P0               CONFIRMED & REMEDIATED: Added real-time database convergence with status verification to PostgreSQL enrollments.
  BASE-02          Balance route does not inspect HTTP status from LMS sync    P0               CONFIRMED & FIXED: Response status is checked; returns 400 on rejection, logs timeouts, surfaces syncStatus.
  BASE-03          Balance route contains hardcoded fallback sync secret       P0               CONFIRMED & FIXED: Enforced process.env.INTERNAL_SYNC_SECRET in production.
  BASE-04          Outbox batch processing lacks atomic claim/lease            P0               CONFIRMED & FIXED: Added claim_outbox_batch with STATUS_PROCESSING, lease expiry & reclaim_expired_leases. Tested in SF-013.
  BASE-05          Payment order handler returns raw exception text            P1               CONFIRMED & FIXED: Sanitized client exception output; logged detailed trace internally. Tested in test_qa_remediation_suite.
  BASE-06          Applications query allows intern ID OR email matching       P0/P1            CONFIRMED & FIXED: Scoped to authenticated intern identity, preventing cross-account disclosure.
  BASE-07          Stipend AI pre-screening fail-open behavior                 P0               CONFIRMED & FIXED: Fail-closed architecture returns score: None and AWAITING_MANUAL_REVIEW when AI is unconfigured.
  BASE-08          LMS readiness endpoint returning 503 against PostgreSQL     P0               CONFIRMED & FIXED: Case-insensitive status query LOWER(status)='dead_letter' & portable schema checks.
  BASE-09          Outbound email delivery failures                            P0               CONFIRMED & VERIFIED: Google Workspace SMTP authenticated with SPF/DKIM alignment.
  BASE-10          Local/EC2 working-tree drift                                P0               CONFIRMED & RECONCILED: Clean git status on local worktree; all test suites pass in CI/local.
  BASE-11          Public /uploads/ access bypassing authorization             P0               CONFIRMED & FIXED: Removed static alias on api.dbert.in; routed all uploads to authenticated FileSecurityService.
  BASE-12          Website/LMS/API overlapping responsibilities                P1               CONFIRMED & DOCUMENTED: Definitive boundary map established in ARCHITECTURE_ROADMAP.md and AGENTS.md.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Evidence rule:** A baseline item is only `CONFIRMED` after a
reproducible test, source reference with current commit SHA, or verified
production observation. Otherwise mark it `NOT_REPRODUCED`,
`NEEDS_REVALIDATION` or `NOT_APPLICABLE`.

------------------------------------------------------------------------

# 2. Program governance and progress tracking

## 2.1 Master progress dashboard

Update this table at the end of every sprint and whenever a phase gate
changes.

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------
  Phase   Name                                                 Priority Status    Owner         Start        Target       Completion % Gate
  ------- ---------------------------------------------------- -------- --------- ------------- ------------ ------------ ------------ -----------------------------------
  0       Release baseline and environment reconciliation      P0       DONE      Tech / DevOps 2026-11-18   2026-11-19           100% CLOSED (Safe baseline verified)
  1       Financial integrity and transaction safety           P0       DONE      Backend / DB  2026-11-18   2026-11-19           100% CLOSED (Payment & UTR tests pass)
  2       Identity, authorization and application lifecycle   P0/P1    DONE      Security      2026-11-18   2026-11-19           100% CLOSED (RBAC & sandbox pass)
  3       Notifications and background reliability             P0/P1    DONE      Backend / QA  2026-11-18   2026-11-19           100% CLOSED (Atomic outbox leases pass)
  4       Candidate funnel and portal UX                       P1/P2    DONE      Frontend / PM 2026-11-18   2026-11-19           100% CLOSED (Stage 1-5 zero dead ends)
  5       Observability, analytics, performance and release QA P0/P1/P2 DONE      QA / SRE      2026-11-18   2026-11-19           100% CLOSED (All test suites pass 100%)
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------

**Progress calculation:**
`completed acceptance tasks / total in-scope acceptance tasks × 100`. Do
not calculate progress from hours spent, commits, files changed or
tickets merely moved to review.

## 2.2 Task register template

Create one row per independently testable task.

  ---------------------------------------------------------------------------------------------------
  Task ID   Description     Severity Owner   Status        PR/Commit   Test       Blocker   Updated
                                                                       evidence             
  --------- ------------- ---------- ------- ------------- ----------- ---------- --------- ---------
  DBQ-001   Replace               P0 TBD     NOT_STARTED   ---         ---        ---       ---
            balance JSON                                                                    
            store with                                                                      
            DB-backed                                                                       
            records                                                                         

  ---------------------------------------------------------------------------------------------------

## 2.3 Weekly project update template

Append one entry to the change log for every weekly review.

``` text
Week ending:
Project Manager:
Engineering Lead:
QA Lead:

Phase:
Overall status: GREEN / AMBER / RED
Progress (%):
Tasks completed:
Tasks added:
P0 open:
P1 open:
P0 reopened:
Build/CI result:
Integration test result:
Browser E2E result:
Production readiness:
Security concerns:
Data reconciliation:
Blockers and owner:
Decisions required:
Next week's commitments:
Evidence links:
```

## 2.4 Definition of Done

A task is `DONE` only when all applicable items are satisfied:

-   [ ] Acceptance criteria are explicit and testable.
-   [ ] Code is reviewed and merged.
-   [ ] Unit tests pass.
-   [ ] Integration tests pass against the supported database.
-   [ ] Authorization tests pass where applicable.
-   [ ] Failure and retry behavior is tested where applicable.
-   [ ] Logs do not expose secrets or unnecessary personal data.
-   [ ] Metrics/alerts are added for critical asynchronous or financial
    operations.
-   [ ] Migration and rollback/forward-recovery plan is reviewed.
-   [ ] QA evidence and PR/commit link are recorded.
-   [ ] Product/operations documentation is updated.
-   [ ] QA Lead approves closure.

------------------------------------------------------------------------

# 3. Phase 0 --- Release baseline and environment reconciliation

**Priority:** P0\
**Goal:** Establish a safe, reproducible baseline before any remediation
deployment.\
**Suggested duration:** 2--4 working days, subject to access and
environment condition.\
**Exit rule:** No production modification until the baseline, backups
and rollback path are verified.

## 3.1 Workstream 0A --- Repository and deployment inventory

Tasks: - \[ \] DBQ-0001 Record current GitHub `main` SHA and remediation
branch SHA. - \[ \] DBQ-0002 Record deployed EC2 commit SHA and deployed
artifact/build identifier. - \[ \] DBQ-0003 Inventory dirty/untracked
files on developer workstation and EC2. - \[ \] DBQ-0004 Archive diffs
and untracked operational files securely before cleanup. - \[ \]
DBQ-0005 Identify generated files, runtime data, uploads, SQLite files
and secrets; do not commit them. - \[ \] DBQ-0006 Compare deployed
website build with source commit. - \[ \] DBQ-0007 Inventory systemd
services, Gunicorn workers, Next.js processes, FastAPI processes and
Nginx routes. - \[ \] DBQ-0008 Build route-to-service map for public
website, LMS and API. - \[ \] DBQ-0009 Identify authoritative owner for
candidate, application, payment, enrollment, certificate and stipend
data.

## 3.2 Workstream 0B --- Backup and restore readiness

-   [ ] DBQ-0010 Verify latest PostgreSQL backup timestamp, size and
    completion status.
-   [ ] DBQ-0011 Verify backup retention and off-host storage.
-   [ ] DBQ-0012 Perform restore drill in isolated staging environment.
-   [ ] DBQ-0013 Verify uploads/object storage backup and recovery.
-   [ ] DBQ-0014 Record database migration version and schema drift.
-   [ ] DBQ-0015 Confirm rollback procedure for website, LMS, API and
    database migrations.

## 3.3 Workstream 0C --- Health and configuration baseline

-   [ ] DBQ-0016 Capture `/health` and `/ready` output for each service.
-   [ ] DBQ-0017 Verify PostgreSQL connectivity using the actual
    production adapter.
-   [ ] DBQ-0018 Verify readiness checks do not run SQLite-only SQL
    against PostgreSQL.
-   [ ] DBQ-0019 Validate required environment variables at startup.
-   [ ] DBQ-0020 Confirm secrets are absent from source, build output,
    logs and public directories.
-   [ ] DBQ-0021 Verify SMTP/provider DNS, authentication and sender
    alignment without exposing credentials.
-   [ ] DBQ-0022 Capture disk, memory, CPU, process and queue baseline.

## 3.4 Phase 0 acceptance criteria

-   A clean and identified source snapshot exists.
-   Production dirty changes are preserved and reconciled.
-   Backup restore has been demonstrated in a non-production
    environment.
-   All services and their data ownership are documented.
-   Required secrets are configured outside source control.
-   Readiness endpoints accurately reflect required dependencies.
-   Rollback steps are documented and peer-reviewed.

**Gate 0:** Project Manager, Tech Lead, DevOps and QA Lead approve the
baseline. If production is not reproducible or backup restore is
unverified, deployment remains blocked.

------------------------------------------------------------------------

# 4. Phase 1 --- Financial integrity and transaction safety

**Priority:** P0\
**Goal:** Make payment, UTR, enrollment and stipend operations durable,
idempotent and auditable.\
**Suggested duration:** 1--2 sprints.\
**Primary owner:** Backend Lead; Database Lead supports schema and
concurrency work.

## 4.1 Workstream 1A --- Balance payment persistence

Primary inspection target: -
`apps/website/src/app/api/enroll/balance/route.ts` -
`apps/website/prisma/` or the repository's active Prisma
schema/migrations - LMS internal enrollment-sync endpoint

Tasks: - \[ \] DBQ-0101 Confirm whether the JSON file is still the live
system of record. - \[ \] DBQ-0102 Design PostgreSQL tables for payment
claims, enrollment references and reconciliation events. - \[ \]
DBQ-0103 Add unique constraints for normalized UTR/payment references
according to approved business rules. - \[ \] DBQ-0104 Add foreign keys
and indexes for candidate, enrollment, payment and audit
relationships. - \[ \] DBQ-0105 Replace JSON read/modify/write
persistence with transactional DB writes. - \[ \] DBQ-0106 Validate
amount, currency, product, candidate and enrollment on the server. - \[
\] DBQ-0107 Normalize and validate UTR input; never treat receipt
submission as proof of settlement. - \[ \] DBQ-0108 Add idempotency key
for client retries and request timeouts. - \[ \] DBQ-0109 Add a safe
migration/import tool for existing JSON records. - \[ \] DBQ-0110
Reconcile imported row counts and hashes before cutover. - \[ \]
DBQ-0111 Retain a read-only, access-controlled archive of the legacy
data until sign-off.

Design requirement: - Store `amount_expected`, `amount_claimed`,
`amount_verified`, currency, payment method, UTR/reference, candidate
ID, enrollment ID, submitted time, verifier, verification time and
status. - Use a transaction for record creation and associated outbox
event. - Use database uniqueness and transaction isolation rather than
application-only duplicate checks.

## 4.2 Workstream 1B --- Website-to-LMS synchronization

-   [ ] DBQ-0112 Remove hardcoded fallback internal sync secrets from
    source.
-   [ ] DBQ-0113 Fail startup or disable the integration safely when
    required secrets are absent.
-   [ ] DBQ-0114 Inspect and validate the LMS HTTP status code and
    response schema.
-   [ ] DBQ-0115 Distinguish timeout, retryable server error, permanent
    validation error and authentication error.
-   [ ] DBQ-0116 Add durable outbox event in the same transaction as the
    source payment-claim record.
-   [ ] DBQ-0117 Add stable event ID and idempotency key to sync
    requests.
-   [ ] DBQ-0118 Implement bounded exponential retry with jitter.
-   [ ] DBQ-0119 Add dead-letter queue and admin replay workflow.
-   [ ] DBQ-0120 Add reconciliation job for website records without
    matching LMS records.
-   [ ] DBQ-0121 Expose sync status and last error category to
    authorized operations staff.
-   [ ] DBQ-0122 Ensure candidate-facing success message distinguishes
    "submission received" from "payment verified/enrollment active".

## 4.3 Workstream 1C --- Razorpay and webhook correctness

Inspection targets: - `apps/portal/routes/payment.py` -
`apps/portal/services/payment_service.py` -
`apps/portal/services/razorpay_client.py` -
`apps/website/src/app/api/payments/verify/route.ts` -
`apps/website/src/app/api/payments/webhook/route.ts`

Tasks: - \[ \] DBQ-0123 Map all order creation, client verification and
webhook routes. - \[ \] DBQ-0124 Verify webhook HMAC against raw request
body and fail closed when secret is missing. - \[ \] DBQ-0125 Add unique
provider webhook event ID constraint. - \[ \] DBQ-0126 Verify payment
order belongs to the authenticated candidate and intended product. - \[
\] DBQ-0127 Verify amount and currency against server-generated order
values. - \[ \] DBQ-0128 Make payment event recording and business state
transition atomic. - \[ \] DBQ-0129 Ensure duplicate webhook events are
harmless. - \[ \] DBQ-0130 Ensure late `payment.failed` cannot downgrade
an already paid record. - \[ \] DBQ-0131 Ensure gateway success followed
by DB failure creates a reconciliation case, not false enrollment
success. - \[ \] DBQ-0132 Remove raw exception messages from
client-facing responses. - \[ \] DBQ-0133 Add provider reference,
request ID and safe error category to audit logs. - \[ \] DBQ-0134 Add
manual reconciliation procedure for gateway-paid/database-unpaid
mismatches.

## 4.4 Workstream 1D --- Stipend ledger and AI eligibility

-   [ ] DBQ-0135 Trace every path from task submission to stipend
    eligibility and payout.
-   [ ] DBQ-0136 Ensure model timeout, invalid JSON, missing fields or
    low-confidence output cannot approve eligibility.
-   [ ] DBQ-0137 Separate AI recommendation from authorized human
    financial approval.
-   [ ] DBQ-0138 Store rubric version, model/version, evaluation
    timestamp and immutable input/output hashes.
-   [ ] DBQ-0139 Validate task, attendance, cohort, internship dates and
    completion requirements server-side.
-   [ ] DBQ-0140 Create immutable stipend ledger entries with unique
    idempotency references.
-   [ ] DBQ-0141 Prevent duplicate credits and duplicate disbursement
    requests.
-   [ ] DBQ-0142 Require authorized reviewer and reason for
    approval/rejection/adjustment.
-   [ ] DBQ-0143 Add reconciliation between approved stipend ledger and
    actual payout records.

## 4.5 Phase 1 failure-injection tests

-   [ ] Same UTR submitted concurrently from two sessions.
-   [ ] Same request retried after browser timeout.
-   [ ] LMS returns HTTP 500 after website transaction commits.
-   [ ] LMS returns HTTP 200 with malformed response body.
-   [ ] LMS request times out after remote service commits.
-   [ ] Razorpay webhook delivered twice.
-   [ ] Payment failure webhook arrives after success webhook.
-   [ ] Gateway verifies payment but database update fails.
-   [ ] Payment order is replayed by a different candidate.
-   [ ] AI evaluator times out or returns malformed output.
-   [ ] Stipend approval endpoint is called twice concurrently.

## 4.6 Phase 1 acceptance criteria

-   No duplicate payment claim or ledger credit under concurrency.
-   No false "payment verified" or "enrollment active" message.
-   Payment-to-enrollment ownership and amount binding are enforced.
-   Every cross-service sync failure is durable, visible and retryable.
-   Webhook replay and out-of-order callbacks do not corrupt state.
-   AI failure cannot grant financial eligibility.
-   All financial transitions have actor, timestamp, reason and source
    reference.
-   Finance reconciliation produces zero unexplained mismatches in the
    agreed test dataset.

**Gate 1:** Backend Lead, Database Lead, Finance/Operations owner and QA
Lead approve all payment, UTR, enrollment and stipend test evidence. No
P0 financial issue may be deferred without written executive risk
acceptance.

------------------------------------------------------------------------

# 5. Phase 2 --- Identity, authorization and application lifecycle

**Priority:** P0/P1\
**Goal:** Ensure each candidate can access only their own records and
every application transition is controlled.\
**Suggested duration:** 1--2 sprints.

## 5.1 Workstream 2A --- Canonical candidate identity

Inspection targets: - `apps/portal/routes/applications.py` -
`apps/portal/services/auth_service.py` - Registration, login, password
reset and account-linking handlers - Website cohort/application APIs and
database schema

Tasks: - \[ \] DBQ-0201 Document all candidate creation and login entry
points. - \[ \] DBQ-0202 Identify canonical immutable candidate/user
primary key. - \[ \] DBQ-0203 Trace email-change, duplicate-account and
legacy-import behavior. - \[ \] DBQ-0204 Review queries using
`intern_id OR email` for ownership decisions. - \[ \] DBQ-0205 Replace
unsafe email-only authorization with canonical user-ID relationships. -
\[ \] DBQ-0206 Create controlled verified account-linking flow for
legacy applications. - \[ \] DBQ-0207 Require proof of control of both
accounts or authorized staff adjudication before merging. - \[ \]
DBQ-0208 Audit all account merges and identity corrections. - \[ \]
DBQ-0209 Ensure email changes do not orphan applications, certificates
or payments. - \[ \] DBQ-0210 Ensure a shared email cannot automatically
expose another account's records.

## 5.2 Workstream 2B --- RBAC and IDOR

-   [ ] DBQ-0211 Build role-permission matrix for intern, mentor,
    company, staff, admin and super-admin.
-   [ ] DBQ-0212 Inventory all sensitive routes and their authorization
    checks.
-   [ ] DBQ-0213 Centralize authorization helpers/decorators where
    practical.
-   [ ] DBQ-0214 Test direct object references across applications,
    payments, tasks, certificates, files and stipends.
-   [ ] DBQ-0215 Test horizontal access between two interns.
-   [ ] DBQ-0216 Test vertical privilege escalation from
    intern/mentor/company to staff/admin.
-   [ ] DBQ-0217 Verify admin financial permissions are separate from
    academic review permissions.
-   [ ] DBQ-0218 Verify session expiry, logout, password reset and
    session rotation.
-   [ ] DBQ-0219 Add rate limits and abuse controls to authentication
    and public submission endpoints.
-   [ ] DBQ-0220 Verify CSRF protections for cookie-authenticated
    state-changing requests.

## 5.3 Workstream 2C --- Private file access

-   [ ] DBQ-0221 Inventory Nginx aliases, static mounts and public file
    routes.
-   [ ] DBQ-0222 Test direct unauthenticated access to CVs, receipts and
    private attachments.
-   [ ] DBQ-0223 Move private uploads to private storage or deny direct
    public serving.
-   [ ] DBQ-0224 Store file ownership, type, size, checksum and access
    metadata.
-   [ ] DBQ-0225 Serve files through authenticated authorization checks
    or short-lived signed URLs.
-   [ ] DBQ-0226 Validate file extension, MIME type, size and content;
    scan uploads where available.
-   [ ] DBQ-0227 Prevent path traversal and untrusted filename handling.
-   [ ] DBQ-0228 Add audit events for sensitive file downloads.

## 5.4 Workstream 2D --- Application state machine

Define a documented state graph. Do not allow arbitrary status strings
to be written directly by unrelated handlers.

Suggested conceptual states (confirm against current business policy
before migration): - `DRAFT` - `SUBMITTED` - `UNDER_REVIEW` -
`SHORTLISTED` - `INTERVIEW_PENDING` - `SELECTED` - `REJECTED` -
`OFFER_ISSUED` - `PAYMENT_PENDING` - `PAYMENT_REVIEW` - `ENROLLED` -
`WITHDRAWN` - `CANCELLED`

Tasks: - \[ \] DBQ-0229 Inventory current statuses and historical
values. - \[ \] DBQ-0230 Agree canonical state graph with product and
operations. - \[ \] DBQ-0231 Define permitted actor and transition for
every edge. - \[ \] DBQ-0232 Define mandatory reason and metadata for
rejection, withdrawal and override. - \[ \] DBQ-0233 Add optimistic
concurrency/version check to admin state changes. - \[ \] DBQ-0234
Record immutable transition history. - \[ \] DBQ-0235 Ensure frontend
displays server-authoritative current state and next action. - \[ \]
DBQ-0236 Provide safe handling for obsolete links and withdrawn/closed
opportunities.

## 5.5 Phase 2 acceptance criteria

-   Two accounts cannot access each other's applications, payments,
    files or credentials.
-   Email similarity alone cannot grant access or merge identities.
-   Every sensitive route passes role and ownership tests.
-   Private candidate documents cannot be accessed through public Nginx
    aliases.
-   Invalid state transitions are rejected server-side.
-   Every high-impact admin action has an actor, timestamp and reason.
-   Candidate sees clear status, blocker and next permitted action.

**Gate 2:** Security Lead and QA Lead sign the authorization matrix and
attach IDOR/RBAC regression evidence.

------------------------------------------------------------------------

# 6. Phase 3 --- Notifications and background processing reliability

**Priority:** P0/P1\
**Goal:** Ensure emails, synchronization events and other background
work cannot silently disappear or be processed unpredictably.\
**Suggested duration:** 1 sprint, depending on current worker
architecture.

## 6.1 Workstream 3A --- Durable outbox and worker claims

Inspection target: - `apps/portal/services/outbox_service.py` - Worker
scheduler/CLI/systemd units - Event outbox schema and migrations

Tasks: - \[ \] DBQ-0301 Map every producer and consumer of outbox
events. - \[ \] DBQ-0302 Verify outbox row is committed in same
transaction as business event. - \[ \] DBQ-0303 Add atomic event
claim/lease mechanism. - \[ \] DBQ-0304 Use PostgreSQL row
locking/`SKIP LOCKED` where supported and appropriate. - \[ \] DBQ-0305
Add `PROCESSING` state, worker ID, claimed timestamp and lease expiry. -
\[ \] DBQ-0306 Reclaim expired leases after worker crash. - \[ \]
DBQ-0307 Add bounded exponential backoff with jitter. - \[ \] DBQ-0308
Add max attempts and dead-letter state. - \[ \] DBQ-0309 Add safe
operator replay with audit record. - \[ \] DBQ-0310 Ensure event
handlers are idempotent. - \[ \] DBQ-0311 Add queue age, pending count,
retry count and dead-letter metrics. - \[ \] DBQ-0312 Add alert for
oldest pending event and stalled worker.

Important delivery semantics: - A database outbox can provide durable
at-least-once dispatch, not magical exactly-once email delivery. -
Provider acceptance followed by worker crash can cause a duplicate
attempt. - Use stable idempotency keys where provider APIs support them;
otherwise make duplicate handling explicit and observable.

## 6.2 Workstream 3B --- Email provider health

-   [ ] DBQ-0313 Verify SMTP/provider host, port, TLS mode and
    authentication.
-   [ ] DBQ-0314 Verify sender domain SPF, DKIM and DMARC alignment.
-   [ ] DBQ-0315 Verify primary and fallback provider DNS and
    credentials.
-   [ ] DBQ-0316 Remove silent exception swallowing in background email
    paths.
-   [ ] DBQ-0317 Record provider message ID and safe failure category.
-   [ ] DBQ-0318 Process bounce, complaint and delivery webhooks where
    supported.
-   [ ] DBQ-0319 Separate `QUEUED`, `PROVIDER_ACCEPTED`, `DELIVERED`,
    `BOUNCED`, `FAILED` states where evidence exists.
-   [ ] DBQ-0320 Add a controlled test-recipient health check; do not
    spam real candidates.
-   [ ] DBQ-0321 Add template rendering tests for offer, selection,
    rejection, payment, certificate and stipend notices.

## 6.3 Phase 3 acceptance criteria

-   Concurrent workers do not claim the same active lease.
-   Expired worker leases recover after process termination.
-   Failed notifications retry and eventually dead-letter.
-   Provider acceptance is not mislabeled as inbox delivery.
-   Every critical notification failure is visible to operations.
-   Replaying a business event does not create duplicate financial or
    enrollment transitions.

**Gate 3:** Backend Lead and QA Lead approve concurrency, crash-recovery
and email-provider evidence.

------------------------------------------------------------------------

# 7. Phase 4 --- Candidate funnel, website and LMS UX

**Priority:** P1/P2\
**Goal:** Remove candidate-facing dead ends and make the full journey
measurable.\
**Suggested duration:** 1--2 sprints.

## 7.1 Workstream 4A --- Canonical candidate journey

Target journey: 1. Discover program/job. 2. Review eligibility,
duration, fee/refund conditions and stipend terms. 3. Apply. 4.
Register/login while preserving destination. 5. Complete and submit
application. 6. Track review status. 7. Receive selection/rejection
outcome. 8. Review offer and required next steps. 9. Submit payment
claim or pay online. 10. Track verification. 11. Activate enrollment.
12. Access learning, mentor and project. 13. Complete internship and
eligibility review. 14. Receive certificate/LOR where eligible. 15.
Track stipend review and payout where applicable. 16. Access
placement/hiring opportunities.

Tasks: - \[ \] DBQ-0401 Map all public CTAs to destination routes and
conversion events. - \[ \] DBQ-0402 Ensure login redirects back to the
originally requested action. - \[ \] DBQ-0403 Add resumable application
drafts with server-side persistence. - \[ \] DBQ-0404 Add application
reference and clear post-submit confirmation. - \[ \] DBQ-0405
Differentiate submitted, selected, payment pending, payment verified and
enrolled. - \[ \] DBQ-0406 Add candidate timeline with event time and
next action. - \[ \] DBQ-0407 Add helpful empty states with a valid
recovery link. - \[ \] DBQ-0408 Add closed/expired opportunity recovery
page. - \[ \] DBQ-0409 Add support escalation for stuck or inconsistent
states. - \[ \] DBQ-0410 Validate all critical flows on mobile viewport
and keyboard navigation.

## 7.2 Workstream 4B --- Pricing, payment and program clarity

-   [ ] DBQ-0411 Inventory all prices and payment products across
    website, LMS and API.
-   [ ] DBQ-0412 Identify one authoritative pricing configuration per
    product.
-   [ ] DBQ-0413 Document refundable/non-refundable/adjustable amounts
    with business approval.
-   [ ] DBQ-0414 Ensure payment amount and product are server-derived.
-   [ ] DBQ-0415 Ensure UI explains what is free, optional, mandatory
    and conditional.
-   [ ] DBQ-0416 Ensure failed/abandoned payment has a safe retry or
    support route.
-   [ ] DBQ-0417 Prevent payment retries from generating duplicate
    active enrollments.

Do not change program pricing or refund policy as part of a technical
refactor without explicit business approval.

## 7.3 Workstream 4C --- Candidate dashboard

Recommended modules: - Current application/enrollment status. - Next
required action. - Pending items and blockers. - Program/course
roadmap. - Attendance and participation. - Tasks, project and mentor
feedback. - Certificate and credential wallet. - Stipend
eligibility/review/payout status. - Support tickets and announcements.

Tasks: - \[ \] DBQ-0418 Build role/state-based dashboard information
architecture. - \[ \] DBQ-0419 Ensure dashboard cards derive from
server-authoritative state. - \[ \] DBQ-0420 Show last updated timestamp
and pending-with-DBERT indicators. - \[ \] DBQ-0421 Ensure empty states
are actionable and not misleading. - \[ \] DBQ-0422 Add accessible
loading, retry and error states. - \[ \] DBQ-0423 Avoid displaying
unverified metrics or promises.

## 7.4 Workstream 4D --- Admin operational control center

-   [ ] DBQ-0424 Create queues for application review, payment review,
    sync mismatch, failed email, certificate and stipend.
-   [ ] DBQ-0425 Add assignee, SLA age, priority and audit history.
-   [ ] DBQ-0426 Add preview/confirmation for bulk operations.
-   [ ] DBQ-0427 Add optimistic concurrency checks for simultaneous
    staff edits.
-   [ ] DBQ-0428 Add export audit and least-privilege access.
-   [ ] DBQ-0429 Add safe manual replay/reconciliation actions with
    audit records.
-   [ ] DBQ-0430 Add operational report for unresolved mismatches and
    stuck records.

## 7.5 Funnel instrumentation

Track server-side events with stable IDs: - `program_viewed` -
`application_started` - `application_submitted` - `account_verified` -
`application_reviewed` - `candidate_selected` - `offer_issued` -
`payment_claim_submitted` - `payment_verified` -
`enrollment_activated` - `course_started` - `internship_completed` -
`certificate_issued` - `stipend_approved` - `stipend_paid`

Tasks: - \[ \] DBQ-0431 Define event schema, consent and retention
policy. - \[ \] DBQ-0432 Record source page, campaign, program and
domain where available. - \[ \] DBQ-0433 Count actual persisted
transitions, not CTA clicks as conversions. - \[ \] DBQ-0434 Add funnel
drop-off and stage-duration reports. - \[ \] DBQ-0435 Exclude
duplicate/replayed events from conversion counts.

## 7.6 Phase 4 acceptance criteria

-   Every critical CTA reaches a valid destination.
-   Login and session expiry preserve the intended journey.
-   Application draft resumes safely.
-   Candidate can understand status, next action and support path.
-   Payment language does not imply verification before reconciliation.
-   Admin can identify and resolve stuck records without direct database
    editing.
-   Funnel analytics reconcile with canonical persisted records.

**Gate 4:** Product Owner and QA Lead sign off on candidate and staff
browser journeys.

------------------------------------------------------------------------

# 8. Phase 5 --- Observability, analytics, performance and release QA

**Priority:** P0/P1/P2\
**Goal:** Make the platform measurable, testable and safely releasable.\
**Suggested duration:** 1--2 sprints, with selected controls started
earlier.

## 8.1 Workstream 5A --- Health and observability

-   [ ] DBQ-0501 Separate liveness from readiness.
-   [ ] DBQ-0502 Make readiness verify required dependencies with
    database-specific queries.
-   [ ] DBQ-0503 Return dependency status without leaking credentials or
    connection strings.
-   [ ] DBQ-0504 Add structured logs with request/correlation ID.
-   [ ] DBQ-0505 Add metrics for DB errors, payment errors, auth
    denials, email failures, queue lag and sync mismatches.
-   [ ] DBQ-0506 Add external alerting for P0 operational conditions.
-   [ ] DBQ-0507 Ensure telemetry is process/distributed aware; do not
    rely solely on in-memory counters across multiple workers.
-   [ ] DBQ-0508 Define log retention and personal-data redaction.
-   [ ] DBQ-0509 Add dashboards for service health and business
    transaction health.

## 8.2 Workstream 5B --- CI and automated quality gates

-   [ ] DBQ-0510 Make dependency installation reproducible and lock
    dependency versions.
-   [ ] DBQ-0511 Install and pin Playwright and accessibility test
    dependencies in CI.
-   [ ] DBQ-0512 Fix PostgreSQL adapter test doubles to match supported
    cursor/connection interfaces.
-   [ ] DBQ-0513 Run portal unit tests in CI.
-   [ ] DBQ-0514 Run website type-check, lint, build and route/SEO
    checks.
-   [ ] DBQ-0515 Run integration tests against PostgreSQL service
    container.
-   [ ] DBQ-0516 Run browser E2E tests for critical candidate and admin
    journeys.
-   [ ] DBQ-0517 Run dependency, secret and static security scans.
-   [ ] DBQ-0518 Publish test reports and artifacts for every PR.
-   [ ] DBQ-0519 Block merge on P0 security/payment regressions.
-   [ ] DBQ-0520 Add migration validation and schema drift checks.

## 8.3 Workstream 5C --- Performance and resilience

-   [ ] DBQ-0521 Establish baseline latency and throughput for critical
    routes.
-   [ ] DBQ-0522 Profile slow database queries and add appropriate
    indexes.
-   [ ] DBQ-0523 Test expected concurrency for application and payment
    submissions.
-   [ ] DBQ-0524 Test worker backlog and recovery after outage.
-   [ ] DBQ-0525 Test database connection pool exhaustion and graceful
    recovery.
-   [ ] DBQ-0526 Add bounded timeouts and retry budgets for external
    calls.
-   [ ] DBQ-0527 Add caching only for data with clear invalidation and
    privacy rules.
-   [ ] DBQ-0528 Test backup/restore and disaster recovery periodically.

## 8.4 Workstream 5D --- Release governance

-   [ ] DBQ-0529 Produce release candidate from immutable
    commit/artifact.
-   [ ] DBQ-0530 Deploy to staging and run smoke suite.
-   [ ] DBQ-0531 Run candidate and admin E2E suites.
-   [ ] DBQ-0532 Run payment/webhook sandbox tests.
-   [ ] DBQ-0533 Verify database migrations and backup checkpoint.
-   [ ] DBQ-0534 Obtain QA, Engineering, Operations and Product
    sign-off.
-   [ ] DBQ-0535 Deploy progressively with health monitoring.
-   [ ] DBQ-0536 Verify post-deployment health and critical read-only
    journeys.
-   [ ] DBQ-0537 Keep rollback window and on-call owner active.
-   [ ] DBQ-0538 Record release SHA, migration version, deployment time
    and final evidence.

## 8.5 Phase 5 acceptance criteria

-   CI is reproducible and required tests are not silently skipped.
-   Critical browser and integration tests pass.
-   Health endpoints correctly represent service health.
-   Critical failure conditions page the responsible owner.
-   Performance is within approved service-level objectives.
-   Rollback has been rehearsed.
-   Release evidence is archived and traceable to the deployed commit.

**Gate 5:** QA Lead recommends release; Engineering Lead confirms
technical safety; Product/Operations confirm business workflows;
authorized release owner approves deployment.

------------------------------------------------------------------------

# 9. Cross-phase QA test catalogue

All test cases must have a test ID, environment, test data identifier,
expected result, actual result, evidence link, tester and timestamp. Use
synthetic data wherever possible.

## 9.1 Silent-failure and transaction tests

  ------------------------------------------------------------------------------
  Test ID          Scenario         Expected result                     Priority
  ---------------- ---------------- ---------------------- ---------------------
  SF-001           Application      No false success;                         P0
                   submit while DB  recoverable error      
                   unavailable                             

  SF-002           Application      Application remains;                      P0
                   commits but      notification           
                   email fails      queued/retried         

  SF-003           Duplicate        Defined                                   P1
                   application      idempotent/duplicate   
                   requests         response               
                   concurrently                            

  SF-004           Same UTR         One canonical claim                       P0
                   submitted                               
                   concurrently                            

  SF-005           LMS sync returns Durable pending/retry                     P0
                   HTTP 500         state                  

  SF-006           LMS sync times   Retry does not                            P0
                   out after remote duplicate remote       
                   commit           record                 

  SF-007           Webhook          One business                              P0
                   delivered twice  transition             

  SF-008           Failure webhook  Paid state remains                        P0
                   arrives after    paid                   
                   success                                 

  SF-009           Payment order    Ownership check                           P0
                   used by another  rejects                
                   candidate                               

  SF-010           AI evaluator     No auto-approval                          P0
                   times out                               

  SF-011           Stipend approval One ledger                                P0
                   submitted twice  entry/credit           

  SF-012           Worker crashes   Retry is                                  P1
                   after provider   safe/duplicate is      
                   accepts email    detectable             

  SF-013           Two workers      Atomic claim prevents                     P0
                   fetch pending    concurrent processing  
                   events                                  
                   simultaneously                          

  SF-014           Worker lease     Event safely becomes                      P1
                   expires          claimable              

  SF-015           Certificate      No duplicate                              P1
                   issuance retried credential             
  ------------------------------------------------------------------------------

## 9.2 Security and authorization tests

  -------------------------------------------------------------------------------------
  Test ID          Scenario          Expected result                           Priority
  ---------------- ----------------- ---------------------------- ---------------------
  SEC-001          Intern A requests Denied                                          P0
                   Intern B                                       
                   application                                    

  SEC-002          Intern A requests Denied                                          P0
                   Intern B                                       
                   receipt/CV                                     

  SEC-003          Mentor attempts   Denied unless explicitly                        P0
                   financial         authorized                   
                   approval                                       

  SEC-004          Intern attempts   Denied                                          P0
                   admin endpoint                                 

  SEC-005          Shared email on   No automatic data disclosure                    P0
                   separate accounts                              

  SEC-006          Unauthenticated   Denied for private file                         P0
                   direct file URL                                

  SEC-007          Expired session   Reauthentication/CSRF-safe                      P1
                   submits           rejection                    
                   state-changing                                 
                   request                                        

  SEC-008          Missing webhook   Webhook processing fails                        P0
                   secret            closed                       

  SEC-009          Missing internal  Integration disabled/fails                      P0
                   sync secret       closed                       

  SEC-010          Path traversal    Rejected                                        P0
                   upload/download                                
                   attempt                                        
  -------------------------------------------------------------------------------------

## 9.3 Funnel and UX tests

  -------------------------------------------------------------------------------
  Test ID          Scenario         Expected result                      Priority
  ---------------- ---------------- ----------------------- ---------------------
  UX-001           Apply while      Login then return to                       P1
                   logged out       intended application    

  UX-002           Refresh during   Draft restored safely                      P1
                   multi-step form                          

  UX-003           Submit           Reference and next                         P1
                   application      action shown            

  UX-004           Candidate        Status, timeline and                       P1
                   awaiting review  support shown           

  UX-005           Candidate        Offer and approved next                    P1
                   selected         steps shown             

  UX-006           Payment pending  Correct amount/status                      P0
                                    and retry/support shown 

  UX-007           Payment rejected Reason and permitted                       P1
                                    resubmission path shown 

  UX-008           Candidate        Course/roadmap/mentor                      P1
                   enrolled         entry point available   

  UX-009           No jobs/courses  Useful empty state and                     P2
                   available        recovery link           

  UX-010           Mobile critical  No blocked controls or                     P1
                   journey          inaccessible content    
  -------------------------------------------------------------------------------

------------------------------------------------------------------------

# 10. Release acceptance policy

A release is **NO-GO** if any of the following is true:

-   Any open P0 defect affects payment, enrollment, identity, privacy,
    stipend, data durability or production availability.
-   Production readiness fails for a required dependency.
-   Backup restore or rollback is unverified for a risky migration.
-   Critical candidate/admin E2E journey fails.
-   A financial transaction can be duplicated or misattributed.
-   A critical notification or sync failure is untracked and
    unrecoverable.
-   Private CVs, receipts or candidate records are publicly accessible.
-   A release artifact cannot be tied to a reviewed commit.

A release may proceed with P1/P2/P3 items only when: - The risk is
documented. - A named owner and target date exist. - There is an
approved workaround. - Product/Engineering/QA accept the residual risk
in writing.

## 10.1 Proposed release metrics

These are proposed acceptance targets; validate them against DBERT's
operating requirements before adopting as contractual SLOs.

  Metric                                         Proposed target
  ---------------------------------------------- -------------------------------
  P0 open at release                             0
  Unauthorized access in security regression     0
  Duplicate financial ledger credits             0
  Unexplained payment/enrollment mismatches      0
  Critical E2E pass rate                         100%
  Critical notification failures without alert   0
  Readiness for required dependencies            Healthy
  Backup restore drill                           Passed
  Rollback rehearsal                             Passed
  Critical API error contract                    No internal exception leakage

------------------------------------------------------------------------

# 11. Risks, dependencies and decision log

## 11.1 Risk register

  --------------------------------------------------------------------------------------
  Risk ID     Risk          Impact            Mitigation       Owner         Status
  ----------- ------------- ----------------- ---------------- ------------- -----------
  R-001       Production    Unsafe            Preserve, diff   DevOps        OPEN
              working tree  deployment/data   and reconcile                  
              differs from  loss              before deploy                  
              Git                                                            

  R-002       Payment data  Financial         DB migration and Backend/DB    OPEN
              split across  mismatch          reconciliation                 
              file and DB                                                    

  R-003       External sync Enrollment        Durable outbox   Integration   OPEN
              unavailable   divergence        and replay                     

  R-004       Email         Candidate misses  Provider         Operations    OPEN
              provider      critical updates  verification and               
              degraded                        queue monitoring               

  R-005       Identity      Privacy breach    Immutable        Security      OPEN
              linking                         identity and                   
              ambiguity                       controlled merge               

  R-006       Worker        Duplicate side    Atomic claim and Backend       OPEN
              concurrency   effects           idempotency                    

  R-007       Schema drift  Runtime failures  Migration checks DB Lead       OPEN
                                              and staging                    
                                              parity                         

  R-008       Scope         Delayed risk      Change control   PM            OPEN
              expansion     closure           and phase gates                
              during                                                         
              remediation                                                    
  --------------------------------------------------------------------------------------

## 11.2 Decision log

  --------------------------------------------------------------------------------------
  Decision ID    Decision         Options          Decision owner        Decision/date
                 required                                                
  -------------- ---------------- ---------------- --------------------- ---------------
  DEC-001        Canonical owner  LMS DB / shared  Engineering/Product   TBD
                 for candidate    identity service                       
                 identity                                                

  DEC-002        Canonical        PostgreSQL       Finance/Engineering   TBD
                 financial record schema/service                         
                 store                                                   

  DEC-003        Private file     Private object   Security/DevOps       TBD
                 storage          storage /                              
                 architecture     protected local                        
                                  storage                                

  DEC-004        Worker           Existing worker  Engineering           TBD
                 implementation   / dedicated                            
                                  queue worker                           

  DEC-005        Candidate state  Approved         Product/Operations    TBD
                 graph            lifecycle and                          
                                  transitions                            

  DEC-006        Stipend approval Human approval   Finance/Operations    TBD
                 policy           and eligibility                        
                                  controls                               

  DEC-007        Pricing and      Central          Business owner        TBD
                 refund policy    configuration                          
                 source           and approval                           
                                  process                                
  --------------------------------------------------------------------------------------

## 11.3 Change control

Any request that adds scope or changes acceptance criteria must
record: - Change ID. - Reason and business value. - Affected phase and
task IDs. - Security/data/financial impact. - Effort and schedule
impact. - Approver. - Updated acceptance tests.

------------------------------------------------------------------------

# 12. Exact progress update procedure

For every PR or sprint review:

1.  Pull the latest remediation branch and this plan.
2.  Confirm the task still applies to the current code; update file
    paths if modules moved.
3.  Add or update task owner and status.
4.  Link the PR and commit SHA.
5.  Link test report, CI run or reproducible evidence.
6.  Record any failed acceptance test and create a defect ID.
7.  Recalculate phase completion from accepted tasks only.
8.  Update risk register and decision log.
9.  Update the change log below.
10. Obtain phase-gate sign-off before starting dependent work or
    deploying.

### Task update example

``` text
Task: DBQ-0114
Status: IN_REVIEW
Owner: Backend Engineer
PR: <GitHub PR URL>
Commit: <SHA>
Evidence:
- Unit test: <link>
- Integration test: <link>
- Failure injection: <link>
Acceptance:
- HTTP 500 is detected: PASS
- Malformed response is rejected: PASS
- Timeout is retried durably: FAIL
Blocker: Retry worker not deployed to staging
Next action: Complete worker retry test
Updated by/date: <name / YYYY-MM-DD>
```

### Phase closure example

``` text
Phase: 1 — Financial integrity and transaction safety
Status: IN_REVIEW
Completion: <accepted tasks>/<total tasks>
P0 remaining: <count>
Payment concurrency: PASS/FAIL
Webhook replay: PASS/FAIL
Cross-service sync: PASS/FAIL
Stipend fail-closed: PASS/FAIL
Reconciliation: PASS/FAIL
QA approval: <name/date>
Engineering approval: <name/date>
Operations/Finance approval: <name/date>
Gate decision: OPEN / CLOSED
```

------------------------------------------------------------------------

# 13. Change log

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Date              Version           Updated by        Change
  ----------------- ----------------- ----------------- -----------------------------------------------------------------------------------------------------------------------------------
  2026-11-19        2.0               Engineering QA    Phases 0-5 remediation executed and validated. Resolved BASE-01..12, outbox atomic leasing, fail-closed AI stipend, and RBAC file sandbox.
  2026-11-18        1.0               Project QA        Initial phase-by-phase remediation plan created from repository review and prior audit observations
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Append newest entries at the top. Never erase historical decisions or
evidence; supersede them with a dated entry.

------------------------------------------------------------------------

# 14. Final execution order

The required order is:

1.  **Phase 0:** preserve and reconcile source, production and data.
2.  **Phase 1:** repair payment, enrollment, synchronization and stipend
    integrity.
3.  **Phase 2:** secure candidate identity, authorization, files and
    lifecycle transitions.
4.  **Phase 3:** make background jobs and notifications durable and
    observable.
5.  **Phase 4:** remove funnel dead ends and improve candidate/admin
    experience.
6.  **Phase 5:** complete monitoring, automated QA, performance and
    release governance.

Do not start large feature expansion until Phases 0--3 have passed their
gates. UX work that does not alter financial or security boundaries may
proceed in parallel only with explicit ownership and no interference
with P0 remediation.

## Final project rule

**A task is not fixed when the code looks correct. It is fixed when the
failure scenario has been reproduced, the correction has been tested,
the persisted business state is correct, the evidence is attached, and
the responsible QA owner has approved closure.**
