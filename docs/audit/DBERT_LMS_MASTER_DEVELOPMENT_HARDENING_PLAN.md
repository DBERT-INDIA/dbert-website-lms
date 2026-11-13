# DBERT LMS --- Master Development & Hardening Plan

## PostgreSQL-only Runtime + DBERT Mailer-only Email + Lean Portal Bootstrap + Agent Resume System

**Repository:** `DBERT-INDIA/dbert-website-lms`\
**Primary production portal:** `https://internship.dbert.online/`\
**Required mail transport:** `https://mailer.aivaratech.online/`\
**Mailer endpoint:** `https://mailer.aivaratech.online/send`

------------------------------------------------------------------------

# 0. Mission

This document is the execution contract for a local AI coding agent
working on the DBERT LMS repository.

The agent must:

1.  Make **PostgreSQL the only runtime database**.
2.  Remove SQLite from runtime and retire `apps/portal/internship.db`
    only after migration verification.
3.  Route **100% of application/transactional email through DBERT
    Mailer**.
4.  Treat `https://mailer.aivaratech.online/` as the only approved
    application email transport.
5.  Keep SMTP/cPanel transport logic inside DBERT Mailer, not inside the
    portal or website.
6.  Reduce `apps/portal/app.py` to a clean application/bootstrap layer.
7.  Preserve and strengthen the extracted `routes/`, `services/`,
    `utils/`, database, learning, and supporting architecture.
8.  Remove dead/duplicate/legacy code only after reachability and
    regression verification.
9.  Add durable tests, negative tests, regression/backtests, security
    checks, and production gates at every phase.
10. Maintain persistent progress so another agent/session can safely
    resume without guessing what was completed.

## Non-negotiable architecture invariants

``` text
PostgreSQL
   ↑
Portal / Website services
   ↑
Routes / API
   ↑
Application bootstrap

Application Email
   ↓
DBERT Mailer
   ↓
cPanel / SMTP infrastructure
```

### Hard rules

-   SQLite is forbidden in production runtime.
-   No runtime fallback from PostgreSQL to SQLite.
-   No direct SMTP from portal or website.
-   No direct cPanel mailbox authentication from portal or website.
-   No `smtplib` outside DBERT Mailer.
-   No fake email success.
-   No duplicate email transport implementations.
-   `app.py` must not become a business-logic container.
-   No destructive legacy-code deletion without reachability evidence.
-   No phase may be marked complete until its exit gate passes.
-   Every implementation phase must include positive tests,
    negative/adversarial tests, and regression/backtests.

------------------------------------------------------------------------

# 1. Agent Operating Rules

The local AI agent must behave as a repository maintainer, not as an
uncontrolled code generator.

## 1.1 Before changing anything

Run:

``` bash
git status --short
git branch --show-current
git log -5 --oneline
```

Then inspect:

``` bash
find . -maxdepth 3 -type f | sort
```

and search architecture-sensitive patterns:

``` bash
git grep -n -E 'sqlite|sqlite3|internship\.db|DATABASE_URL|SQLALCHEMY_DATABASE_URI'
git grep -n -E 'smtplib|SMTP|send_email|send_mail|Flask-Mail|CPANEL_EMAIL_API|EMAIL_PROVIDER|mailer'
```

Do not modify code until the current phase is loaded from:

``` text
.agent/CURRENT_PHASE.md
.agent/PROGRESS.json
.agent/FINDINGS.md
.agent/BUG_REGISTER.md
.agent/BLOCKERS.md
.agent/DECISIONS.md
.agent/TEST_RESULTS.md
```

## 1.2 Resume rule

If a session starts after interruption:

1.  Read `.agent/MASTER_PLAN.md`.
2.  Read `.agent/CURRENT_PHASE.md`.
3.  Read `.agent/PROGRESS.json`.
4.  Read `.agent/BLOCKERS.md`.
5.  Inspect `git status`.
6.  Inspect the last commit.
7.  Re-run the phase preflight.
8.  Continue from the first incomplete task.
9.  Never assume a task is complete because code appears to exist.
10. Never overwrite uncommitted work without first understanding it.

## 1.3 Phase status values

Use only:

``` text
NOT_STARTED
IN_PROGRESS
BLOCKED
FAILED
READY_FOR_REVIEW
COMPLETE
```

