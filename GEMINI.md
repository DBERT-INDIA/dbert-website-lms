# DBERT Engineering & Agent Brain (GEMINI.md)
================================================================================
Universal Context, Architectural Rules, and Operational Playbook for Antigravity & Gemini Agents
================================================================================

## 1. Domain Authority & SEO Mandate (CRITICAL)
- **Active Sovereign Domain**: `https://dbert.in`
- **Legacy Retired Domain**: `dbert.online` (Redirects to `dbert.in`).
- **NEVER use `dbert.online`** as the active origin, baseUrl, canonical tag, or in any newly generated code, API endpoints, emails, certificate PDFs, or WhatsApp copy.
- **Dual SEO Headlines**: Maintain migration notice phrasing ("DBERT.online is now DBERT.in" / "dbert.online is not the active platform") across Header, Footer, About Credentials, Learners, and Verification pages.
- **Migration Page**: Dedicated landing page at `/dbert-online` with FAQPage and BreadcrumbList JSON-LD schemas.
- **Google Analytics 4 (GA4)**: Measurement ID is strictly `G-MN7ME9X518` across `apps/website`, `apps/portal`, and deployment templates.

---

## 2. Monorepo Architecture & Directory Map
- `apps/website/`: Next.js 14/16 App Router application (Turbopack standalone build).
  - Public portal, SSG/SSR verification engine (`/verify`, `/verify/[certId]`, `/verify/directory`, `/dbert-online`).
  - Master certificate registry: `apps/website/src/data/certificates_registry.json`.
  - Master candidate directory: `apps/website/src/data/directory_candidates.json` (465 records).
  - Incubation Enrollment & Balance Completion: `apps/website/src/app/enroll/1999/`, `/enroll`, and `/eroll`.
  - Backend API routes:
    * `/api/enroll/lookup`: Instant candidate profile autofill by Cert ID or email.
    * `/api/enroll/balance`: Idempotent 12-digit UTR submission recording with duplicate protection.
    * `/api/verify`: Public verification check endpoint.
- `apps/portal/`: Python Flask LMS & Internship Administration Portal.
  - Student learning management, task submissions, ambassador tracking, and mentorship portals.
- `data/`: Centralized candidate data, SQLite queues, and cross-channel tracking:
  - `data/all_409_provisional_registry.json`: Complete 409 candidate records.
  - `data/dispatch_tracking_409.json` / `.csv`: Live email dispatch tracking state.
  - `data/dispatch_409.log`: Live chronological email delivery audit log.
  - `data/balance_enrollments_1500.json`: Live candidate ₹1,500 balance submissions and UTR records.
  - `data/dbert_whatsapp.db`: Dual-account SQLite database in WAL mode (`whatsapp_dispatch`, `whatsapp_sent_log`).
  - `data/dbert_whatsapp_master.csv`, `_acc1.csv`, `_acc2.csv`: Live queue exports.
  - `data/dbert_unified_omnichannel_tracking.csv`: Merged email + WhatsApp status report.
- `scripts/`: Production automation, testing, and dispatch scripts:
  - `scripts/dispatch_409_provisional.py`: Core email batch delivery daemon with DNS pre-flight audit and milestone telemetry.
  - `scripts/deploy_enrollment_1999_to_ec2.py`: Automated build & deployment script for enrollment portal.
  - `scripts/deploy_directory_to_ec2.py`: Automated build & deployment script for alphabetical directory.
  - `scripts/send_dbert_whatsapp.py`: Core Playwright WhatsApp automation engine.
  - `scripts/verify_and_launch_dbert_whatsapp.py`: Automated pre-flight login & dual launcher.

---

## 3. Production EC2 Deployment Architecture

