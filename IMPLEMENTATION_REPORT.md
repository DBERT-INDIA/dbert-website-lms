# DBERT offline implementation report

## Development baseline

This working copy was created from the extracted `dbert-website-lms-main` source. It has a local Git history on `feature/platform-improvements`. The original download and the separate GitHub checkout remain available as references. Offline fixtures are empty for applicant and credential registries. Operational exports and certificate attachments are outside this working copy.

The [course cohort and study classroom report](COHORT_CLASSROOM_IMPLEMENTATION.md) records the next set of offline changes. It covers course cohorts, waitlists, the study workspace, learner reviews, mentor follow-ups, milestones, and cohort credentials.

### Résumé checker

- **Before** — The page used inline event handlers that its Content Security Policy blocked. Each scan also replaced the previous score.
- **Change** — Recovered upload, pasted text, scanning, and report unlock under the enforced policy. Added a baseline and revision comparison for the same target role.
- **How it works** — A local script binds controls through event listeners. The comparison keeps numeric score snapshots in the browser tab and clears them on reload. Unlock uses the last successful submission.
- **Benefit** — Keyboard users can run an audit and see which of the five categories improved after a revision.
- **Verification** — The carried-forward change previously passed three isolated Chromium tests with synthetic inputs and mocked responses. The verification results for this working copy are recorded below as checks complete.

## Backlog status

Items are tracked against the approved backlog. The sections below record the flaw, change, benefit, operation, and verification for each delivered change.

| Item | Scope | Status |
| --- | --- | --- |
| 1 | Public website and forms | Implemented locally |
| 2 | Course and internship discovery | Implemented locally |
| 3 | Student dashboard | Implemented locally. Includes measured progress, due reviews, next booked mentor, and an applications shortcut. |
| 4 | Applications | Implemented locally |
| 5 | Learning reviews and submission reliability | Partial. Turn API and review queue implemented. Streaming chat does not yet have end-to-end replay. |
| 6 | Mentorship | Implemented locally. PostgreSQL migration needs staging verification. |
| 7 | Job-specific résumé feedback and portfolio | Implemented locally. Includes opt-in verified evidence on the public CV and PDF. |
| 8 | Staff task review | Implemented locally |
| 9 | Payments and enrollment | Implemented locally with synthetic verification. Provider and historical reconciliation remain deployment work. |
| 10 | Privacy and access | Partial. Offline fixtures and narrowed responses. Public repository remediation and authenticated lookup remain open. |
| 11 | Accessibility and visual consistency | Partial. Controls and forms repaired on the surfaces listed below. A full cross-platform audit remains open. |
| 12 | Release quality | Partial. Offline verifier and Compose correction. Hosted checks, an exact Next.js build, and cPanel verification remain open. |
| 13 | Unified search | Implemented locally with entry points in both apps |
| 14 | Personalized onboarding | Implemented locally as a learner dashboard starter with browser preferences |
| 15 | Skill map | Implemented locally in the classroom |
| 16 | Project workspace | Implemented locally for the course capstone and staff review workflow |
| 17 | Assessment recovery | Implemented locally for course day quizzes |
| 18 | Notification inbox | Implemented locally. Inbox and existing device preferences share a page. Delivery providers need staging verification. |
| 19 | Support tracking | Implemented locally |
| 20 | Course publishing | Implemented locally for course titles and existing lesson text. Existing authoring owns structural changes. |
| 21 | Mentor workspace | Implemented locally |
| 22 | Employer dashboard | Implemented locally |
| 23 | Listing quality | Implemented locally |
| 24 | Funnel analytics | Implemented locally for existing recorded milestones |
| 25 | Staff action history | Implemented locally for applications, enrollments, reviews, credentials, support, and course publication |
| 26 | Credential wallet | Implemented locally in Flask. The legacy public website registry still needs migration. |
| 27 | Account and security center | Partial. Session management and existing preferences link. Verified contact changes remain open. |
| 28 | Low-bandwidth experience | Partial. Progressive rendering and draft recovery. End-to-end performance measurement remains open. |
| 29 | Content freshness | Partial. Ecosystem spotlights support schedule and preview. Events and cohort announcement scheduling remain open. |
| 30 | Production health | Partial. Admin dashboard for worker and queue data. Fleet-wide monitoring and alerts remain open. |
| 31 | Bounty and perk planner | Implemented locally |
| 32 | Route and service reliability | Partial. Learning, mentoring, and payment conflicts addressed. Other duplicate routes remain open. |