A phase may become `COMPLETE` only after all mandatory acceptance
criteria and regression tests pass.

------------------------------------------------------------------------

# 2. Persistent Agent State

Create and maintain:

``` text
.agent/
├── MASTER_PLAN.md
├── CURRENT_PHASE.md
├── PROGRESS.json
├── FINDINGS.md
├── BUG_REGISTER.md
├── BLOCKERS.md
├── DECISIONS.md
├── TEST_RESULTS.md
├── CHANGELOG.md
└── scripts/
    ├── preflight.sh
    ├── architecture_scan.sh
    ├── sqlite_scan.sh
    ├── email_transport_scan.sh
    ├── secret_scan.sh
    └── release_gate.sh
```

## 2.1 `PROGRESS.json`

Recommended structure:

``` json
{
  "project": "DBERT LMS",
  "repository": "DBERT-INDIA/dbert-website-lms",
  "current_phase": 0,
  "status": "IN_PROGRESS",
  "last_updated": "",
  "completed_tasks": [],
  "failed_tasks": [],
  "tests_passed": [],
  "tests_failed": [],
  "files_modified": [],
  "files_removed": [],
  "files_added": [],
  "blockers": [],
  "decisions": [],
  "next_action": "",
  "last_verified_commit": ""
}
```

Update this file after every meaningful task group.

## 2.2 Phase completion record

At phase completion record:

-   phase number
-   completion timestamp
-   commit SHA
-   tests run
-   tests passed
-   tests failed
-   files changed
-   files deleted
-   migration status
-   security findings
-   known limitations
-   next phase

------------------------------------------------------------------------

# 3. Required Development Discipline

For every phase:

### Step A --- Discover

Read current implementation.

### Step B --- Map

Identify:

-   callers
-   imports
-   dependencies
-   database effects
-   external integrations
-   tests
-   frontend consumers
-   production configuration

### Step C --- Implement

Make the smallest safe change.

### Step D --- Test

Run focused tests.

### Step E --- Adversarial test

Test invalid, duplicate, unauthorized, malformed, replayed, missing, and
failure conditions.

### Step F --- Backtest

Run previously passing relevant tests and user journeys.

### Step G --- Inspect diff

``` bash
git diff --check
git diff --stat
git status --short
```

### Step H --- Record

Update `.agent/*`.

### Step I --- Commit

Use a focused commit after the phase gate passes.

------------------------------------------------------------------------

# 4. PHASE 0 --- Repository Baseline & Agent Resume System

## Objective

Establish a reproducible baseline before modifying architecture.

## Tasks

-   Create `.agent/`.
-   Record repository branch and commit.
-   Inventory backend, frontend, mailer, database, migrations, scripts,
    tests and docs.
-   Record existing test commands.
-   Record Python/Node/package versions.
-   Identify production configuration files.
-   Identify generated files and secrets.
-   Create baseline architecture scan.

## Inspect

``` text
apps/portal/
apps/website/
apps/portal/dbert-mailer/
tests/
docs/
migrations/
scripts/
```

## Required scans

``` bash
git grep -n -E 'sqlite|sqlite3|internship\.db'
git grep -n -E 'smtplib|Flask-Mail|SMTP|send_email|send_mail'
git grep -n -E 'CPANEL_EMAIL_API|mailer\.dbert\.online|mailer\.aivaratech\.online'
```

## Tests

-   Existing backend test suite.
-   Existing frontend test/lint/build suite.
-   Mailer test suite if present.
-   Import/startup test.

## Acceptance

-   Baseline recorded.
-   Current tests documented.
-   No untracked unexplained files.
-   Agent state files created.

## Exit gate

`PROGRESS.json` contains the baseline commit and next action.

------------------------------------------------------------------------

# 5. PHASE 1 --- Architecture Discovery & Dependency Graph

## Objective

Understand what has already been extracted from `app.py` and prevent
duplicate implementations.

## Tasks

Build a map of:

``` text
app.py
  ├── routes
  ├── services
  ├── database
  ├── learning
  ├── utilities
  ├── middleware
  └── startup/bootstrap
```

For every major function/class in `apps/portal/app.py`, classify:

``` text
BOOTSTRAP
ACTIVE_BUSINESS_LOGIC
DUPLICATE
LEGACY
DEAD
UNKNOWN
```

