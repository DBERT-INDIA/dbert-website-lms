# DBERT Platform QA Audit and Phase-by-Phase Development Plan

**Audit date:** 10 November 2026 (IST)  
**Repository:** `C:\Users\user\Desktop\dbert-website-lms`  
**Production host:** `ubuntu@3.26.237.171` (`/var/www/dbert-website-lms`)  
**Audit mode:** Read-only against EC2. No production files, databases, services, queues, or user records were changed.

> **Execution handoff:** The next AI agent should treat this document as the active remediation goal. Start with Phase 0, preserve every existing local and production change, resolve the P0 items, then proceed in order. Do not reset, clean, pull over, or deploy from either dirty checkout until its changes and data have been inventoried and protected.

## 1. Executive Summary

The public website and API respond, and all four documented EC2 services were active during the audit. The production LMS is **not fully healthy**: its readiness endpoint returns HTTP 503 against the live PostgreSQL database, and production logs show repeated failures in outbound email delivery. The top-level LMS liveness endpoint still returns 200, so a green liveness check alone is not sufficient evidence that the LMS is ready to serve critical work.

The deployment state is difficult to reproduce safely. EC2 is at commit `c98c8bc`, three commits behind local `HEAD` (`425ce9d`), and the EC2 checkout has 129 dirty/untracked paths. The local checkout has 580 status entries, including 258 apparent vendored dependency deletions, 246 untracked paths, and 77 modified tracked files. These are material release and data-integrity risks; there is no clean source snapshot from which to assume the running service can be rebuilt.

The local website production build completed successfully, including TypeScript and 117 static page generations. It logged that Razorpay keys were missing from the local build environment. The full portal test suite cannot currently be considered green: collection stops because Playwright and `axe_playwright_python` are missing. A focused run completed 39 tests and failed 2 PostgreSQL adapter simulation tests because their mock cursor does not implement the context manager required by the adapter. More importantly, the live PostgreSQL readiness failure is not represented by those SQLite-centric health checks.

### Immediate disposition

1. Treat LMS email as **degraded/unreliable** until the formatter import, primary SMTP connection, and fallback mailer DNS are repaired and delivery is confirmed by provider/outbox evidence.
2. Treat LMS `/ready` as **broken** until it uses database-aware checks and returns 200 against the deployed PostgreSQL service.
3. Freeze deployment actions until local and EC2 changes have been captured and reconciled. Do not overwrite either dirty tree.
4. Correct the stipend date fail-open and AI failure-to-approval behavior before relying on those eligibility signals.

## 2. Audit Scope and Evidence

### Inspected

- Local Git state, recent commits, relevant modified code, route definitions, database adapter, health checks, stipend/verification and AI evaluation paths, environment templates, API Compose configuration, and existing QA files.
- Read-only EC2 state over the documented SSH connection: deployed commit, dirty-file count, active services, disk usage, systemd liveness, recent sanitized portal errors, and public GET route status.
- Public HTTP checks for `dbert.in`, `lms.dbert.in`, and `api.dbert.in`.
- Existing local checks: website production build; portal test collection; focused portal observability/database adapter tests; whitespace check.

### Not inspected or not performed

- No database rows, applicant records, secrets, payment transactions, SMTP messages, or authenticated user workflows were read or changed as part of the audit.
- No direct PostgreSQL session, backup/restore drill, authenticated browser journey, payment, mail send, or live write test was run.
- Production log evidence below is limited to sanitized error categories and the relevant exception messages. No full logs or private message bodies are included.
- Public GET status checks establish reachability, not correctness of authenticated or state-changing flows.

## 3. Snapshot Results

### 3.1 Repository and release state

| Check | Result | Interpretation |
|---|---|---|
| Local branch / HEAD | `main` / `425ce9d` | Local is at the most recent observed feature commit. |
| EC2 deployed HEAD | `c98c8bc` | Three commits behind local `HEAD`. |
| Local working tree | 580 status entries: 77 modified, 246 untracked, 258 deleted | High risk of accidental omission or inclusion in a future commit/deployment. |
| Local vendored files | 258 paths appear deleted under `apps/portal/vendor/` | Filesystem access to these directories is denied in this audit environment. Confirm whether actual file removal or ACL/checkout damage before any Git operation. |
| EC2 working tree | 129 dirty/untracked paths: 71 modified and 58 untracked | Live checkout is not a reliable deployment source or rollback point until preserved and reconciled. |
| Local `.git` whitespace check | No actionable whitespace errors reported | Does not validate app correctness. |