## Implementation details and verification

### Public website, navigation, and forms (1, 11, 28)

- **Before** — Important public destinations were harder to reach on mobile. Form labels were disconnected from their controls, and restarting a completed form could retain the previous submission. Some content depended on JavaScript animation to become visible.
- **Change** — Added direct homepage shortcuts and improved keyboard navigation and focus return. Contact, demo, and consultation now use shared accessible form behavior and can recover entered values after a failed request.
- **How it works** — Shared form components bind labels and feedback to each control. Motion is conditional on browser preferences and data saver. Essential links and content render in the HTML.
- **Benefit** — Visitors can find the right destination, recover from a failed submission, and use the site with a keyboard or a slow connection.
- **Verification** — Isolated Chromium checked desktop and 390 px mobile behavior, menu focus, all three forms, a simulated 503 and retry, and script-disabled navigation. The harness ran the changed components with cached dependencies and mocked requests.

### Course discovery, saved opportunities, and sign-in handoff (2)

- **Before** — Course cards, course counts, and metadata were maintained separately. Internship sign-up links could lose the selected role or city. There was no browser shortlist.
- **Change** — Unified the public catalog, added course filters, and preserved return paths across the website-to-LMS handoff. LMS detail pages now let visitors save roles and review their availability.
- **How it works** — One typed Next.js catalog drives cards and structured data. Handoff values are encoded in the URL query before the sign-up fragment. The shortlist stores only listing IDs, titles, and types in the browser, then checks the portal’s existing public listing conditions.
- **Benefit** — Visitors can narrow the catalog, resume the correct opportunity after signing in, and see when a saved role has closed.
- **Verification** — Chromium exercised course filtering, JSON-LD agreement and exact handoff URL construction. Flask tests checked the availability response against open, unapproved, draft, and expired records.

### Learner dashboard, review queue, and skill map (3, 5, 15)

- **Before** — The dashboard showed a fixed review count and estimated quiz and practice figures. The course page opened the first lesson every time, and fetching the concept map could create mastery rows.
- **Change** — Display recorded quiz averages and pass counts, show due concepts, add a read-only classroom skill map, and show the next confirmed mentoring session on the dashboard. Review links open the associated lesson when the learner is enrolled.
- **How it works** — Quiz percentages are calculated from scores and maximums. The review service supplies due concepts and checks enrollment before producing a lesson URL. The skill map reads mastery and attempt counts from the existing tables.
- **Benefit** — Learners can trust the numbers and go directly to practice instead of finding the right lesson themselves.
- **Verification** — Flask and Jinja syntax checks cover the updated entry points. The transaction and route checks are listed in the verification section.

### Applications and employer hiring (4, 22)

- **Before** — Applications were shown in one list. Employers could change a status but lacked a usable interview schedule and filled-role flow.
- **Change** — Added action-required, waiting, and closed filters, a status timeline, interview actions, employer scheduling, and the ability to mark a role filled.
- **How it works** — Views use recorded application dates and existing state. Employer actions are limited to the company that owns the role. Interview times are stored in UTC and displayed in the expected timezone. Filled roles leave active listings and retain their application history.
- **Benefit** — Applicants can see who acts next. Employers can close out hiring without losing candidate history.
- **Verification** — Synthetic hiring tests and offline assertions covered state labels, timeline rendering, job ownership, and scheduling.