## Deliverables

Create:

``` text
.agent/APP_PY_REACHABILITY.md
.agent/DEPENDENCY_GRAPH.md
```

## Acceptance

Every candidate deletion has:

-   caller search
-   import search
-   route registration check
-   template/frontend reference check
-   test reference check
-   runtime reachability conclusion

No deletion based solely on file size or appearance.

------------------------------------------------------------------------

# 6. PHASE 2 --- PostgreSQL-Only Enforcement

## Objective

Make PostgreSQL the only supported runtime database.

## Rules

The application must fail clearly if PostgreSQL is unavailable or
incorrectly configured.

It must never silently switch to SQLite.

## Tasks

-   Identify canonical database configuration.
-   Normalize environment variables.
-   Ensure all production services use PostgreSQL.
-   Remove fallback database initialization.
-   Ensure migrations target PostgreSQL.
-   Ensure test configuration uses PostgreSQL-compatible infrastructure.
-   Verify connection pooling and transaction configuration.
-   Add readiness check for database connectivity.

## Forbidden patterns

``` python
sqlite3.connect(...)
```

``` text
sqlite:///...
```

``` text
if postgres_fails:
    use_sqlite()
```

## Tests

### Positive

-   PostgreSQL connection succeeds.
-   Application startup succeeds with valid configuration.
-   CRUD operations work.

### Negative

-   Missing PostgreSQL URL.
-   Invalid PostgreSQL credentials.
-   Unreachable PostgreSQL host.
-   Missing database.
-   Migration mismatch.

Application must fail safely and visibly.

## Acceptance

-   No production SQLite fallback.
-   PostgreSQL is canonical.
-   Startup/readiness reflects actual DB state.

------------------------------------------------------------------------

# 7. PHASE 3 --- SQLite Retirement & Removal

## Objective

Retire legacy SQLite safely.

## Precondition

Phase 2 must be complete.

## Tasks

Search:

``` bash
git grep -n -i 'sqlite'
git grep -n 'internship.db'
find . -iname '*sqlite*' -o -name 'internship.db'
```

Identify:

-   runtime references
-   migration references
-   tests
-   scripts
-   docs
-   backups
-   development-only utilities

## Migration safety

Before deleting the database:

1.  Export/backup legacy data.
2.  Compare SQLite schema with PostgreSQL.
3.  Compare table counts.
4.  Compare row counts.
5.  Validate primary keys.
6.  Validate foreign keys.
7.  Validate unique constraints.
8.  Validate nullable/non-nullable fields.
9.  Validate timestamps.
10. Validate enums/status values.
11. Validate application-level records.

## Required artifact

``` text
.agent/SQLITE_RETIREMENT_REPORT.md
```

## Deletion

After verification:

-   remove runtime SQLite references
-   remove `apps/portal/internship.db`
-   remove obsolete SQLite scripts
-   update docs
-   update `.gitignore`

If historical Git removal is required, use a dedicated
repository-history cleanup procedure and rotate exposed secrets
before/with it.

## Exit gate

A fresh checkout can run the application without SQLite.

------------------------------------------------------------------------

# 8. PHASE 4 --- Database Migration Integrity & Production Verification

## Objective

Prove the migrated PostgreSQL database is structurally and functionally
correct.

## Verify

### Schema

-   tables
-   columns
-   data types
-   primary keys
-   foreign keys
-   indexes
-   unique constraints
-   check constraints
-   defaults
-   nullable fields

### Data

-   row counts
-   orphan detection
-   duplicate detection
-   invalid status detection
-   missing required values
-   broken relationships
-   date/timestamp consistency

### Application

Test:

-   registration
-   authentication
-   enrollment
-   payments
-   applications
-   tasks
-   learning
-   submissions
-   interviews
-   certificates
-   notifications
-   admin workflows

## Backtest

Run the same business journeys before and after any schema change.

## Acceptance

No unexplained migration discrepancy remains.

------------------------------------------------------------------------

# 9. PHASE 5 --- DBERT Mailer Architecture Enforcement

## Objective

Make DBERT Mailer the sole email transport.

## Canonical endpoint

``` text
https://mailer.aivaratech.online/send
```

## Architecture