The local working tree includes application code, candidate/certificate registries, dispatch state, deployment/verification scripts, and other operational files. Keep sensitive records out of the audit log and handle them under the repository’s data/secret rules.

### 3.2 Production service and route checks

| Surface | Observation |
|---|---|
| `dbert-website.service` | Active |
| `dbert-portal.service` | Active |
| `dbert-api.service` | Active |
| `nginx.service` | Active |
| EC2 root filesystem | 36% used (18 GB available of 29 GB) |
| Website `/`, `/verify/directory`, `/dbert-online`, `/enroll/1999` | HTTP 200 |
| Website `/verify/` | HTTP 308 (canonical slash redirect) |
| Website `/api/verify` and `/api/enroll/lookup` | HTTP 200 for read-only sample requests |
| LMS `/`, `/health` | HTTP 200 |
| LMS `/ready` | **HTTP 503**; DB connection check is true, while schema/outbox/WAL checks are false. PostgreSQL reports that `sqlite_master` does not exist. |
| LMS `/stipend/tasks` and `/portal` without a session | HTTP 302 (authentication redirect) |
| LMS `/intern/login` with GET | HTTP 405; this is a POST-only login handler, so this probe is not evidence of a defect. `/login` is not a registered route and returned 404. |
| API `/health`, `/ready`, `/status`, `/docs` | HTTP 200; `/ready` reports database connected. |
| Served website GA4 ID | `G-MN7ME9X518`, as required by repository instructions. |

### 3.3 Local verification

- `npm run build` under `apps/website`: **passed**. Next.js compiled, TypeScript completed, and 117 static pages generated. The build logged `Razorpay keys are missing from environment variables`; the local environment therefore did not prove payment configuration.
- Full `python -m pytest apps/portal/tests`: **blocked during collection** by missing `playwright` and `axe_playwright_python` packages in browser/a11y test modules.
- Focused `test_observability.py` + `test_database_abstraction.py`: **39 passed, 2 failed**. The two failures are PostgreSQL adapter simulation tests whose mock cursor does not support the context manager used by `_configure_pg_schema`. Update the mock and retain a real PostgreSQL integration check; do not dismiss the production readiness defect as a mock-only issue.

## 4. Findings by Priority

### P0 — Fix immediately

#### P0.1 — LMS outbound email path has a deterministic `NameError` and failed transports

- **Evidence:** `apps/portal/app.py:28` imports `formatdate` and `make_msgid`, but `_smtp_send_raw` calls `formataddr` at line 4361. `formataddr` is not imported in this module. The same call exists at line 4363.
- **Live evidence:** Sanitized EC2 portal logs contain repeated `NameError: name 'formataddr' is not defined`. The same 24-hour window contains primary SMTP `SMTPServerDisconnected: Connection unexpectedly closed` and cPanel fallback DNS failures resolving `mailer.aivaratech.online`.
- **Impact:** Any path using this sender pool can fail before sending. Primary SMTP and the fallback are also independently failing, so fixing only the import will not establish delivery. Password activation/reset, applicant notifications, and other LMS mail may be affected depending on which sender path each uses.
- **Fix:** Import the correct formatter or use the centralized `services/delivery_service.py` implementation; validate the primary host/port/auth from EC2; repair or remove the unreachable fallback; make failed sends observable and retry-safe via the outbox. Never mark a message sent solely because a send was queued or an exception was swallowed.
- **Acceptance:** Unit test sender formatting; test primary and fallback with deterministic mocks; perform a separately authorized controlled canary only after config/DNS is verified; reconcile provider message ID, outbox state, and delivery tracking. No duplicate canary or candidate messages.

#### P0.2 — LMS PostgreSQL readiness probe is SQLite-only and fails in production