### Guided Learning transactions and route conflicts (5, 32)

- **Before** — Mastery, events, and reviews committed separately. A retry after a later answer could process the original answer again. Some Flask routes had competing definitions with different behavior.
- **Change** — Saved each learning turn in a single transaction and stored an outcome for keyed retries. Canonical handlers now serve the updated learning, mentor booking, and payment paths.
- **How it works** — A transaction protects the learner and session rows while grading results, mastery, review scheduling, and the receipt are written. A retry returns the original result. Existing callers of the mastery helpers retain their default commit behavior.
- **Benefit** — Failed writes leave progress intact, and concurrent delivery of the same answer creates one attempt.
- **Verification** — SQLite tests forced a late write failure, retried an older key after another turn, and submitted the same key concurrently.

### Mentor scheduling and workspace (6, 21)

- **Before** — Inline controls could be blocked by CSP. Duplicate booking handlers disagreed on capacity. Calendar downloads could use the wrong timezone or a placeholder meeting link.
- **Change** — Added consistent reservation and cancellation, capacity handling, timezone-correct calendar files, confirmed meeting links, learner questions, shared agenda, and follow-up.
- **How it works** — One booking service owns slot changes and enforces ownership and availability. Existing SQLite reservations are migrated. Calendar output converts IST to UTC and is exposed to eligible bookings.
- **Benefit** — Learners can trust the time and meeting link. Mentors can prepare and follow up on the same booking.
- **Verification** — Four isolated SQLite tests and a Flask smoke from booking to .ics download and cancellation passed. Production PostgreSQL was outside offline verification.

### Job-specific résumé feedback (7)

- **Before** — A role-level résumé score did not explain coverage against an individual job description.
- **Change** — Both checkers accept a job description and show mentioned skills, skills needing evidence, and practice links. The existing role revision comparison remains available.
- **How it works** — The Flask service matches recognized skills from the existing domain catalogs against résumé text. Job comparison uses a deterministic local calculation. The preview and unlock requests use the same submitted inputs.
- **Benefit** — Students can revise for a real job based on visible evidence and find relevant coursework or practice.
- **Verification** — Python tests cover aliases, punctuation, duplicate mentions, and a skill such as SQL appearing inside another word. Mocked Chromium verified PDF and text submission and the same-payload unlock on the public site.

### Staff task review, listing quality, and action history (8, 23, 25)

- **Before** — Staff had a status-only task queue, could not quickly see waiting time, and lacked a usable listing report queue. Task decisions and their audit entry could be written separately.
- **Change** — Added backlog counts, waiting age, domain filters, pagination, review history, and a listing-quality queue with learner reports.
- **How it works** — The queue reads the existing submission records, limits one row per task submission, and writes the review event in the decision transaction. Listing reports deduplicate per learner, listing, and reason. Staff see duplicate, incomplete, expired, or stale listing signals.
- **Benefit** — Staff can prioritize older work, address poor listings, and review who acted on a case.
- **Verification** — Synthetic SQLite staff queue and hiring workflow tests checked pagination and domain or status filtering, report deduplication, and audit behavior.

### Payment reconciliation and enrollment (9, 32)

- **Before** — An unverified transfer claim could immediately credit enrollment. Retries could add the same amount again. Some checkout flows used purchase data from the browser or lacked a durable order record.
- **Change** — Added a pending claim ledger, staff reconciliation, learner receipts, and persisted checkout terms. Offline code includes shared capture fulfillment for browser and webhook paths and a queue for online payment exceptions.
- **How it works** — Transfer references reuse a canonical receipt, and only verified settlement credits an enrollment. Online capture must match the persisted buyer, product, amount, and currency. The successful payment ID and credit are recorded atomically.
- **Benefit** — Learners get accurate pending or verified status, and staff can resolve unmatched payments without double crediting.
- **Verification** — Synthetic Flask and Node checks covered pending claims, exact verified settlement, legacy credit preservation, rollback, signed capture, and retries. Provider credentials, live callbacks, and production database migration were outside offline verification.