### 3.1. Server Connection & Infrastructure
- **Host**: `ubuntu@3.26.237.171`
- **SSH Key**: `C:\Users\user\.ssh\dbert-production-server.pem`
- **Remote Base Directory**: `/var/www/dbert-website-lms`
- **Web App Directory**: `/var/www/dbert-website-lms/apps/website`
- **Services Managed via Systemd**:
  - `dbert-website.service` (Next.js Standalone Node server on port 3000)
  - `dbert-portal.service` (Flask LMS Gunicorn server on port 5001)
  - `dbert-api.service` (FastAPI Uvicorn server on port 8000)
  - `nginx.service` (Reverse proxy with SSL termination for `dbert.in`, `lms.dbert.in`, `api.dbert.in`)

### 3.2. Next.js Standalone Build & Deployment Procedure
When deploying updates to `apps/website`, any agent must follow this exact sequence:
1. **Upload Modified Files**:
   ```powershell
   scp -i "C:\Users\user\.ssh\dbert-production-server.pem" -o StrictHostKeyChecking=no -o BatchMode=yes <local_file> ubuntu@3.26.237.171:/var/www/dbert-website-lms/apps/website/<target_path>
   ```
2. **Execute Remote Standalone Build & Asset Sync**:
   ```bash
   cd /var/www/dbert-website-lms/apps/website
   export NODE_ENV=production
   npm run build
   cp -r public .next/standalone/ 2>/dev/null || true
   cp -r public .next/standalone/apps/website/ 2>/dev/null || true
   # Ensure permanent data symlink persists across builds:
   mkdir -p /var/www/dbert-website-lms/data
   rm -rf /var/www/dbert-website-lms/apps/website/.next/standalone/data
   ln -s /var/www/dbert-website-lms/data /var/www/dbert-website-lms/apps/website/.next/standalone/data
   sudo systemctl restart dbert-website.service
   sleep 2
   systemctl is-active dbert-website.service
   ```
3. **Live Verification**:
   Verify endpoints return `HTTP 200` without caching issues.

---

## 4. Provisional Email Batch Dispatch System

### 4.1. Core Deliverability Constraints
1. **Tri-Factor DNS Pre-Flight Check**:
   Before initiating dispatch, verify SPF (`v=spf1 include:_spf.google.com ~all`), DKIM (`google._domainkey.dbert.in`), and DMARC (`v=DMARC1; p=none;`).
2. **Authenticated SMTP Delivery**:
   Uses Google Workspace SMTP relay (`smtp.gmail.com:465`) authenticated as `abhinav.sharma@dbert.in`.
3. **Pacing & Anti-Spam Rate Control**:
   Strict 30-second intervals between consecutive candidate dispatches.
4. **Header Alignment**:
   `Reply-To` MUST match the sender email address (`abhinav.sharma@dbert.in`) exactly.
5. **Atomic State & Idempotency**:
   Every sent message records `sent_at`, `message_id`, and `provider` into `data/dispatch_tracking_409.json` and `.csv`. A resumed process skips previously sent candidates automatically.
6. **Milestone Telemetry**:
   Every 100 delivered emails (and upon 100% completion), an automated telemetry report is dispatched to both `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.

---

## 5. Alphabetical Credential Directory (`/verify/directory`)

- **Route**: `https://dbert.in/verify/directory`
- **Dataset**: `apps/website/src/data/directory_candidates.json` (465 candidates: 56 verified + 409 provisional).
- **Features**:
  - Full A–Z alphabet letter selector with candidate count badges.
  - Real-time client-side instant search across candidate names, Certificate IDs, Intern IDs, and domain tracks.
  - Filter pills for major domains (AI/ML, Data Analyst, Full Stack, Python Automation, etc.).
  - Direct deep-links to each candidate's verification dossier (`/verify/[certId]`).

---

## 6. ₹1,999 Enrollment & Balance Completion Portal (`/enroll/1999`)

### 6.1. Financial Ledger Breakdown
- **Total Program Fee**: ₹1,999
- **Caution Deposit Paid**: -₹499 (Credited in full)
- **Net Remaining Balance Payable**: **₹1,500**
- Prominent notice informs candidates that as they already paid the ₹499 caution deposit, they only need to complete the remaining ₹1,500 balance to finalize enrollment and unlock official credentials.