- **Evidence:** `apps/portal/services/telemetry_service.py:202-260` always runs `PRAGMA journal_mode` and queries `sqlite_master`. The deployed adapter correctly ignores PostgreSQL PRAGMAs, but the catalog query then fails. Live `https://lms.dbert.in/ready` returns 503 with `database_connected: true`, and the error names the missing relation `sqlite_master`.
- **Impact:** The service advertises itself as unready despite a successful DB connectivity check. Any deployment controller, health monitor, or load balancer that uses this route may withdraw the LMS. Current systemd and public liveness remained active, which does not make readiness safe.
- **Fix:** Branch on the selected database adapter/engine. For PostgreSQL, verify required relations through the adapter’s `table_exists` or PostgreSQL catalog, check the outbox with portable SQL, and do not require SQLite WAL mode. Keep WAL verification only for SQLite. Include the failing check/error in a structured response without exposing connection details.
- **Acceptance:** SQLite readiness tests continue to pass; PostgreSQL readiness runs against a disposable PostgreSQL instance and production `/ready` returns HTTP 200 with all applicable checks true. A genuine DB outage still returns 503.

#### P0.3 — Unsafe release state on both sides

- **Evidence:** Local `HEAD=425ce9d`; EC2 `HEAD=c98c8bc` (3 commits behind). EC2 has 129 dirty/untracked paths. Local has 580 status entries, including 258 vendor deletions whose directories are inaccessible here.
- **Impact:** A deployment from the local tree may omit undocumented EC2 hotfixes or include unrelated data/scripts; a deployment from EC2 may include uncommitted production-only edits and no reproducible revision. A commit could unintentionally delete runtime dependencies.
- **Fix:** Phase 0 must inventory, checksum, and back up both working trees, identify and preserve production-only edits, resolve local vendor ACL/removal state, compare tracked/untracked content without printing secrets or candidate PII, and create a clean reviewed release artifact from a named commit. No `reset --hard`, `clean`, broad copy, or rebuild-in-place during reconciliation.
- **Acceptance:** A signed/recorded release commit and artifact digest are agreed; all differences are classified; backup and rollback artifacts are verified; no unexplained dirty production changes remain before deployment.

### P1 — Correctness, eligibility, and trust risks

#### P1.1 — Missing completion data currently passes the stipend completion gate

- **Evidence:** `apps/portal/services/certificate_service.py:292-299` returns `is_completed: True` when no enrollment date or registry end date can be found (`source: "none"`).
- **Impact:** For an otherwise verified candidate with a linked UPI account, missing/corrupt completion data can satisfy the business-rule gate and permit a stipend submission before the required completion date.
- **Fix:** Represent missing date as `unknown` / `is_completed: false`; show a review-needed state. Keep the joining-date + 60-day rule and registry fallback explicit, use a defined business timezone, and log/reconcile records with no date.
- **Acceptance:** Tests cover missing, malformed, future, exact-boundary, timezone/day-boundary, and valid fallback dates. Unknown never unlocks submission.

#### P1.2 — AI evaluation errors are converted into an approval recommendation

- **Evidence:** `apps/portal/services/ai/stipend_evaluator.py:263-272` catches all evaluation/parsing exceptions and returns score 75 with verdict `RECOMMENDED_APPROVE`. `apps/portal/routes/stipend.py:213-228` persists the returned verdict as evaluation status. The endpoint has a separate manual-review fallback only if the evaluator raises, but the evaluator catches its own failure, so that outer fallback will not run.
- **Impact:** An AI outage or malformed model response can be displayed, emailed, and stored as a positive AI recommendation even though no evaluation succeeded. Human staff may remain the final authority, but the false signal is unsafe and defeats accurate auditing.
- **Fix:** Use an explicit neutral result such as `AI_FAILED_MANUAL_REVIEW`, a nullable score, and the original failure category. Validate score bounds, required rubric dimensions, and verdict enum before persisting. Never synthesize a passing score or approval from a failed parse/network call.
- **Acceptance:** Inject timeout, 429, invalid JSON, missing score, out-of-range score, unknown domain, and empty response. Each results in a visible, auditable manual-review state and never an approval recommendation.

#### P1.3 — Public activation flow permits enumeration and account creation side effects

- **Evidence:** `apps/portal/routes/stipend.py:292-335` accepts an unauthenticated email, looks up the certificate registry, creates an LMS account if missing, invalidates older reset tokens, and sends an activation message. It returns distinct 404 vs success responses and echoes the address. The GET flow in `stipend_tasks()` at lines 33-50 also creates an account for a registry-matching `?email=` request.
- **Impact:** The public interface can reveal whether an address belongs to a credential holder, cause unsolicited activation messages, and create account records without proving mailbox ownership. Email sending currently also fails in production.
- **Fix:** Make response shape/status enumeration-resistant, rate-limit by IP and normalized email, require a verified one-time activation token before account creation/activation, queue email transactionally, and avoid public account creation from a GET page view. Review CSRF protections and token expiry/use checks.
- **Acceptance:** Unknown and known addresses return indistinguishable public responses; repeated requests are throttled; account creation occurs only after token verification; activation tokens are single-use, hashed at rest, and expire; email failure leaves a retryable outbox record.