``` text
Portal / Website
      |
      | email request
      v
Application Email Service / Outbox
      |
      | authenticated HTTP API
      v
DBERT Mailer
      |
      +--> sender pool
      +--> rate limits
      +--> cPanel / SMTP
```

## Rules

Portal and website must not:

-   open SMTP connections
-   authenticate against mailboxes
-   rotate SMTP senders
-   implement cPanel mail delivery
-   use direct third-party email providers
-   report successful delivery when only a local placeholder executed

DBERT Mailer owns:

-   API authentication
-   sender selection
-   sender rotation
-   SMTP/SSL/STARTTLS
-   cPanel infrastructure
-   sender limits
-   global rate limits
-   delivery response
-   mail transport failure handling

## Documentation normalization

Replace obsolete references such as:

``` text
mailer.dbert.online
```

with:

``` text
https://mailer.aivaratech.online/
```

and:

``` text
https://mailer.aivaratech.online/send
```

Do not place real API keys or mailbox credentials in Git.

------------------------------------------------------------------------

# 10. PHASE 6 --- Complete Email Path Migration

## Objective

Find and migrate every application email path.

## Inventory

Search all relevant repositories:

``` bash
git grep -n -E 'send_email|send_mail|smtplib|SMTP|MIMEText|MIMEMultipart|Flask-Mail|mail\.send|CPANEL_EMAIL_API|EMAIL_PROVIDER|mailer'
```

Classify each path:

``` text
AUTH
OTP
PASSWORD_RESET
APPLICATION
APPLICATION_DECISION
ENROLLMENT
PAYMENT
INTERVIEW
TASK
SUBMISSION
CERTIFICATE
COHORT
ADMIN
NOTIFICATION
OTHER
```

## Required invariant

Every application email must converge on one application email
abstraction and one outbox mechanism.

## No duplicate implementation

Do not create:

``` text
PortalEmailService
WebsiteEmailService
AnotherMailer
LegacyMailer
DirectSMTPHelper
```

if the existing architecture can be extended safely.

Prefer the existing notification/outbox services.

## Acceptance

A static scan proves:

-   no direct SMTP in portal
-   no direct SMTP in website
-   no direct email provider
-   no placeholder-success production path
-   all email paths call the approved mailer abstraction

------------------------------------------------------------------------

# 11. PHASE 7 --- Email Outbox, Retry & Observability

## Objective

Make email delivery reliable and auditable.

## Required state machine

``` text
QUEUED
  ↓
SENDING
  ↓
SENT

SENDING → RETRYING → SENDING
              ↓
          DEAD_LETTER
```

## Store

At minimum:

-   event ID
-   event type
-   recipient
-   template
-   subject
-   source service
-   request/correlation ID
-   payload hash
-   attempt count
-   status
-   mailer response
-   sender if returned
-   created timestamp
-   updated timestamp
-   last error
-   next retry timestamp

## Idempotency

Duplicate events must not create duplicate transactional emails.

Use a durable unique event/idempotency key.

## Retry

Use bounded exponential backoff.

Do not retry permanent validation failures indefinitely.

## Tests

-   successful send
-   timeout
-   HTTP 429
-   HTTP 5xx
-   invalid API key
-   malformed mailer response
-   duplicate event
-   worker restart
-   dead-letter
-   retry recovery

------------------------------------------------------------------------

# 12. PHASE 8 --- `app.py` Decomposition Verification

## Objective

Reduce `apps/portal/app.py` to bootstrap responsibility.

## Target responsibilities

`app.py` should primarily contain:

-   app creation
-   configuration loading
-   extension initialization
-   blueprint registration
-   middleware
-   security headers
-   error handlers
-   startup/readiness hooks
-   minimal process bootstrap

## Move out

If still present:

-   business logic
-   SQL queries
-   payment logic
-   email logic
-   learning logic
-   certificate generation
-   file processing
-   application workflows
-   duplicate route logic
-   legacy helpers
-   large data structures unrelated to bootstrap

## Required method

For each candidate:

``` text
Search callers
↓
Identify replacement
↓
Run focused tests
↓
Remove
↓
Run import/startup test
↓
Run regression suite
```

## Acceptance target

`app.py` is substantially smaller and contains no duplicated business
implementation.

Do not enforce an arbitrary line-count target. Architectural
responsibility is the acceptance criterion.

------------------------------------------------------------------------