### 6.2. Candidate Autofill API (`GET /api/enroll/lookup`)
- Supports query parameters `?certid=` or `?email=` (e.g., `https://dbert.in/enroll/1999?certid=CERT-DBERT-2026-DA-057`).
- Queries the candidate database and auto-populates Full Name, Email, WhatsApp Phone, College, Domain Track, and Certificate ID.

### 6.3. Payment & Submission Engine
- **Payment Methods**:
  - Embedded high-res UPI QR code (`/images/qrcode.jpeg` and `/qrcode.jpeg`).
  - Mobile 1-Tap UPI Launchers (Google Pay, PhonePe, Paytm, Default UPI) with pre-filled amount ₹1,500 and merchant VPA `Q652429146@ybl` (`DBERT Admissions`).
  - Blob-based "Download QR" button compatible with all mobile browsers.
- **UTR Submission API (`POST /api/enroll/balance`)**:
  - Validates 12-digit UPI UTR.
  - Prevents duplicate submissions (`alreadySubmitted: true`).
  - Assigns unique submission ID (e.g. `DBERT-ENR-XXXXXX-XXXX`).
  - Records permanently into `/var/www/dbert-website-lms/data/balance_enrollments_1500.json`.
- **WhatsApp Proof Routing**:
  - 1-Tap WhatsApp button routing pre-formatted transaction details to Admissions (`+91 81929 11360`).
- **Typo & Alias Forwarding**:
  - Both `/enroll` and `/eroll` dynamically forward to `/enroll/1999` with all query parameters intact.
- **Locked Certificate CTA Integration**:
  - Locked certificates on `/verify/[certId]` link directly to `/enroll/1999?certid={certId}`.

---

## 7. WhatsApp Dual-Account Dispatch System

### 7.1. Architectural Constraints
1. **First-15-Lines Placement**:
   - Both the **Verification URL** (`https://dbert.in/verify?certid=...`) and the **Google Form URL** (`https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header`) **MUST appear within the first 15 lines** of the WhatsApp message.
   - Current template positions: Verification URL at **Line 8**, Google Form URL at **Line 11**.
2. **Reverse Chronological Candidate Ordering (Latest First)**:
   - Candidates must be dispatched in order of registration timestamp (`signup_dt`), starting with the latest October 2026 signups down to older cohorts.
3. **Queue Partitioning (46 + 46 = 92 Candidates per Batch)**:
   - **Account 1 (Odd Serials)**: Assigned to `.chrome_session_account1` (46 candidates).
   - **Account 2 (Even Serials)**: Assigned to `.chrome_session_account2` (46 candidates).
4. **Anti-Ban Pacing & Human Safety**:
   - 18s–35s randomized human breaks between consecutive deliveries.
   - Circuit breaker automatically pauses worker if 3 consecutive failures occur.
   - Permanent deduplication table `whatsapp_sent_log` ensures zero duplicates.

---

## 8. Key CLI Commands Reference

```powershell
# ==================== EMAIL DISPATCH SYSTEM ====================
# Launch or resume live 409 provisional candidate email batch dispatch
python scripts\dispatch_409_provisional.py --live --delay 30 --report-interval 100

# Inspect recent dispatch log
powershell -Command "Get-Content data/dispatch_409.log -Tail 20"

# Check email tracking state summary
python -c "import json; d = json.load(open('data/dispatch_tracking_409.json', encoding='utf-8')); s = sum(1 for x in d if x['status']=='SENT'); print(f'Sent: {s}/409, Pending: {409-s}')"

# ==================== EC2 DEPLOYMENT SCRIPTS ====================
# Deploy enrollment portal updates to production EC2
python scripts\deploy_enrollment_1999_to_ec2.py

# Deploy alphabetical directory updates to production EC2
python scripts\deploy_directory_to_ec2.py

# ==================== WHATSAPP DISPATCH SYSTEM ====================
# Inspect active WhatsApp queue (Dry Run)
python scripts\send_dbert_whatsapp.py --dry-run

# Check WhatsApp campaign metrics (Sent vs Remaining)
python scripts\send_dbert_whatsapp.py --status

# Load next batch of 92 uncontacted candidates (Latest signups first)
python scripts\send_dbert_whatsapp.py --next-batch

# Run interactive pre-flight session check and launch dual workers
python scripts\verify_and_launch_dbert_whatsapp.py
```