#### P1.4 — Stipend submission lacks a visible server-side duplicate guard

- **Evidence:** The dashboard queries and displays an existing submission at `apps/portal/routes/stipend.py:100-112`, but the POST handler at lines 128-246 does not check for an existing active submission before inserting another row.
- **Impact:** Double-clicks, retries, and browser resubmits can create multiple review queue entries for the same intern/task. This increases the risk of duplicate staff action and payout; the financial release path must be audited before assuming ledger idempotency protects it.
- **Fix:** Define a business idempotency key/unique constraint for intern + stipend task + submission lifecycle; implement a transaction-safe duplicate response and a deliberate resubmission/version path after staff requests revision. Audit stipend decision/payout for a unique source-submission ledger key.
- **Acceptance:** Concurrent duplicate POSTs create one active submission; intentional resubmission is versioned; repeated staff approval cannot credit a second 5,000-coin award.

#### P1.5 — PostgreSQL-specific production still contains SQLite-only access patterns

- **Evidence:** In addition to the live readiness failure, the local source has SQLite catalog/PRAGMA use in `apps/portal/app.py:7315` and `apps/portal/services/integrity_service.py` (including table and column inspection around lines 24, 103, and 118). `PostgreSQLAdapter.execute()` translates placeholders/SQLite syntax and ignores PRAGMA, but raw `sqlite_master` is not a PostgreSQL catalog.
- **Impact:** Admin integrity, diagnostics, or other conditional routes can fail only on the production PostgreSQL path while SQLite tests pass. Some handlers may catch and suppress the failure, leaving incomplete dashboards or skipped repairs.
- **Fix:** Search all application/runtime code for `sqlite_master`, `PRAGMA`, SQLite-only `lastrowid`, and schema assumptions. Replace with adapter capability methods or explicit dialect branches. Do not make blanket SQL substitutions without testing translation and transaction behavior.
- **Acceptance:** Route/service coverage for every discovered call site on SQLite and PostgreSQL; error-path assertions verify failures are surfaced instead of returned as empty success.

#### P1.6 — Fail-open anti-bot verification

- **Evidence:** `apps/portal/app.py:905-921` documents Turnstile disabled by default and returns `True` when the configured verification service raises an exception.
- **Impact:** When enabled, network failure accepts submissions as if verification passed. When disabled, the check is not a security control at all. This can admit automated application traffic during a provider outage.
- **Fix:** Decide per route whether a challenge is mandatory. For abuse-sensitive application/activation actions, fail closed or use a separately logged, rate-limited fallback; do not treat provider outage as successful verification. Preserve a deliberate availability policy for low-risk routes.
- **Acceptance:** Tests cover disabled, missing secret/token, provider rejection, timeout, malformed response, and valid response. Every route’s behavior matches its documented policy and emits telemetry.

### P2 — Maintainability, security posture, and quality-system gaps

#### P2.1 — Credential encryption falls back to bespoke XOR and embedded fallback secrets

- **Evidence:** `apps/portal/app.py:960-992` derives a Fernet key from a Flask secret or a hard-coded fallback, then falls back to custom XOR/HMAC stream construction if Fernet fails. The write path’s fallback construction does not authenticate the ciphertext. Decryption tries multiple legacy/hard-coded keys at lines 1003-1030.
- **Impact:** If the intended crypto dependency/configuration is missing, sensitive Gemini configuration can be stored using a non-standard, unauthenticated format. Embedded compatibility keys expand the compromise surface and make rotations ambiguous.
- **Fix:** Require a dedicated secret-manager-provided Fernet key for encrypted values; fail startup/health checks if required encryption is unavailable. Provide a one-time migration for legacy values, remove fallback writers and hard-coded keys, and audit the UPI encryption path separately.
- **Acceptance:** No plaintext/default-key write path; encryption round-trip, tamper rejection, key rotation, and migration tests pass. Health checks distinguish “configured” from “decrypts existing data.”