# 13. PHASE 9 --- Legacy / Dead Code Removal

## Objective

Remove obsolete code only after evidence.

## Search

-   unused imports
-   unreachable functions
-   duplicate services
-   old route implementations
-   obsolete environment variables
-   old provider integrations
-   old DB helpers
-   deprecated feature flags
-   abandoned migrations
-   stale docs

## Safety

Every deletion requires:

``` text
No caller
No import
No route registration
No template reference
No frontend API dependency
No test dependency
No deployment dependency
```

## Backtest

Run complete relevant suite after each logical deletion group.

------------------------------------------------------------------------

# 14. PHASE 10 --- Payment Security & State Machine

## Objective

Eliminate payment tampering, mismatched orders, replay and persistence
failures.

## Website findings to fix

### Server-authoritative pricing

Do not trust:

``` text
amount
```

from the client.

The server must resolve:

``` text
product/cohort/package → authoritative price
```

then create the Razorpay order.

### Order binding

Persist a payment-order record containing:

-   user
-   enrollment/application
-   product
-   amount
-   currency
-   Razorpay order ID
-   state
-   timestamps
-   idempotency key

### Verification

Verification must ensure:

``` text
submitted order ID == stored order ID
payment belongs to that order
payment belongs to the expected user/context
amount/currency are consistent
signature is valid
```

Use timing-safe signature comparison.

### Persistence

Do not report successful enrollment when payment succeeded but
enrollment persistence failed.

Use an explicit state machine and reconciliation path.

## Portal payment

Apply the same order-binding principles.

## Tests

-   modified amount
-   modified product
-   modified enrollment ID
-   modified joining date
-   modified domain
-   mismatched order/payment
-   duplicate verification
-   replayed signature
-   concurrent verification
-   webhook vs verification race
-   DB write failure after payment
-   already-paid order

------------------------------------------------------------------------

# 15. PHASE 11 --- Authentication, Authorization & IDOR

## Objective

Verify every object access is authorized.

## Audit

-   admin
-   company
-   mentor
-   student
-   interviewer
-   applicant
-   file owner
-   submission owner
-   enrollment owner
-   certificate owner

## Critical mentor rule

Role `mentor` alone must not grant access.

Authorization should prove:

``` text
mentor
  ↓
assigned student
  ↓
student resource
  ↓
specific task/submission/file
```

## Tests

Attempt:

-   user A accessing user B
-   mentor accessing unassigned student
-   student accessing another student's submission
-   company accessing another company's application
-   direct object-ID manipulation
-   unauthorized file download
-   privilege escalation

------------------------------------------------------------------------

# 16. PHASE 12 --- Guided Learning Transaction & Idempotency

## Objective

Make learning-session processing truly atomic and replay-safe.

## Known concern

`process_turn_atomic()` must not call lower-level methods that
independently commit before the outer operation finishes.

## Refactor

Use:

``` text
Route
  ↓
Application service
  ↓
single transaction
  ├── validate
  ├── load
  ├── generate/process
  ├── update mastery
  ├── record turn
  ├── update progress
  └── commit once
```

## Durable idempotency

Create a durable idempotency record keyed appropriately by:

``` text
student/session/request
```

Store:

-   request key
-   request hash
-   status
-   response
-   created timestamp
-   completed timestamp

## Concept tree

Ensure course/enrollment authorization is checked before exposing or
creating student-specific mastery state.

## Tests

-   normal turn
-   duplicate request
-   concurrent duplicate
-   model failure
-   DB failure
-   partial failure
-   transaction rollback
-   unauthorized course
-   stale session

------------------------------------------------------------------------

# 17. PHASE 13 --- Application & Enrollment State Machines

## Objective

Centralize state transitions.

## Rules

Routes must not directly mutate workflow status if a service/state
machine exists.

Example:

``` text
SUBMITTED
→ UNDER_REVIEW
→ APPROVED
→ ENROLLED
→ ACTIVE
→ COMPLETED
```

with explicit valid/invalid transitions.

## Tests

-   valid transition
-   invalid transition
-   repeated transition
-   unauthorized transition
-   concurrent transition
-   missing record
-   rowcount = 0

Never return success for a nonexistent object mutation.

------------------------------------------------------------------------

# 18. PHASE 14 --- Public API Abuse & Rate Limiting

## Audit