---

## 9. Persistent Documentation Directory
- Comprehensive architectural records and changelogs:
  - [`DOMAIN_MIGRATION_AND_GA4_CHANGELOG.md`](file:///c:/Users/user/Desktop/dbert-website-lms/DOMAIN_MIGRATION_AND_GA4_CHANGELOG.md)
  - [`new_certifications_reconciliation_and_dispatch_plan.md`](file:///C:/Users/user/.gemini/antigravity/brain/542c2e0b-55d0-41c9-9b46-721bf0724211/new_certifications_reconciliation_and_dispatch_plan.md)
  - [`enrollment_1999_deployment_walkthrough.md`](file:///C:/Users/user/.gemini/antigravity/brain/542c2e0b-55d0-41c9-9b46-721bf0724211/enrollment_1999_deployment_walkthrough.md)
  - [`intern_directory_alphabetical_verification_plan.md`](file:///C:/Users/user/.gemini/antigravity/brain/542c2e0b-55d0-41c9-9b46-721bf0724211/intern_directory_alphabetical_verification_plan.md)

---

## 10. Verified Candidates Ingestion & Dispatch (Google Sheet gid=1265293201)

### 10.1. Scope & Reconciliation Breakdown
- **Source Sheet**: `Certificate Internship Batch 2026 (Responses)` (`gid=1265293201`).
- **Total Rows**: 65.
- **Rows 1–56**: 56 original verified candidates (`CERT-DBERT-2026-DA-001` – `FSD-056`).
- **Rows 57–65 (9 Candidates)**: Paid form submissions with ₹299 transaction proof uploaded to Google Drive.
  - **7 Upgraded Candidates**: `N Deekshitha` (`AIML-092`), `M Brahmani` (`DA-117`), `Ankit Saini` (`FSD-070`), `Lucky kumar` (`PA-023`), `Rohit Ranjan Tiwari` (`DA-124`), `Shreyash Sambhaji Kamble` (`DA-077`), `Satya Patil` (`DA-109`).
  - **2 Brand New Candidates**: `Vasu Rakholiya` (`CERT-DBERT-2026-DA-183`), `Janhvi singh` (`CERT-DBERT-2026-DA-184`).
- **Artifacts Generated**:
  - Full 3-document PDF packets (Certificate of Completion, Academic Evaluation, LOR) in `outputs/cohort_2026/`.
  - Preview PNGs copied to `apps/website/public/certificates/previews/{certId}.png`.
  - All 9 records updated to `status: "VERIFIED"`, `isProvisional: false` in `certificates_registry.json` and `directory_candidates.json`.
  - Deployed to EC2 (`3.26.237.171`), Next.js rebuilt and reloaded. Live verified on `https://dbert.in`.

### 10.2. SMTP Daily Limit Cooldown
- Google Workspace SMTP for `abhinav.sharma@dbert.in` reached daily user quota (`550 5.4.5 Daily user sending limit exceeded`) after delivering 303 emails earlier today.
- `scripts/dispatch_9_verified_certificates.py` manages the 9 verified candidates (`data/dispatch_tracking_9_verified.json`).
- `scripts/dispatch_409_provisional.py` manages the remaining 106 provisional candidates (resuming at #304).
- Both daemons automatically execute once Google's 24h rolling limit expires.

---

## 11. Approved Incubation Enrollment & Live Countdown Architecture (`/enroll/1999`, `/eroll`)

### 11.1. Candidate Approval & Balance Reconciliation
- **Approved Candidate**: **Bhargavi Poola** (`bhargavi13032007@gmail.com`, Phone: `9603742553`, UTR: `679862090077`, Ref: `DBERT-ENR-703685-TYN6`, Paid: ₹1,500).
- **Domain Track**: Full Stack Web Development (`CERT-DBERT-2026-FSD-156` / `DBERT-2026-INT-1412`).
- **Ledger Status**: Marked `status: "APPROVED"` in `data/balance_enrollments_1500.json` on EC2 (`/var/www/dbert-website-lms/data/`) and locally.
- **Batch Kickoff**: **Monday, 9 Nov 2026 at 06:00 PM IST** (`2026-11-09T18:00:00+05:30`).

### 11.2. Verification & Approved Countdown View
- **URL Routing**:
  - `https://dbert.in/eroll?email=bhargavi13032007@gmail.com` (Redirects HTTP 307 to `/enroll/1999?email=...`).
  - `https://dbert.in/enroll/1999?email=bhargavi13032007@gmail.com`.
  - Also works by typing email or Certificate ID into the lookup input on `dbert.in/enroll/1999`.
- **API Engine (`GET /api/enroll/lookup`)**:
  - Checks `balance_enrollments_1500.json` first.
  - Returns `enrollmentStatus: "APPROVED"`, `isApproved: true`, `batchStartDate: "2026-11-09T18:00:00+05:30"`, and `batchStartDisplay: "Monday, 9 Nov 2026"`.
- **Approved UI Dossier & Countdown**:
  - Replaces payment form & QR code with the official **Approved & Seat Confirmed Dossier**.
  - Displays a real-time **1-second live countdown timer** (Days, Hours, Minutes, Seconds) ticking down to Monday, 9 Nov 2026 (06:00 PM IST).
  - Features Candidate Dossier grid (Ref ID, UTR, Fee Reconciled: ₹1,999 Paid in Full), 4-step Sprint Roadmap, and direct WhatsApp Concierge routing to Admissions.
- **Public Credential Integration**:
  - Bhargavi Poola registered in `certificates_registry.json` and `directory_candidates.json`.
  - Public verification dossier live at `https://dbert.in/verify/CERT-DBERT-2026-FSD-156`.

---

## 12. Automated Google SMTP Quota Watchdog & Phased Candidate Dispatcher

### 12.1. Operational Purpose & Architecture
- **Daemon Script**: `scripts/quota_watchdog_and_dispatcher.py`
- **1-Click Launcher**: `start_quota_watchdog.bat`
- **Persistent State**: `data/quota_watchdog_state.json`
- **Detailed Execution Log**: `data/quota_watchdog.log`
- **Polling Cadence**: Probes `smtp.gmail.com:465` via `EmailDeliveryService` every 300 seconds (5 minutes).
- **Circuit Breaker**: `dispatch_9_verified_certificates.py` and `dispatch_409_provisional.py` both exit with status code `55` if Google's `550 5.4.5 Daily user sending limit exceeded` is detected mid-batch, halting gracefully without burning candidate records.

### 12.2. Automated Sequential Pipeline (Triggered upon Quota Unlock)
1. **Phase 1: EC2 Deployment & Live Verification**:
   - Executes `scripts/deploy_new_certificates_to_ec2.py`.
   - Rebuilds Next.js Turbopack standalone, syncs public assets and data symlinks, restarts `dbert-website.service`.
   - Validates live HTTP 200 and `verified: True` via `https://dbert.in/api/verify?certid=CERT-DBERT-2026-AIML-092`.
2. **Phase 2: 9 Verified Candidate Dispatches**:
   - Executes `scripts/dispatch_9_verified_certificates.py --live --delay 30`.
   - Delivers official 3-document credential packets (Certificate, Academic Evaluation, LOR) to all 9 verified candidates.
3. **Phase 3: Resume Remaining 106 Provisional Dispatches**:
   - Executes `scripts/dispatch_409_provisional.py --live --delay 30 --report-interval 100`.
   - Resumes candidate #304 through #409.
   - Milestone telemetry automatically dispatched to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.
4. **Phase 4: Omnichannel Sync**:
   - Executes `scripts/send_dbert_whatsapp.py --sync-email`.
   - Updates `data/dbert_unified_omnichannel_tracking.csv`.
5. **Phase 5: Mission Completion Telemetry**:
   - Dispatches a comprehensive HTML + plain text completion report to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.