#### P2.2 — The portal test fixtures broadly disable CSRF checks

- **Evidence:** `apps/portal/tests/conftest.py` adds a long list of endpoint names to `CSRF_EXEMPT_ENDPOINTS` for all tests.
- **Impact:** Most route tests bypass the protection expected in production. A passing functional test does not prove that a real form/client sends and validates CSRF tokens, and test-global mutation can leak between tests.
- **Fix:** Test CSRF by default with session/form/header tokens. Add a narrowly scoped fixture only for cases that are explicitly testing logic independent of CSRF, and restore global state after each test. Keep webhook exemptions narrowly documented.
- **Acceptance:** Security tests prove missing/invalid token is rejected and valid token accepted for each state-changing route; no suite-wide CSRF bypass.

#### P2.3 — QA environment and PostgreSQL coverage are insufficient

- **Evidence:** Full suite collection is missing `playwright` and `axe_playwright_python`. Focused tests have 2 failures due mock cursor behavior. The live PostgreSQL readiness bug escaped existing tests. Website build succeeds but reports absent Razorpay environment keys.
- **Fix:** Pin and install test dependencies in a reproducible CI image; use a PostgreSQL service container for adapter, schema, health, and critical route tests; update the adapter mock contract. Make release preflight verify required payment/email/encryption configuration without printing secret values.
- **Acceptance:** CI collects the full suite with no missing modules; SQLite and PostgreSQL jobs pass; `npm run build` passes with all intended public build-time variables; separate secret/config checks fail with actionable variable names only.

#### P2.4 — API Compose defaults are unsafe and partially inconsistent

- **Evidence:** `dbert-api-package/docker-compose.yml` supplies a known default PostgreSQL password when `POSTGRES_PASSWORD` is omitted. The backend `DATABASE_URL` hardcodes username `dbert_user`, while the database user is configurable through `POSTGRES_USER`. `dbert-api-package/.env.example` includes a default admin password and wildcard CORS setting.
- **Impact:** A quick deployment without overriding defaults can start with predictable credentials. Customizing the DB user can make backend and DB credentials disagree. Wildcard CORS is easy to carry into an unintended deployment.
- **Fix:** Require non-empty generated values (no production defaults), derive both DB and backend credentials from the same variables, validate CORS origins by environment, and add a startup config guard that refuses unsafe production values.
- **Acceptance:** Compose fails closed when required secrets are absent; custom database/user names connect correctly; production config rejects wildcard CORS unless explicitly reviewed.

#### P2.5 — Local vendored dependency paths are inaccessible / appear deleted

- **Evidence:** Git reports 258 deletions under `apps/portal/vendor/`; attempts to enumerate/read the package directories return access denied, while the root listing shows the vendor directory. This may be ACL damage rather than deliberate removal.
- **Impact:** A commit can record dependency deletions or packaging may omit runtime modules. A normal `git diff` review is incomplete while paths cannot be read.
- **Fix:** Resolve ownership/ACL or restore vendor files from the correct lock/requirements source in an isolated clone. Decide whether vendored packages are an intended deployment artifact. Prefer pinned wheels/requirements or a reproducible build over committing opaque vendor state.
- **Acceptance:** Git status for vendor is clean or intentional and documented; build/package includes all runtime dependencies; clean environment install and portal startup pass.

## 5. Phase-by-Phase Development Plan

### Phase 0 — Preserve state and define the release source (blocking)

**Objective:** Create a safe, reviewable baseline before code or deployment changes.

1. Record local and EC2 branch, commit, `git status --porcelain`, and hashes for modified tracked files. Do not print `.env`, private keys, payment credentials, or candidate rows.
2. Make a read-only backup of EC2 application files and databases using the existing operational runbooks; separately verify backup completion and restore readability. Preserve uploads, SQLite/PG data, JSON ledgers/registries, and queue state according to their storage location.
3. Resolve the local vendor ACL issue. Determine whether vendor files were deleted, are inaccessible, or are merely blocked by inherited Windows permissions. Preserve all untracked local scripts/data before cleanup decisions.
4. Compare EC2’s 129 changed paths with local changes and commits. Classify each as production hotfix, generated/operational artifact, sensitive data, or stale/unneeded file. Bring legitimate hotfixes into reviewed source control; keep live data out of source commits.
5. Produce one clean release branch/worktree and immutable build artifact. Record commit SHA, artifact hash, dependency lock hashes, and required runtime environment variable names.