Public endpoints such as cohort/application APIs must have:

-   request validation
-   payload size limits
-   rate limiting
-   duplicate policy
-   anti-bot protection where appropriate
-   server-controlled allowlists
-   safe error messages

## Cohort rule

Do not accept arbitrary client-controlled cohort identifiers when the
server expects an allowlisted cohort.

If only `aivara` is active, enforce it server-side or use an explicit
allowlist.

## Tests

-   invalid cohort
-   huge payload
-   rapid repeated submission
-   duplicate application
-   malformed JSON
-   missing fields
-   unexpected fields
-   replay

------------------------------------------------------------------------

# 19. PHASE 15 --- File Security

## Objective

Harden uploads and downloads.

## Audit

-   MIME validation
-   extension validation
-   magic-byte validation
-   file size
-   filename normalization
-   path traversal
-   storage isolation
-   authorization
-   malware/security scanning integration if applicable
-   signed/controlled download URLs
-   deletion behavior

## Tests

-   executable disguised as PDF
-   double extension
-   path traversal
-   oversized file
-   malformed file
-   unauthorized download
-   deleted object
-   cross-user access

------------------------------------------------------------------------

# 20. PHASE 16 --- Silent Failure & Error Handling Audit

## Objective

Find places where the system reports success despite failure.

Search for:

``` text
except:
pass
return success
return 200
return 201
optional failure ignored
rowcount not checked
placeholder mode
fallback silently
```

## Known examples to inspect

-   email placeholder success
-   enrollment persistence after payment
-   admin status updates with zero affected rows
-   mailer failures
-   database failures
-   file processing
-   certificate generation

## Rule

Every externally visible success response must correspond to a verified
successful operation.

------------------------------------------------------------------------

# 21. PHASE 17 --- Frontend / Backend Contract Audit

## Objective

Ensure frontend assumptions match backend behavior.

For every API:

-   request schema
-   response schema
-   auth requirement
-   error schema
-   idempotency behavior
-   loading state
-   retry behavior
-   timeout behavior

## Website cohort

Ensure the frontend cannot select arbitrary server-sensitive cohort
values.

## Payment

Never rely on client-calculated price.

## Backtest

Run browser/API journeys for:

-   registration
-   application
-   payment
-   enrollment
-   login
-   dashboard
-   learning
-   submission
-   certificate

------------------------------------------------------------------------

# 22. PHASE 18 --- End-to-End User Journeys

## Required journeys

### Applicant

``` text
Visit
→ apply
→ confirmation email
→ admin review
→ decision email
→ enrollment
```

### Paid enrollee

``` text
Select package
→ authoritative price
→ create order
→ payment
→ verify
→ enrollment
→ receipt/email
```

### Student

``` text
Login
→ dashboard
→ course
→ guided learning
→ progress
→ task
→ submission
→ feedback
→ certificate
```

### Admin

``` text
Login
→ applications
→ approve/reject
→ enrollment
→ task review
→ certificate
→ notifications
```

### Email

For each journey verify:

``` text
event created
→ outbox
→ DBERT Mailer
→ accepted/sent
→ status recorded
```

------------------------------------------------------------------------

# 23. PHASE 19 --- Performance & Reliability

## Measure

-   API latency
-   DB query latency
-   connection pool usage
-   email queue latency
-   mailer latency
-   learning turn latency
-   concurrent sessions
-   error rate
-   retry rate

## Load tests

At minimum test representative:

-   authentication
-   dashboard
-   learning turn
-   payment creation
-   public application
-   admin list endpoints

Do not optimize by deleting functionality.

------------------------------------------------------------------------

# 24. PHASE 20 --- Production Deployment Verification

## Verify

### Database

-   PostgreSQL only
-   correct migrations
-   backup
-   restore procedure
-   connection health

### Mailer

-   `https://mailer.aivaratech.online/`
-   `/health`
-   `/send`
-   API key configured through secret storage
-   sender pool valid
-   rate limits configured
-   no exposed credentials

### Portal

-   startup
-   readiness
-   migrations
-   routes
-   workers
-   logs
-   environment variables

### Website

-   build
-   API routes
-   payment
-   cohort application
-   email

------------------------------------------------------------------------

# 25. PHASE 21 --- Final Security Regression

## Required scans