### Privacy and account sessions (10, 27)

- **Before** — The fallback enrollment lookup returned full contact and verification-submission fields. Development data included applicant exports, and users lacked a place to review active sign-ins.
- **Change** — Narrowed unauthenticated responses, removed submitted verification details and rejection notes, masked contact fields, and used empty local registry fixtures. Added active session controls scoped to the signed-in identity.
- **How it works** — The website returns a minimal lookup response with private cache headers. `/account/security` selects only session metadata and revokes sessions by the current email and role without returning tokens.
- **Benefit** — Less personal information is exposed, and users can sign out other devices without losing their own session.
- **Verification** — Synthetic Flask checks covered identity and role boundaries, current-session preservation, and revocation. Public-history cleanup, registry migration, and verified contact updates need additional work.

### Search and support (13, 19)

- **Before** — Discovery was scattered across menus. Learners could not follow a support request through a visible queue.
- **Change** — Added website and portal search, a help entry point, owner-only request histories, and an authorized support queue.
- **How it works** — Public catalog and published opportunity results use existing visibility rules. Learner navigation appears only to signed-in learners. Support retains the page path without its query or fragment and records staff assignment, status, and updates.
- **Benefit** — Users can find the right page and follow a request from submission to resolution.
- **Verification** — Isolated Chromium checked script-disabled website search. Flask tests checked search visibility, ticket ownership, invalid form recovery, and authorized updates.

### Personalized learner starter (14)

- **Before** — Learners had navigation links but no simple way to choose and remember their first goal.
- **Change** — Added a starter card with learning, practice, and mentoring paths plus skip and resume.
- **How it works** — The dashboard uses the signed-in learner’s track and course assignment to select destinations. Only the chosen goal and skip preference are saved for that account in the current browser.
- **Benefit** — Learners can start with work that fits their immediate goal and return to the card later.
- **Verification** — Jinja and JavaScript syntax checks cover the card and its dashboard integration.

### Course quiz recovery (17)

- **Before** — Refresh restarted the measured timer, unsent answers could disappear, and a retried submission had no durable grade receipt.
- **Change** — Added attempt-scoped autosave, server-timer recovery, retryable feedback, and stored grade receipts. Corrected the 70% pass threshold for short quizzes.
- **How it works** — A server attempt key binds the browser draft to the current enrollment. The browser restores answers after refresh. A database transaction saves the grade and receipt. The same key can return the grade without recording another attempt.
- **Benefit** — A learner can recover from a lost response or refresh without losing answers, resetting the timer, or recording duplicate progress.
- **Verification** — Isolated Flask tests use a synthetic clock and check refresh, elapsed time, the grade threshold, retry, and enrollment ownership.

### Funnel analytics and platform health (24, 30)

- **Before** — Staff had no compact view of learner drop-offs or a place to compare delivery backlog with request health.
- **Change** — Added an admin-only funnel, separate visitor aggregates, and a platform health dashboard.
- **How it works** — The funnel deduplicates learner accounts and checks recorded application, course enrollment, and learning activity. Health uses the existing worker telemetry and database outbox counts, without exposing raw events.
- **Benefit** — Staff can see where learners stall and whether a queue or integration needs attention.
- **Verification** — Synthetic Flask checks exercise role restrictions, actual counts, and redaction. Metrics describe the current portal worker and database, rather than a monitored fleet.

### Credential wallet and lifecycle (25, 26)

- **Before** — Certificates were scattered across views, and printable or public verification status could not distinguish a replaced or revoked credential.
- **Change** — Added a signed-in wallet and admin replacement or revocation with reason history. The existing Flask verification and print paths recognize inactive credentials.
- **How it works** — The wallet reads only certificates belonging to the learner. An admin can replace a valid certificate with another valid certificate for the same learner, or revoke it. The update and its audit entry are committed together.
- **Benefit** — Learners can share one verification link, and recipients see the current status before trusting a document.
- **Verification** — Synthetic Flask checks cover owner visibility, admin permission, same-owner replacement, and blocked print for replaced certificates.