**Exit criteria:** Approved source snapshot; backups are verifiably readable; local and EC2 deltas are classified; no unknown edits will be overwritten; rollback artifact is named and available.

### Phase 1 — Restore email delivery and make failures explicit (P0)

**Objective:** Restore the LMS’s transactional email path without duplicate sends or false success.

1. Fix the `formataddr` missing import or route all messages through the centralized delivery service; avoid maintaining two subtly different senders.
2. From EC2, validate the configured primary SMTP hostname, TLS mode, port, credentials presence, provider quota, and network reachability. Do not print credential values.
3. Validate fallback DNS and HTTP/TLS health for the cPanel mailer. If it is no longer a supported host, remove it from fallback order and configure a known working provider.
4. Trace the delivery service’s result object, caller exception handling, retry state, and outbox transitions. Persist provider response/message ID, timestamps, attempts, and terminal error category. Confirm retry uses a stable idempotency key.
5. Audit all email callers used for account activation/reset, application updates, stipend submission, and staff decisions. Replace direct/background sends that can lose exceptions or report success on failure.
6. Add tests for missing formatter, SMTP disconnect, DNS failure, quota response, provider timeout, fallback success, total failure, retry, and duplicate delivery prevention.
7. After config validation and explicit operational authorization, perform one controlled canary to a designated internal recipient; reconcile application outbox, provider response, and inbox receipt.

**Exit criteria:** Canary is delivered exactly once; no `formataddr` NameError; fallback does not point to an unresolved host; failed deliveries remain retryable and visible; production monitoring alerts on sustained failure.

### Phase 2 — Correct health/readiness semantics for PostgreSQL (P0)

**Objective:** Make liveness and readiness describe the actual active database and dependencies.

1. Add adapter-level engine reporting and portable table existence checks.
2. Refactor `check_readiness()` to run engine-appropriate probes. PostgreSQL must not be required to expose SQLite WAL mode or `sqlite_master`.
3. Check required relations in the configured schema, verify the event outbox can be queried, and report pending/dead-letter thresholds separately from connectivity.
4. Keep liveness lightweight and independent of DB. Make readiness return 503 only for actual required dependency failures.
5. Add SQLite and PostgreSQL tests including connection failure, missing relation, outbox query failure, dead-letter threshold, and dialect-specific WAL applicability.
6. Add a deployment smoke gate that checks `/health` and `/ready` and inspects structured check fields.

**Exit criteria:** Live LMS `/health` returns 200; `/ready` returns 200 with PostgreSQL checks true; simulated DB/schema outage returns 503 with accurate reason; no SQLite catalog exception appears in logs.

### Phase 3 — Close eligibility and credential lifecycle fail-open paths (P1)

**Objective:** Enforce certificate, completion, and account ownership rules consistently.

1. Change missing/malformed completion dates from eligible to ineligible/review-required. Make the business timezone explicit and test exact date boundaries.
2. Audit `CertificateService.is_intern_verified()` for DB exceptions and registry fallback. Define behavior when DB is unavailable, registry is unreadable, the newest record is provisional, duplicate email records exist, or registry and DB disagree.
3. Remove account creation side effects from public GET views. Require mailbox token ownership before creating/activating an account.
4. Make activation endpoints enumeration-resistant and rate-limited. Use hashed, one-time, expiring tokens and generic public responses. Ensure mail failure is an outbox retry rather than an unhandled 500 or lost activation.
5. Add state transition tests for candidate types: verified, provisional, revoked/missing, duplicate certificate, no account, existing locked account, expired token, reused token, and data-source outage.

**Exit criteria:** Every unknown or inconsistent eligibility input denies submission and presents a review state; no public request creates an account before proof of email ownership; identity changes are auditable.

### Phase 4 — Make stipend evaluation and payout review safe under retries

**Objective:** Ensure AI is advisory, submission state is idempotent, and staff approval cannot double-credit.