``` bash
git grep -n -i 'sqlite'
git grep -n -E 'sqlite3|internship\.db'
git grep -n -E 'smtplib|SMTP|Flask-Mail'
git grep -n -E 'mailer\.dbert\.online'
git grep -n -E 'send_email|send_mail'
```

Review every result.

## Secret scan

Check:

-   `.env`
-   API keys
-   SMTP passwords
-   database credentials
-   Razorpay secrets
-   JWT secrets
-   private keys

A tracked secret requires:

1.  credential rotation
2.  repository cleanup
3.  history cleanup where appropriate
4.  secret scan
5.  verification that the old credential is unusable

------------------------------------------------------------------------

# 26. PHASE 22 --- Final Release Gate

A release is allowed only if all are true.

## Architecture

-   [ ] PostgreSQL is the only runtime DB.
-   [ ] SQLite runtime references are zero.
-   [ ] `internship.db` is retired.
-   [ ] No direct SMTP outside DBERT Mailer.
-   [ ] All application email routes through DBERT Mailer.
-   [ ] Mailer endpoint is `https://mailer.aivaratech.online/`.
-   [ ] `app.py` contains bootstrap responsibilities only.
-   [ ] Duplicate legacy business logic removed.

## Security

-   [ ] No known secrets tracked.
-   [ ] Payment order binding implemented.
-   [ ] Payment replay protection implemented.
-   [ ] Authorization/IDOR audit passed.
-   [ ] File authorization passed.
-   [ ] Public API abuse controls passed.

## Reliability

-   [ ] Email outbox works.
-   [ ] Email retry works.
-   [ ] Dead-letter handling works.
-   [ ] Learning transactions are atomic.
-   [ ] Durable idempotency works.
-   [ ] DB failure behavior is explicit.
-   [ ] No silent success paths remain.

## Testing

-   [ ] Unit tests pass.
-   [ ] Integration tests pass.
-   [ ] API tests pass.
-   [ ] Security tests pass.
-   [ ] Negative tests pass.
-   [ ] Regression/backtests pass.
-   [ ] End-to-end journeys pass.
-   [ ] Production smoke tests pass.

## Documentation

-   [ ] Architecture docs updated.
-   [ ] Deployment docs updated.
-   [ ] Environment variables documented.
-   [ ] Mailer documentation updated.
-   [ ] Migration report stored.
-   [ ] Known limitations recorded.
-   [ ] Agent progress finalized.

------------------------------------------------------------------------

# 27. Required Verification Scripts

## `architecture_scan.sh`

``` bash
#!/usr/bin/env bash
set -euo pipefail

echo "== Database references =="
git grep -n -E 'sqlite|sqlite3|internship\.db' || true

echo "== Email transport references =="
git grep -n -E 'smtplib|Flask-Mail|SMTP|send_email|send_mail' || true

echo "== Mailer endpoints =="
git grep -n -E 'mailer\.dbert\.online|mailer\.aivaratech\.online' || true

echo "== Secret-looking files =="
find . \
  -path './.git' -prune -o \
  -name '.env' -print \
  -o -name '*.pem' -print \
  -o -name '*.key' -print
```

## `sqlite_scan.sh`

``` bash
#!/usr/bin/env bash
set -euo pipefail

if git grep -n -i -E 'sqlite|sqlite3|internship\.db'; then
  echo "SQLite references found."
  exit 1
fi

if find . -name 'internship.db' -o -iname '*sqlite*' | grep -v '^./.git/'; then
  echo "SQLite artifacts found."
  exit 1
fi

echo "SQLite scan passed."
```

## `email_transport_scan.sh`

``` bash
#!/usr/bin/env bash
set -euo pipefail

FAIL=0

if git grep -n -E 'smtplib|Flask-Mail|SMTP' -- 'apps/portal/**' 'apps/website/**'; then
  FAIL=1
fi

if git grep -n -E 'mailer\.dbert\.online' -- .; then
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  echo "Unauthorized email transport references found."
  exit 1
fi

echo "Email transport scan passed."
```

These scans must be adapted to the repository's actual shell/environment
if required.

------------------------------------------------------------------------

# 28. Executable Agent Command Template

The local agent should use a loop similar to:

``` bash
git status --short

cat .agent/CURRENT_PHASE.md
cat .agent/PROGRESS.json

# Inspect
git grep -n "TARGET_PATTERN"

# Implement
# ...

# Validate
git diff --check
pytest -q

# Backtest
pytest -q

# Record
# update .agent files

git status --short
git diff --stat
```

For frontend:

``` bash
npm ci
npm run lint
npm run test
npm run build
```

Use the repository's actual package-manager scripts where they differ.

------------------------------------------------------------------------

# 29. Required Phase Template

Every new phase entry in `.agent/CURRENT_PHASE.md` should use:

``` markdown
# Phase X — NAME

## Objective

## Current State

## Scope

## Files to Inspect

## Files to Modify

## Files That Must Not Be Touched

## Implementation Tasks

- [ ] Task 1
- [ ] Task 2

## Positive Tests

- [ ] Test 1
- [ ] Test 2

## Negative / Adversarial Tests

- [ ] Test 1
- [ ] Test 2

## Regression / Backtest

- [ ] Existing test suite
- [ ] Relevant user journey

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Exit Gate

PASS only when every mandatory criterion is satisfied.

## Files Changed

## Tests Run

## Failures

## Blockers

## Decisions

## Next Action
```

------------------------------------------------------------------------

# 30. Special Instructions for the AI Agent

## Never

-   invent an architecture that conflicts with the existing extracted
    services
-   rewrite large files without understanding dependencies
-   delete `app.py` code because it looks duplicated
-   delete SQLite before migration verification
-   create another email transport
-   hardcode secrets
-   trust client payment amounts
-   report payment success before durable persistence
-   return success for zero-row mutations
-   bypass authorization for convenience
-   mark a phase complete because code compiles
-   skip negative tests
-   skip regression testing
-   silently swallow errors
-   make broad unrelated refactors during a focused phase

## Always

-   inspect first
-   preserve working behavior
-   make focused changes
-   test after each logical change
-   run adversarial tests
-   backtest previous behavior
-   update agent state
-   document decisions
-   commit at stable gates
-   leave the repository in a resumable state

------------------------------------------------------------------------

# 31. Recommended Commit Strategy

Use focused commits:

``` text
phase-00: establish agent baseline
phase-01: document architecture and reachability
phase-02: enforce postgres-only runtime
phase-03: retire sqlite
phase-04: verify postgres migration integrity
phase-05: enforce DBERT mailer architecture
phase-06: migrate all email paths
phase-07: harden email outbox
phase-08: reduce app.py to bootstrap
phase-09: remove verified legacy code
phase-10: harden payment state machine
phase-11: harden authorization
phase-12: harden learning transactions
phase-13: centralize workflow state machines
phase-14: harden public APIs
phase-15: harden file security
phase-16: eliminate silent failures
phase-17: align frontend/backend contracts
phase-18: validate end-to-end journeys
phase-19: performance and reliability
phase-20: production verification
phase-21: security regression
phase-22: release gate
```

Do not combine unrelated phases into one giant commit.

------------------------------------------------------------------------

# 32. Final Definition of Done

The DBERT LMS is considered technically ready only when the repository
can demonstrate:

``` text
                 ┌──────────────────────┐
                 │      DBERT LMS       │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │   Routes / APIs      │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │ Services / Domain    │
                 └──────┬─────────┬─────┘
                        │         │
              ┌─────────▼───┐ ┌──▼──────────────┐
              │ PostgreSQL  │ │ Email Outbox    │
              │ ONLY        │ │ / Notifications │
              └─────────────┘ └──────┬──────────┘
                                     │
                            ┌────────▼─────────┐
                            │ DBERT Mailer     │
                            │ aivaratech.online│
                            └────────┬─────────┘
                                     │
                            ┌────────▼─────────┐
                            │ cPanel / SMTP    │
                            └──────────────────┘
```

The final repository must have:

-   one authoritative runtime database: PostgreSQL
-   one authoritative application email transport: DBERT Mailer
-   one coherent service architecture
-   a lean bootstrap `app.py`
-   no unverified legacy code
-   no silent critical failures
-   durable payment and learning state
-   authorization enforced at object level
-   repeatable tests
-   repeatable security scans
-   phase-by-phase progress tracking
-   a clear recovery path for interrupted AI-agent sessions

**The agent must never claim completion without evidence from tests,
scans, migration checks, and the phase exit gate.**