### Bounty and perk planner (11, 31)

- **Before** — Learners had to compare prices and balances themselves, and inline event handlers could block tabs or redemption under the portal’s CSP.
- **Change** — Added a goal selector, coin gap, progress bar, and available bounty suggestions. Updated tab, filter, and redemption controls to use CSP-compatible handlers.
- **How it works** — The planner uses the existing task balance, perk prices, and open bounty rewards. The server still owns redemption and its eligibility checks.
- **Benefit** — Learners can plan what to work on without changing coin balances or redemption rules.
- **Verification** — Jinja and JavaScript checks cover the planner and its existing form and navigation hooks.

### Release and content corrections (12, 29)

- **Before** — Compose tried to extend a different database service name. Public internship pages presented static counts and dates as current. Several useful checks required unrelated integrations to boot.
- **Change** — Corrected the database override and added a repeatable offline verification command. Removed unsupported count, weekday, and category posting-date claims.
- **How it works** — The local verifier checks Compose structure, parses Flask and Jinja sources, and runs synthetic tests in the Python and Node runtimes. The website links to the existing live-listing route for current opportunities.
- **Benefit** — Developers can validate critical behavior offline. Visitors receive fewer misleading claims about current opportunities.
- **Verification** — Run `python -B scripts/verify_offline.py` from this directory. The offline checker validates Compose configuration structure. A Docker daemon, exact Next.js dependency set, hosted checks, and cPanel runtime were unavailable for this verification.

### Verified projects and credentials on the public CV (7, 10)

- **Before** — The public CV could list all certificate records and auto-add approved projects after a staff decision. Existing account contact fields were included in public CV rendering.
- **Change** — Added a separate portfolio selector and included only selected, eligible evidence in the public CV and PDF. New CVs are private by default.
- **How it works** — Selections are stored per learner. Each public render rechecks that the selected projects are approved, certificates are valid, and the learner owns them. Hidden account contact fields are omitted.
- **Benefit** — Learners choose what recruiters see. Revoked credentials and another learner’s work cannot appear through a portfolio selection.
- **Verification** — Synthetic portfolio tests cover default empty selection, eligibility, ownership, and later revocation.

### Capstone project revisions (16, 25)

- **Before** — Students saw only the latest submission and had no record of reviewer feedback. They could submit another copy while the previous version was pending.
- **Change** — Added a preparation checklist, revision history, learner-visible rubric feedback, and a request-changes path in the staff queue.
- **How it works** — Revision creation checks the current enrollment’s latest status while holding its write lock. Staff decisions write feedback, rubric, timestamp, and audit entry in the same transaction. Students revise the existing project after changes are requested.
- **Benefit** — A student can see why the submission needs work and review feedback across attempts. Staff see one pending revision at a time.
- **Verification** — The isolated Flask workflow submits a project, rejects a duplicate pending submission, records a rubric and correction, and renders both revisions.

### Notification inbox and delivery leases (18)

- **Before** — Account notifications had a passive feed. Worker claims and acknowledgements could overlap when an old claim expired.
- **Change** — Added all/unread views and mark-one or mark-all actions next to existing push preferences. Added unique leases, expiry recovery, and guarded delivery acknowledgements.
- **How it works** — Read actions are scoped to the learner who owns the alert. Workers commit their claim before invoking a dispatcher. A status change must match the current live lease.
- **Benefit** — Students can triage alerts and staff get more reliable delivery state after worker interruptions.
- **Verification** — Offline SQLite checks confirm that a stale worker cannot acknowledge a reclaimed event and that the claim is already visible before a local test dispatcher runs. Live delivery remains a staging check.

### Course editions and rollback (20, 25)