1. Replace AI fabricated score/approval defaults with explicit neutral/manual-review states. Validate strict result schema and allowed status values before persistence.
2. Normalize domains through one canonical map shared by task selection and evaluator rubrics; unmatched domains should route to human review.
3. Add submission idempotency, unique source identifiers, and a deliberate revision-request lifecycle. Make concurrent duplicate POSTs safe.
4. Audit staff approval/rejection transaction boundaries, ledger uniqueness keys, balance updates, notifications, and retries. Approval and the one-time 5,000-coin credit must be atomic or recoverable with a ledger-driven outbox.
5. Add failure-injection tests at each boundary: upload failure, evaluator timeout, DB insert/commit failure, email failure, approval retry, ledger conflict, and notification retry.
6. Validate PDF uploads by size, extension, MIME/magic bytes, parser success, and safe storage path. Ensure access is authenticated and uploads are not rendered inline unsafely.

**Exit criteria:** AI failures never look like approval; one active submission per idempotency key; approval retry cannot duplicate credit; all failures have a recoverable state and user-facing response.

### Phase 5 — Remove database dialect leaks and establish PostgreSQL parity

**Objective:** Eliminate SQLite-only behavior from PostgreSQL production routes.

1. Search runtime modules for SQLite catalog references, PRAGMAs, SQLite-only date functions, raw connection assumptions, positional result-shape assumptions, and `lastrowid` use.
2. Replace application service introspection with adapter methods; identify missing adapter operations and add a documented interface rather than ad hoc SQL in route modules.
3. Audit every `except: pass`, `except Exception: return None/default`, and swallowed transaction failure in runtime code. Add structured logs/counters and only retain deliberate optional behavior with a visible degraded state.
4. Verify transaction commit/rollback behavior in nested helper flows; PostgreSQL’s aborted-transaction behavior must not be mistaken for an empty result.
5. Run route and service suites against SQLite and real disposable PostgreSQL, including integrity dashboard, stipend gates, certificate auto-heal, startup reconciliation, mentor capacity booking, and outbox.

**Exit criteria:** All discovered dialect-specific calls are adapted or documented as SQLite-only; no runtime exception is swallowed into a success-shaped response; PostgreSQL and SQLite jobs pass their declared contract suites.

### Phase 6 — Security and privacy hardening

**Objective:** Reduce abuse, secret, and personal-data risks without breaking normal user journeys.

1. Remove bespoke XOR fallback encryption and embedded key compatibility. Require dedicated encryption keys and document rotation/migration.
2. Replace suite-wide CSRF exemptions in tests with real tokens. Review route exemptions and ensure state-changing endpoints have authorization, CSRF, rate limits, and audit logs.
3. Review public registry lookup, enrollment lookup, activation, stipend pages, certificate APIs, admin health, and file downloads for email/certificate enumeration, IDOR, cache exposure, and PII over-return.
4. Confirm all uploads are outside executable/public paths where possible, bounded, scanned/validated, and accessed through authorization-checked routes.
5. Review API CORS and environment templates: remove predictable production defaults; enforce secrets; align Compose database URL variables; ensure wildcard CORS cannot be accidentally promoted to production.
6. Verify cookie flags, trusted proxy configuration, HTTPS-only links, rate-limit persistence across workers, and account recovery behavior.

**Exit criteria:** Security regression tests exercise real CSRF/auth behavior; no known default production credentials; encryption failure is closed and visible; high-risk public endpoints are rate-limited and enumeration-resistant.

### Phase 7 — Repair QA, test repeatability, and coverage

**Objective:** Make future regressions visible before a release reaches EC2.

1. Add pinned test dependencies (including Playwright and accessibility tooling) to a documented CI/test setup.
2. Update PostgreSQL adapter mock cursor context-manager support; retain unit tests for translation and a PostgreSQL service-container integration job.
3. Add tests for all P0/P1 cases above and service error-injection. Include readiness as a PostgreSQL test so the exact production bug cannot recur.
4. Add build/config preflight for website and API payment variables, without requiring secret values in logs or artifacts.
5. Run route smoke checks for canonical redirects, enrollment lookups, certificate verification, directory, LMS auth, stipend lock/unlock, API health/readiness, and main protected routes. Use test identities and no live write operations.
6. Add a baseline dependency vulnerability/license scan and remove unsupported/unneeded duplicate vendor trees after the deployment packaging decision is documented.

**Exit criteria:** Full test collection succeeds; SQLite and PostgreSQL suites pass; Next.js production build passes; required config is validated; QA artifacts link to exact commit and environment.

### Phase 8 — Controlled production deployment and rollback validation

**Objective:** Deploy only a reviewed artifact and prove all critical routes remain healthy.

