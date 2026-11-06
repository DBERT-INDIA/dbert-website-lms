# DBERT Workspace Rules & Architectural Invariants
================================================================================
Universal Ground Rules for Antigravity, Gemini, and Autonomous Agents
================================================================================

## 1. Domain Authority & SEO Mandate
1. **Sovereign Domain**: The official live domain is strictly `https://dbert.in`. Under no circumstances should `dbert.online` be used in active endpoints, API URLs, certificate preview links, emails, or WhatsApp copy.
2. **Google Analytics 4**: Sitewide Measurement ID is strictly `G-MN7ME9X518`.
3. **Migration Continuity**: The `/dbert-online` landing page and migration notice copy must be preserved across header, footer, and verification layouts.

## 2. WhatsApp Dual-Account Dispatch System
1. **First-15-Lines Placement**: Both the **Verification Link** (`https://dbert.in/verify?certid=...`) and the **Google Form / Enrollment Link** MUST appear within lines 1–15 of every dispatch message.
2. **Reverse Chronological Ordering**: Candidates must always be dispatched latest-first based on registration timestamp (`signup_dt`).
3. **Strict Queue Partitioning (46 + 46 = 92)**:
   - Account 1 (Odd Serials): `.chrome_session_account1` (46 candidates).
   - Account 2 (Even Serials): `.chrome_session_account2` (46 candidates).
   - Mutually exclusive subsets with `LIMIT 46`. Zero overlap.
4. **Permanent Deduplication**: All sent candidates must be logged in SQLite `whatsapp_sent_log` to guarantee zero duplicate messages across runs.
5. **Anti-Ban Pacing**: 18s–35s randomized human delay between consecutive messages, with automatic circuit breaker on 3 consecutive errors.

## 3. Email Batch Dispatch System
1. **Tri-Factor DNS Compliance**: Verify SPF, DKIM, and DMARC records before starting dispatch.
2. **Authenticated SMTP Relay**: Deliver exclusively through Google Workspace authenticated SMTP (`abhinav.sharma@dbert.in`).
3. **Rate Control**: Minimum 30-second pacing between consecutive emails.
4. **Header Alignment**: `Reply-To` header must match sender email address (`abhinav.sharma@dbert.in`).
5. **Atomic State Tracking**: Record every sent email immediately in `data/dispatch_tracking_409.json` and `.csv`. Never re-send to candidates marked `SENT`.
6. **Milestone Telemetry**: Automated progress reporting at every 100 emails to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.

## 4. Enrollment & Balance Ledger Integrity
1. **Fee Ledger Transparency**: Total Incubation Program Fee is ₹1,999. Candidates who paid ₹499 initial caution deposit have their advance credited in full and only owe the remaining ₹1,500 balance.
2. **Dynamic Route Preservation**: Both `/enroll` and `/eroll` must dynamically redirect to `/enroll/1999` while preserving all query parameters (`?certid=...` or `?email=...`).
3. **Submission Idempotency**: UTR submissions in `/api/enroll/balance` must reject duplicate UTRs (`alreadySubmitted: true`) and record permanently into `/var/www/dbert-website-lms/data/balance_enrollments_1500.json`.

## 5. Production EC2 Deployment Protocol
1. **Target Server**: `ubuntu@3.26.237.171` using SSH key `C:\Users\user\.ssh\dbert-production-server.pem`.
2. **Standalone Build Asset Sync**: Always copy `public` into both `.next/standalone/` and `.next/standalone/apps/website/` after running `npm run build`.
3. **Permanent Storage Symlink**: Re-establish symlink from `.next/standalone/data` to `/var/www/dbert-website-lms/data` so Next.js standalone rebuilds never erase candidate submission logs.
4. **Verification**: Always curl or request live endpoints (`/enroll/1999`, `/eroll`, `/verify/directory`, `/api/enroll/lookup`) after service restart to verify `HTTP 200`.

## 6. Google SMTP Quota Tracking Watchdog & Dispatch Engine
1. **Autonomous Watchdog**: `scripts/quota_watchdog_and_dispatcher.py` continuously probes Google SMTP (`smtp.gmail.com:465`) every 300 seconds during cooldown.
2. **Sequential Unlock Pipeline**: When Google lifts the daily sending limit, the daemon automatically:
   - Phase 1: Re-deploys website updates to EC2 and verifies `https://dbert.in`.
   - Phase 2: Dispatches the 9 official verified candidate credentials.
   - Phase 3: Resumes and delivers the remaining 106 provisional candidate emails (#304–#409).
   - Phase 4: Syncs omnichannel tracking into `data/dbert_unified_omnichannel_tracking.csv`.
   - Phase 5: Sends completion telemetry to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.
3. **Circuit Breaker Integrity**: All dispatchers exit with code `55` if Google quota re-engages, preventing false failures.