- **Before** — Authors had course creation and approval, but editing lesson text had no draft and rollback workflow.
- **Change** — Added author-owned drafts, previews, admin publishing, an edition history, and restoration of earlier editions.
- **How it works** — Drafts save course titles and lesson content as snapshots linked to existing IDs. Publishing validates the lesson set and writes the live pointer and an audit entry in one transaction. The prior live material is captured before the first change.
- **Benefit** — Authors can review changes privately and admins can restore a previous release without changing lesson IDs, quiz references, or completions.
- **Verification** — Synthetic Flask tests cover company ownership, validation, preview, role-gated publish, and rollback.

### Scheduled ecosystem spotlights (11, 29)

- **Before** — Staff could switch slides on or off, but they could not schedule them. The learner carousel's inline click handlers could be blocked under CSP.
- **Change** — Added publish and expiry times, status labels, a preview, and normal links and keyboard-operable slide controls.
- **How it works** — Staff enter IST values, the app stores UTC timestamps, and the learner endpoint filters by the active window. The carousel binds events in its approved script and pauses automatic rotation during keyboard interaction or reduced-motion use.
- **Benefit** — Staff can schedule campaigns and retire stale slides. Learners can open and navigate them with the enforced policy enabled.
- **Verification** — Tests check time conversion, scheduled, live, expired, and paused states. Template checks cover the staff and learner entry points.

### Unified staff action history (25)

- **Before** — Application, enrollment, review, credential, support, and publishing events were scattered across separate records.
- **Change** — Added an admin-only, filterable action history with actor, action, time, record, and reason when present.
- **How it works** — The page reads bounded results from existing histories and sorts them by recorded time. The output omits raw snapshots and event payloads.
- **Benefit** — Admins can trace decisions without opening several operational screens or inspecting applicant data exports.
- **Verification** — Synthetic Flask tests confirm admin access, filter behavior, and omitted metadata.

## Reproduce the offline verification

Run from the root of `dbert-website-lms-offline`.

```powershell
python -B scripts/verify_offline.py --browser
```

The completed run passed **44 Python tests, 4 Node tests, and 4 Chromium tests**. The verifier also passed Compose service and dependency checks, Flask and selected Jinja syntax checks. Separate JavaScript syntax checks passed for the modified dashboard, spotlight, classroom, quiz, and perks code. The public website component harness separately exercised desktop and mobile navigation, the three public forms, course filters, sign-in handoff, search without JavaScript, and job-specific résumé feedback with simulated responses.

### What this environment can run

- The smoke suite uses installed Python and Node libraries, SQLite fixtures, mocked payment and AI responses, and an installed Chromium. Browser requests are intercepted for the test pages.
- The Flask application requires the local packages in `apps/portal/requirements.txt`, including PyJWT, cryptography, ReportLab, boto3, and PyMuPDF, which were missing from this Python runtime. With those dependencies and local configuration available, start the portal from `apps/portal` with `python -m flask --app app run --port 5000`.
- The website lockfile pins Next.js 16.3.4. The exact dependency set was unavailable offline, so full `npm run build` and application startup remain unverified. For local development, set `LMS_INTERNAL_URL=http://127.0.0.1:5000` for the résumé checker proxy. The payment-claim intake also reads `INTERNAL_LMS_SYNC_URL` and needs `INTERNAL_SYNC_SECRET` configured on both apps.
- Docker CLI was unavailable. Compose was checked as configuration. Production PostgreSQL migrations, payment providers, delivery providers, and cPanel deployment remain staging checks.

### Operational data inventory

The original review found an applicant account export with 2,947 rows, a cohort export with 2,585 contact records, candidate inbox correspondence, and separate enrollment and verification exports. This working copy uses empty registry fixtures and excludes operational exports and certificate attachments. Public repository access remediation and moving historical records to controlled storage require maintainer action. Historical payments created by the previous checkout also need reconciliation against provider records before cutover.

The approved backlog table above records remaining implementation separately from runtime checks. The existing application data and production services were never used as test fixtures.