1. Follow repository `AGENTS.md` deployment procedure for website changes and the documented portal/API runbooks for their respective services. Do not copy from a dirty tree.
2. Verify artifact checksum and required environment variable *presence* before activation. Back up current deployment and data first.
3. Deploy application artifacts separately from stateful data. Never replace live DBs, ledgers, uploads, or candidate state with local copies.
4. Run the read-only post-deploy route matrix and verify HTTP status, redirect behavior, response schema, service state, readiness, GA4 ID, canonical domain, and migration notice.
5. Check journal error rates and outbox/delivery state after deployment. A 200 page response does not pass the release if `/ready` fails or email is broken.
6. Keep rollback pointed at the preserved known-good artifact. Roll back application code if health, ready, core workflow, or delivery checks regress; do not roll back data without a separately verified data recovery plan.

**Exit criteria:** All four systemd services active; website, LMS, and API critical routes pass; LMS `/ready` is 200; a separately authorized mail canary is confirmed; no new severe runtime errors; rollback package is retained.

### Phase 9 — Operational monitoring and architecture upgrades

**Objective:** Prevent silent failures and reduce the ongoing cost of operating a mixed legacy stack.

1. Alert on liveness/readiness divergence, SMTP provider failure, growing outbox/dead-letter queues, DB pool saturation, exception spikes, and recent deployment SHA drift.
2. Create a daily deployment consistency report comparing Git SHA, artifact digest, active service version, and dirty working tree state.
3. Add structured request IDs and consistent error classes across Flask, Next.js route handlers, FastAPI, and background dispatchers. Do not log secrets, access tokens, payment credentials, or unnecessary candidate data.
4. Document a supported source of truth for candidate/certificate data and reconcile website JSON, portal PostgreSQL, and external ledgers with checksums and explicit conflict policy.
5. Plan incremental decomposition only after parity tests and operational controls exist. Keep the current LMS usable while moving bounded domains (identity, credentials, payments, messaging) behind stable APIs; avoid a big-bang rewrite.

**Exit criteria:** Alerts are tested, deployment drift is visible, core metrics are available, and future architecture work has a migration/rollback plan backed by compatibility tests.

## 6. Recommended Work Order and Stop Conditions

1. Phase 0 state preservation must finish before any deploy, reset, or broad file copy.
2. Fix P0.1 email code/config and P0.2 readiness in isolated, reviewed changes. Validate both locally and in staging or controlled canary before EC2.
3. Resolve P1.1 completion fail-open before enabling/announcing stipend submission eligibility.
4. Resolve P1.2 AI approval fallback and P1.4 duplicate submission/payout handling before issuing new stipend decisions.
5. Continue security, database parity, and QA phases before expanding portal/API features.
6. Stop deployment if there are unexplained dirty paths, a failed backup, missing required secrets/config, failed readiness, unverified migration counts, or unresolved rollback gaps.

## 7. Suggested First-Run Commands for the Next Agent

Run these from the appropriate checkout, capture output without secrets, and do not run destructive cleanup:

```text
git rev-parse HEAD
git status --short --branch
git diff --stat
git diff --check
```

On EC2, start with read-only inspection and backup verification before touching service files:

```text
hostname
git rev-parse --short HEAD
git status --short
systemctl is-active dbert-website.service dbert-portal.service dbert-api.service nginx.service
curl -fsS https://lms.dbert.in/health
curl -fsS https://lms.dbert.in/ready
curl -fsS https://api.dbert.in/health
curl -fsS https://api.dbert.in/ready
```

Run local checks after a clean review branch is prepared:

```text
npm --prefix apps/website run build
python -m pytest apps/portal/tests/test_observability.py apps/portal/tests/test_database_abstraction.py -q
python -m pytest apps/portal/tests -q
```

The full portal suite requires the missing browser/a11y packages observed during this audit. The focused database tests also need their PostgreSQL mock cursor corrected or replaced with a real PostgreSQL integration fixture.

## 8. Audit Conclusion

Production is reachable but **not ready for an unqualified “healthy” sign-off**. The website and API sampled routes passed, while the LMS has a reproducibly failing PostgreSQL readiness probe and recurring email delivery exceptions. The current source/deployment state is also too dirty to deploy safely. The first AI agent taking this goal should preserve both checkouts, fix and verify P0 items, close the stipend fail-open cases, establish PostgreSQL-backed regression coverage, and only then produce a reviewed deployment artifact.
