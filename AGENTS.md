# DBERT Engineering & Agent Brain (AGENTS.md)
================================================================================
Universal Context, Architectural Rules, and Operational Playbook for Antigravity & AI Agents
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

## 5. Pre-Vetted Engineers Directory (`/verify/directory`)

- **Route**: `https://dbert.in/verify/directory` (Linked from `/hire/pre-vetted-engineers`)
- **Dataset**: `apps/website/src/data/directory_candidates.json` (465 candidates: 65 verified pre-vetted engineers + 400 provisional incubation fellows).
- **Architecture & Features**:
  - **Alphabetical Filter Eliminated**: Recruiters search by technical domain, stack keywords, and competency instead of candidate first names.
  - **Segregated Status Tabs**:
    - **Tab 1: Pre-Vetted Engineers (Verified · Ready to Hire)** (65 verified candidates with completed evaluations and verified credentials).
    - **Tab 2: Incubation Fellows (Provisional · In Sprints)** (400 candidates completing active milestones).
  - **Dynamic Hireability Ranking Mechanism**: Candidates are ranked dynamically with highest evaluation scores (98, 97, 96...) and verified status surfaced first.
  - **Score Ranking Filter**: Dropdown filter for Top Tier Distinction (90+ Score), High Merit (85+), and Proficient (80+).
  - **Derived Technical Stack Chips**: Domain-mapped technology pills (Next.js, PostgreSQL, PyTorch, LangChain, Celery, Docker, Figma, etc.).
  - **Dual Recruiter CTAs**:
    - `View Proof Dossier →`: Direct deep-link to cryptographically verified evaluation rubric, Turnitin score, and recommendation letter at `/verify/[certId]`.
    - `Connect on LMS →`: Direct routing to `https://lms.dbert.in/company/signup?ref=directory&candidate=[certId]` for instant employer registration and candidate messaging.
  - **Employer Value Banner**: Top B2B hero showcasing 48h match turnaround, top 3% screening bar, zero recruiter markup, and 14-day risk-free trial.

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
# Deploy website UI/UX updates to production EC2 & rebuild Next.js standalone
python scripts\deploy_website_updates_to_ec2.py

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

---

## 13. Stipend Contribution & Verification Gating System (`/stipend/tasks`)

### 13.1. Business Rules & 3-Step Eligibility Checklist
- **Strict Verification Gate**: Stipend eligibility and technical contribution submission are **strictly restricted to candidates with VERIFIED credentials** (`status: "VERIFIED"`, `verified: true`, `isProvisional: false`).
- **Completion Date Gate**: Interns can only apply for stipend **on or after their official completion date** (`joining_date + 60 days` from LMS enrollment, fallback to certificate `endDate`). Before this date, an informative countdown timer is displayed.
- **Payout Setup Requirement**: Intern must configure and verify their Fernet-encrypted UPI ID on their profile before submitting their contribution dossier.
- **Provisional Candidates Locked View**: Candidates with provisional status (`isProvisional: true`) see a locked stipend dashboard:
  - Prominent alert: *"Verification Required: Your certificate is currently Provisional"*.
  - Action CTA button: *"Complete Verification to Unlock Stipend"* deep-linking to `https://dbert.in/enroll/1999?email={email}` (or `/eroll?email=...`).
  - No access to submit contributions until verified.
- **LMS Authentication & Tracking**: Interns must authenticate at LMS portal (`https://lms.dbert.in`). All milestone submissions, AI reviews, and payout disbursements are tracked within their individual student profile. Seamless onboarding allows verified certified candidates without an LMS account to activate with 1-click password setup.

### 13.2. Technical Contribution, AI Pre-Screening & 5,000 Coins Payout Engine
1. **Domain-Specific Task Tracks**:
   - Matching the intern's certified domain: AI & Machine Learning, Data Analyst, Full Stack Web Development, Python Automation.
   - Requires: GitHub Repository URL, Live Demo / Deployment URL, and Technical Contribution Report PDF.
2. **Automated AI Pre-Screening Engine (`GeminiProvider`) & Silent-Fail Elimination**:
   - Upfront strict validation of `GEMINI_API_KEY` via an in-portal Admin Health Card (`/admin`) and pre-flight probe. Submissions are safely halted if AI is unconfigured to prevent silent failures.
   - On submission, AI evaluates deliverables against domain rubrics, outputting an informational 0–100 score, rubric breakdown, and summary notes.
   - Dual notification automatically dispatched: Confirmation email via Google Workspace SMTP + real-time in-app status timeline.
3. **Staff / Admin Review Queue (`/staff/tasks/<id>/decision`)**:
   - Staff queue displays AI score badge and rubric breakdown.
   - Human staff holds final approval authority.
   - 1-click "Approve & Release Stipend" button atomically credits **5,000 coins** to LMS wallet (`coin_ledger_mirror` with `ledger_kind='referral'` withdrawable balance) and dispatches an approval email.
4. **LMS Wallet & UPI Payout Engine**:
   - Intern visits `/intern/ambassador/withdraw` and clicks "Request Payout" for their 5,000 coins.
   - Admin reviews decrypted UPI ID (with single-reveal audit log) and executes payout on `/admin/ambassador-payouts`.
5. **Database & Sync Architecture**:
   - Dual-layer verification check in `CertificateService.is_intern_verified()`: Primary lookup in PostgreSQL `intern_certificates`, auto-healing fallback to `certificates_registry.json`.
   - Seeding and sync script: `scripts/sync_verified_certificates_to_portal.py` to ensure all 66 verified candidates are synced to LMS PostgreSQL.
   - Master implementation plan: [`stipend_contribution_and_lms_tracking_plan.md`](file:///C:/Users/user/.gemini/antigravity/brain/59004557-b26d-4b45-b8e4-941544fadc24/stipend_contribution_and_lms_tracking_plan.md).

---

## 14. Unified 3-Document Certificate Generation & Executive Print Dossier (`/portal/certificate/<cert_id>/print`)

### 14.1. Visual & Structural Parity Mandate
- **Exact Email Parity**: Web-rendered printable certificates on `/portal/certificate/<cert_id>/print` must match the official 3-document credential packet sent via authenticated Google Workspace SMTP:
  1. **Document 1 (Certificate of Completion)**: 640 × 495 Landscape canvas with `targets12.png` luxury slate artwork, gold hairline rules, Palatino/Georgia typography, Mr. Abhinav Sharma's signature, and verification QR code.
  2. **Document 2 (Academic Project Evaluation)**: US Letter Portrait with double navy/gold border, 9-dimension rubric table, 100-mark scoring (`score/100`), Turnitin originality validation seal, and signatory sign-off.
  3. **Document 3 (Letter of Recommendation)**: US Letter Portrait with official letterhead, ref `LOR-DBERT-{certId}`, 4-paragraph technical endorsement, and executive signature.
- **Engine**: Encapsulated in `apps/portal/services/certificate_packet_service.py` using ReportLab and PyMuPDF (`fitz`).
- **Dynamic Master PDF Generation**: Merges all 3 documents into a single 3-page vector master PDF (`/portal/certificate/<cert_id>/pdf`).
- **Individual Downloads**: Dedicated routes for standalone documents (`/portal/certificate/<cert_id>/download/1`, `/2`, `/3`) and high-res previews (`/portal/certificate/<cert_id>/preview/1`, `/2`, `/3`).
- **Executive Dossier UI**: `apps/portal/templates/certificate_dossier.html` provides interactive tab switching between all 3 documents, 1-click "Print Master PDF", standalone download dropdown, and deep-link to public verification (`https://dbert.in/verify?certid={cert_id}`).

### 14.2. Global LMS Navigation Bar & Responsive Routing
- **LMS Integration Mandate**: The printable credential dossier (`/portal/certificate/<cert_id>/print`) is an integral LMS portal feature (`lms.dbert.in`), not an external static website page.
- **Top Navigation Bar (`.lms-navbar`)**: Positioned sticky at the top (`z-index: 60`), providing direct navigation across LMS routes:
  - Home (`/`), My Portal (`/portal`), Courses (`/courses`), Sprint Tasks (`/tasks`), Stipend Milestone (`/stipend/tasks`), 1:1 Mentorship (`/mentors/slots`), and Placements & Jobs (`/jobs`).
  - Mobile responsive drawer with burger menu toggle (`#lmsMenuBtn`, `#lmsMobileMenu`).
  - Sub-header (`.dossier-header`) and tab switcher (`.dossier-tabs`) smoothly stack below the LMS navbar.
- **Strict Print Isolation**: `@media print` cleanly suppresses both `.lms-navbar` and `.dossier-header` to output unblemished, full-page credential certificates.

### 14.3. Document Security & Right-Click Prevention
- **Anti-Tampering & Asset Integrity**: Right-click context menus (`contextmenu` event) and drag-and-drop (`dragstart` event) are strictly intercepted and prevented across all document stages, preview canvases, and cards (`.dossier-stage`, `.doc-card`, `.doc-frame`, `.doc-frame img`).
- **CSS Anti-Selection**: `user-select: none; -webkit-user-drag: none;` applied to all rendered credential previews.
- **Interactive Security Toast (`#protectionToast`)**: When right-click or `Ctrl+S` is attempted on the document view, an executive floating security badge informs the user that official credentials are protected and directs them to use the authorized Master PDF / Print buttons.

---

## 15. Group Mentorship Sessions & Cascading Calendar Booking System (`/mentors/slots`)

### 15.1. Cascading 3-Step Booking Engine (`session_booking.html`)
- **Step 1: Domain Track & Mentor Filtering**:
  - Filter by Domain: `All Tracks`, `Data Analyst`, `AI / Machine Learning`, `Full Stack Web Development`, `Python Automation`. Auto-defaults to the intern's verified domain track.
  - Filter by Mentor: Dropdown allowing interns to filter by specific mentor or view all recommended faculty mentors.
- **Step 2: 14-Day Visual Date Strip**:
  - Horizontal scrollable strip of 14 calendar day cards starting from today (`09 NOV`, `10 NOV`, etc.).
  - Each card shows day of week, day number, month, and real-time available session badges (`5 Slots`, `None`, etc.).
  - Selecting any date highlights the card with gold/blue illumination and instantly filters available sessions.
- **Step 3: Session Cards with Live Capacity Meter**:
  - Time chips: Strictly within mandatory 14:00 – 20:15 IST window (45-minute sprint blocks).
  - Mentor details: Avatar, faculty title, domain track pill, and session agenda topic.
  - Live Capacity Meter: Interactive bar showing `seats_booked / capacity` (up to 30 interns per session).
  - Status indicators: `🟢 Open` (>5 seats), `🟡 Filling Fast` (1–5 seats left), or `🔴 Session Full` (30/30).
  - 1-Click "Reserve Seat (Free)" button (or "✓ Seat Reserved" if already booked).
- **Step 4: My Scheduled Sessions**:
  - Confirmed session list with direct 1-click **Join Google Meet ↗** link.
  - 1-click **Add to Google Calendar** URL generator.
  - 1-click **Cancel Reservation** button releasing seat back to cohort.

### 15.2. Group Capacity & Concurrency Protection
- **Capacity**: Sessions support **up to 30 interns simultaneously** (`capacity INTEGER DEFAULT 30`, `seats_booked INTEGER DEFAULT 0`).
- **Compound Uniqueness**: `UNIQUE(slot_id, intern_id)` on `mentor_session_bookings` prevents duplicate reservations while enabling cohort scalability.
- **Atomic Reservation (PAY-001 / RAC-002)**: Check-and-increment transaction prevents race conditions and ensures total bookings never exceed slot capacity under concurrent load.

### 15.3. Mentor Faculty Console (`/staff/mentor-slots`)
- **Session Publisher**: Mentors set start/end times within 14:00 – 20:15 IST, domain track, topic agenda, and capacity up to 30.
- **Live Roster**: Mentors can view all registered interns (Name, Email, Booked timestamp) for each of their scheduled sessions.
- **CSRF Protection**: `bookSlot()` incorporates `X-CSRF-Token` header to ensure seamless, error-free booking transactions.

---

## 16. College Ambassador & Referral Subsystem (`/ambassador`, `/intern/ambassador`)

### 16.1. Defect Remediation & Security Hardening
- **Encoding & Mojibake Elimination**:
  - Replaced corrupted mojibake bytes (`'â€¢'`) in `mask_upi()` with unicode bullet constant `\u2022`.
  - Display renders cleanly as `kus•••@okhdfcbank` across all browsers and operating systems.
- **CSRF Token Attachment**:
  - `saveUpi()` and `requestWithdrawal()` in `ambassador.html` now include `'X-CSRF-Token': '{{ csrf_token() }}'` in request headers, eliminating 403 Forbidden rejections.
- **Pending Balance Display Logic**:
  - `pendingRow` (`#ambPendingRow`) is strictly hidden when `pending_withdrawal <= 0`, preventing false "₹0 already requested" alerts.
- **Zero-Error Alert Initialization**:
  - Removed dangling raw `.alert.alert-err` blocks from the initial DOM; error alert dynamically populates only upon actual API errors.
- **Sidebar Layout Integration**:
  - Standardized wrapper with `<div class="main" id="main-content"><div class="content">`, completely preventing 240px fixed sidebar clipping.

### 16.2. Referral Attribution, Wallet & Payout Engine
- **Anonymous Tracking**: Referral clicks via `/r/click?ref=<code>` tracked without session dependencies.
- **Attribution & Anti-Fraud**: `attach_referral_on_signup` safely binds new students to their referrer; blocks self-referrals and duplicate attributions.
- **10% Commission Calculation**: When an attributed student enrolls (e.g., ₹1,999), 10% (₹200) is atomically credited to the ambassador's withdrawable wallet (`coin_ledger_mirror` with `ledger_kind='referral'`).
- **Fernet Encrypted UPI ID**: Payout destinations stored with Fernet symmetric encryption; only revealed to authorized administrators during single-reveal payout processing with full audit logging.
- **Double-Spend & Overdraw Prevention**: Validates withdrawal amounts against available balance; enforces atomic ledger debits upon admin execution at `/admin/ambassador-payouts`.
- **E2E Test Suite**: Verified via `scripts/test_ambassador_e2e.py` covering all 10 lifecycle stages with 100% pass rate.

---

## 17. Sovereign REST API Developer Platform & Instructions Hub (`https://api.dbert.in`)

### 17.1. Public Developer Hub & Onboarding Landing Page (`GET /`, `/instructions`)
- **Sovereign Domain**: `https://api.dbert.in` (FastAPI Uvicorn running on port 8000 reverse-proxied through Nginx with HTTP/2 and TLS 1.3).
- **Interactive Developer Portal**: Replaces former 404 response on `/` with a comprehensive, responsive, executive developer portal:
  - **4-Step Quickstart Instructions**: Base URL setup (`https://api.dbert.in/api/v1`), JWT Bearer Token acquisition (`/api/v1/auth/*`), header specification (`Authorization: Bearer <token>`), and idempotent JSON response handling.
  - **Multi-Language Interactive Code Snippets**: Tabbed copy-paste examples in cURL, Python (requests/httpx), JavaScript (fetch), and Node.js (axios).
  - **Core Architectural Modules**: Deep-dive summaries for 15 domains including Credentials Verification, Job Marketplace (6,600+ vetted openings), Application State Machine, Courses & AI Guided Tutor, Ambassador Referrals, and Payments.
  - **Interactive Searchable Endpoint Catalog**: Table covering primary production endpoints with HTTP method pills (`GET`, `POST`, `PUT`, `DELETE`), authorization level, description, and direct links to test within Swagger UI.
  - **Direct Documentation Launchers**: One-click links to Swagger UI (`/docs`), ReDoc (`/redoc`), OpenAPI 3.1 JSON (`/openapi.json`), and Liveness Probes (`/health`, `/ready`, `/status`).

### 17.2. Dual Content Negotiation & Machine Discovery (`/`, `/api`, `/api/v1`)
- **JSON Negotiation**: If client header includes `Accept: application/json` or query param `?format=json`, `/` returns a structured JSON API Manifest instead of HTML, allowing CLIs, SDKs, and automated agents to discover capabilities instantly.
- **API Version Discovery**: Dedicated routes `GET /api` and `GET /api/v1` provide machine-readable discovery indices of all available routes and modules.
- **OpenAPI Schema Metadata**: Enhanced `FastAPI` instance configuration with server endpoints (`https://api.dbert.in`, `http://127.0.0.1:8000`), detailed markdown description, and support contact coordinates (`engineering@dbert.in`).

---

## 18. Multi-Sector Domain Architecture (9 Core Technical & Growth Domains)

### 18.1. Scope & 9 Standardized Career Tracks
DBERT operates across **9 canonical career tracks** providing end-to-end alignment across job/internship discovery (`/jobs`, `/internships`), courses & Launchpad curricula (`/courses`, `/learners/courses`), pre-selection AI interviews (`InterviewService`), stipend evaluation rubrics (`GeminiProvider`), and 3-document credential generation (`CertificatePacketService`):

| # | Canonical Domain Name | Domain Slug | Key Focus & Tech Stack |
|---|---|---|---|
| 1 | **AI Agent Development** | `ai-agent-development` | Autonomous Agents, RAG Pipelines, Tool Calling, LangChain, FastAPI |
| 2 | **Data Analyst** | `data-analyst` | SQL, Python Pandas, Tableau/PowerBI, EDA, Variance & Driver Decomposition |
| 3 | **Full Stack Development** | `full-stack-development` | React/Next.js, Python Flask/FastAPI, Node.js, PostgreSQL/SQLite, Docker |
| 4 | **Python Automation** | `python-automation` | Web Scraping (Playwright/Selenium), ETL Pipelines, API Automation, RPA |
| 5 | **UI/UX Design** | `ui-ux-design` | Figma Design Systems, User Research, Wireframing, Design Tokens, UX Audits |
| 6 | **DevOps & Cloud** | `devops-cloud` | AWS/GCP, Docker, Kubernetes, CI/CD Actions, Terraform, Prometheus/Grafana |
| 7 | **Mobile App Development** | `mobile-app-development` | React Native, Flutter, Android (Kotlin), iOS (Swift), Mobile API Integration |
| 8 | **Cybersecurity** | `cybersecurity` | Threat Modeling, SOC Analysis, Penetration Testing, OWASP, Network Security |
| 9 | **Digital Marketing** | `digital-marketing` | Growth Engineering, SEO, Google/Meta Ads, Funnel Analytics, Content Systems |

### 18.2. Database Segregation & Automated Seeding
- **Active Posts Table**: Segregated in PostgreSQL (`dbert_internship.posts`) on EC2 (`3.26.237.171`) and local SQLite (`internship.db`).
- **Post Distribution**: Minimum 5-16 verified internships and 2-3 jobs per domain (111 active published postings total).
- **Migration Script**: `scripts/migrate_and_seed_9_domains.py` supports dual modes:
  ```powershell
  # Local SQLite migration
  python scripts/migrate_and_seed_9_domains.py --sqlite apps/portal/internship.db

  # Production EC2 PostgreSQL migration
  python scripts/migrate_and_seed_9_domains.py --pg-url "postgresql://dbert_user:...@localhost:5432/dbert_lms" --schema "dbert_internship"
  ```

### 18.3. Cross-Service Domain Integration
1. **Portal Routing & Listings (`apps/portal/app.py`)**:
   - `VALID_DOMAINS` and `DOMAIN_SLUGS` support all 9 tracks with clean URL routing (`/jobs/<domain_slug>`, `/internships/<domain_slug>`).
   - `DOMAIN_SEO` provides bespoke metadata, page titles, and H1 tags for all 9 domains.
   - `DOMAIN_COURSES_METADATA` holds 3-day structured curriculum metadata without bloating active SQLite/PostgreSQL `courses` tables.
2. **Sourcing & Scraper Pipeline (`services/sourcing/`)**:
   - `normalizer.py` automatically classifies incoming job/internship leads from Unstop, Indeed, LinkedIn, and DuckDuckGo search aggregators into the 9 canonical domains.
3. **Pre-Selection AI Interview Engine (`services/interview_service.py`)**:
   - `INTERVIEW_DOMAIN_BANK` houses tailored technical, applied, and communication question sets for all 9 domains.
4. **Stipend Review Engine (`services/ai/stipend_evaluator.py`)**:
   - `DOMAIN_RUBRICS` provides 4-category evaluation rubrics for AI pre-screening across all 9 domains.
5. **Credential Packet Generation (`services/certificate_packet_service.py`)**:
   - `topics_map` generates official academic curriculum descriptions on Document 2 (Academic Evaluation) and Document 3 (LOR).
6. **Sovereign Website Launchpad (`apps/website/src/data/launchpadDomains.ts`)**:
   - Provides comprehensive 2-month curricula, module breakdowns, capstone deliverables, and GitHub repository blueprints for all 9 tracks.


---

## 19. Institutional Trust, Program Transparency & Credibility Standards
================================================================================

### 19.1. Canonical Terminology & Program Durations
1. **Single Unified Incubation Duration**: All cohort references, course schema JSON-LD, FAQs, and marketing copy strictly use **2 Months (8 Weeks)** (`P2M` / `P60D`). Legacy mentions of "three months" are completely retired.
2. **Guaranteed Placement Disambiguation**:
   - DBERT strictly guarantees **Active Production Codebase Assignment** under senior engineer code review, 1-on-1 technical mentorship, and an independently verifiable 3-document credential packet.
   - DBERT **does not claim or guarantee unconditional permanent corporate employment**. Unconditional job guarantees are misleading and prohibited across all copy.
3. **Zero Application Fee Guarantee**: DBERT never charges application, registration, screening, or interview fees. Initial selection is 100% merit-based.

### 19.2. Performance Stipend Governance & Audited Rubrics
- Stipends (₹5,000–₹18,000) are performance-based and earned against delivery milestones submitted through the LMS task portal (`/stipend/tasks`).
- Evaluated against 4 objective engineering dimensions:
  1. *Code Quality & Cleanliness*: Linting (PEP8/ESLint), typing, modular separation, error boundaries.
  2. *Architecture & Security*: Database migrations, parameterization, zero hardcoded secrets.
  3. *Practical Feasibility & Testing*: Unit/integration tests, live deployability.
  4. *Technical Documentation*: Comprehensive READMEs, architecture decision records.
- Approved disbursements are released atomically via UPI directly to the fellow's verified account.

### 19.3. Statutory Disclosure & Entity Clarification
- **Parent Legal Enterprise**: *Digital Blinc Education Research And Technology* (MSME / UDYAM compliant).
- **Official Government Verification**: Direct link to `https://udyamregistration.gov.in/Udyam_Verify.aspx`.
- **Statutory Distinction**: MSME registration establishes formal legal entity compliance under Indian law; it does not replace UGC/AICTE degree accreditation. DBERT credentials represent audited production software engineering evidence.
- **Entity Advisory**: Zero affiliation with discontinued third-party operations or unofficial recruitment agencies soliciting fees under similar legacy names.

### 19.4. Published Metrics Hierarchy
To maintain mathematical consistency across all web portals:
- **1,500+ Evaluated Learners**: Developers and university students upskilled across open hackathons, masterclasses, and foundational assessments.
- **465+ Certified Fellows in Sovereign Directory**: Formally registered candidates with verifiable UUID credentials in our public [Alphabetical Credential Directory](https://dbert.in/verify/directory).
- **120+ Venture Incubation Fellows**: Selective cohorts deployed on live venture client repos and multi-agent systems.

---

## 18. Comprehensive 9-Domain SEO Architecture, Sitemaps & Cross-Domain Link Mesh

### 18.1. Architecture & Keyword Silos Across 9 Domains
Both `https://dbert.in` (Main Website & Verification Engine) and `https://lms.dbert.in` (LMS & Career Hub) are structured into 9 unified technical and growth domains:
1. **AI Agent Development** (`ai-agent-development`)
2. **Data Analyst & Power BI** (`data-analyst`)
3. **Full Stack Development** (`full-stack-development`)
4. **Python Automation & Scraping** (`python-automation`)
5. **UI/UX Design & Prototyping** (`ui-ux-design`)
6. **DevOps & Cloud Engineering** (`devops-cloud`)
7. **Mobile App Development** (`mobile-app-development`)
8. **Cybersecurity & Threat Defense** (`cybersecurity`)
9. **Digital Marketing & SEO** (`digital-marketing`)

### 18.2. Sitemaps Generation & Canonical Indexing
- **`https://dbert.in/sitemap.xml`**:
  - Dynamically generated from `apps/website/src/data/seo.config.ts`, `apps/website/src/lib/blog.ts`, and verified candidates in `certificates_registry.json`.
  - All 9 course tracks mapped at `/learners/courses/<domain>` with priority `0.9` and weekly change frequency.
  - Automatically synced to `public/sitemap.xml` and standalone build assets on EC2.
- **`https://lms.dbert.in/sitemap.xml`**:
  - Programmatically indexed across all 9 domains for category hubs (`/internships/<domain>`, `/jobs/<domain>`), work-from-home filters (`/internships/work-from-home/<domain>`), paid filters (`/internships/paid/<domain>`), remote filters (`/internships/remote/<domain>`), and programmatic city corridors (Bangalore, Pune, Delhi NCR, Hyderabad, Mumbai, Chennai, Remote).
  - Indexes all live direct company postings and active curated job/internship leads for Google Jobs search indexing.

### 18.3. Cross-Domain Footers & Structured Data Parity
- **Website Global Footer (`Footer.tsx`)**:
  - Multi-column layout featuring all 9 domain course paths under **AI Academy** and deep linking to live sourced opportunities on `lms.dbert.in` (`/internships/remote/<domain>`, `/internships/virtual-remote-internships`, `/internships/paid-internships`, `/jobs`).
  - Trust & Verification column cross-linking to `/verify`, `/verify/directory`, and `/enroll/1999`.
- **LMS Global Footer (`_footer_seo.html`)**:
  - Standardized across `post_listings.html`, `post_detail.html`, `scraped_internship_detail.html`, and `index.html`.
  - Responsive 4-column link mesh (AI & Engineering, Data/Design/Growth, Sourced Hubs & Modes, Verification & Studio) targeting high-intent long-tail keywords.
- **Google `JobPosting` Structured Data (`index.html`)**:
  - Full schema JSON-LD covering all 9 technical domains with realistic compensation ranges (₹5,000–₹18,000/month), direct apply links, and telecommute indicators.


---

## 19. DBERT Platform Evolution Roadmap Execution & Production Baseline (Phases 0–9)

### 19.1. Phase 0: Baseline Discovery & Audit Artifacts
All canonical system audit deliverables specified in `DBERT_PLATFORM_EVOLUTION_ROADMAP.md` are established in `docs/dbert-roadmap/audit/` and deployed to EC2:
1. **Repository Map (`docs/dbert-roadmap/audit/repository-map.md`)**: Complete infrastructure mapping (Next.js 16 on port 3000, Flask LMS on port 5001, FastAPI on port 8000, Nginx reverse proxy, PostgreSQL 15, and SQLite fallbacks).
2. **Route Inventory (`docs/dbert-roadmap/audit/route-inventory.csv`)**: 533 total cataloged endpoints across `dbert.in`, `lms.dbert.in`, and `api.dbert.in` with handler files and auth requirements.
3. **Data Model Map (`docs/dbert-roadmap/audit/data-model-map.md`)**: Entity-relationship mapping of PostgreSQL tables (`users`, `companies`, `posts`, `scraped_internships`, `intern_applications`, `tasks`, `task_submissions`, `intern_certificates`, `coin_ledger_mirror`), Prisma schemas, and JSON registries.
4. **Integration Map (`docs/dbert-roadmap/audit/integration-map.md`)**: Configuration details, protocols, credentials, rate limits, and circuit breakers for Google Workspace SMTP, GA4 (`G-MN7ME9X518`), WhatsApp Playwright dual-engine, Google Gemini 2.5 AI, Razorpay/UPI (`Q652429146@ybl`), and AWS EC2.
5. **Test Baseline (`docs/dbert-roadmap/audit/test-baseline.md`)**: Automated test suites in `apps/portal/tests/` (12/12 pytest passed), `dbert-api-package/tests/` (remediation security suite), and Next.js static route audits.
6. **Current Public Claims Audit (`docs/dbert-roadmap/audit/current-public-claims.md`)**: Programmatic validation of public claims (₹1,999 program fee with ₹499 caution deposit credit = ₹1,500 net balance; 60-day sprint duration; 65 verified vs 400 provisional candidates; MSME accreditation disclaimer; active Alkame open-source repo).
7. **Risks and Unknowns Log (`docs/dbert-roadmap/audit/risks-and-unknowns.md`)**: Operational mitigations for Google Workspace SMTP 24h rolling quotas, candidate privacy-by-default, and Next.js standalone build symlinks.

### 19.2. Phase 1: Programme Truth & Financial Ledger Alignment
- **Single Source of Truth**:
  - `https://dbert.in/terms` and `https://dbert.in/refund` aligned with `https://lms.dbert.in/terms` and `https://lms.dbert.in/program`.
  - Free Internship Track: Zero application/screening fee; 100% refundable security deposit returned upon milestone completion.
  - Incubation Program: ₹1,999 total committed seat fee (or ₹1,500 balance payable if ₹499 caution deposit was credited).
  - Performance Stipend: ₹5,000–₹18,000 milestone-based, governed by Turnitin/rubrics, submitted via `/stipend/tasks` and approved by senior staff.

### 19.3. Phase 2: Marketplace Sourcing Integrity & Database Type Safety
- **Dual Source Badging**:
  - Direct employer listings tagged with `.source-pill-portal` (`Direct Company Posting`).
  - Aggregated engineering leads tagged with `.source-pill-curated` (`Curated Sourced Lead`).
- **PostgreSQL Database Type Coercion**:
  - In `apps/portal/app.py` lines 12134 and 12452, patched `post_comments` joins with explicit casts `CAST(a.id AS TEXT) = CAST(pc.intern_id AS TEXT)` and `CAST(pc.post_id AS TEXT) = ?` to prevent PostgreSQL `operator does not exist: integer = text` errors.
- **Fit Breakdown Modal UI & Accessibility**:
  - Upgraded `.match-btn-close` and header close buttons in `post_listings.html` with explicit borders, high-contrast dark text, font-awesome icons, and elevated shadows to eliminate unstyled plain text appearance.
- **Scraped Opportunity Domain Audit**:
  - Audited all 6,622 active scraped leads across all 9 domains in PostgreSQL on EC2 (`scraped_internships`: 4,565 Full Stack, 649 Digital Marketing, 525 AI Agent, 372 Data Analyst, 200 UI/UX, 117 DevOps, 112 Python, 43 Cybersecurity, 39 Mobile).
  - Validated that Lead 3307 (`Social Media Marketing Internship | Niswarth - The Selfless NGO`) is strictly categorized under `Digital Marketing`.

### 19.4. Phases 3–9: End-to-End Operational Continuity & Deployment
- **Pre-Vetted Directory**: Verified candidates surfaced first by hireability rank (98, 97, 96...) at `/verify/directory`, linked from `/hire/pre-vetted-engineers` with dual CTAs (`View Proof Dossier` & `Connect on LMS`).
- **Cryptographic Verification**: Exact-ID lookups on `dbert.in/verify/[certId]` rendering official 3-document credential packets.
- **Production Build & Verification**: Next.js Turbopack standalone successfully rebuilt on EC2, public assets synced, `/data` symlinks preserved, and systemd units (`dbert-website.service`, `dbert-portal.service`) running active (HTTP 200 on all endpoints).

---

## 20. Pre-Vetted Engineers Directory, Add-On SEO & Omnichannel Sitemaps Architecture

### 20.1. Strict Add-On Mandate & Zero-Disruption Policy
- **Additive SEO Principle**: All enhancements are strictly additive ("Add-On" only). 100% of pre-existing SEO keywords (`DBERT candidate directory`, `verify DBERT certificate`, MSME statutory disclosures, course hubs), candidate records, routes, and rankings are fully preserved.
- **Dual-Audience Intent**: The candidate directory (`/verify/directory`) serves a dual audience:
  1. **Candidate Verification**: Students and institutions verifying certificate authenticity and academic rubrics.
  2. **B2B Engineering Recruitment**: Startups and enterprise hiring managers looking to onboard pre-vetted AI, Full Stack, and Data engineers with verified Turnitin scores and live GitHub pull requests.

### 20.2. Pre-Vetted Directory Structured Data & Rich Snippets (`/verify/directory`)
- **Tri-Schema JSON-LD Implementation**:
  1. **`ItemList` Schema**: Formats all 465 candidate records into structured `Person` entities, detailing their specialization domain, evaluation score (e.g. 98/100), verified credential ID, and public proof dossier URL.
  2. **`BreadcrumbList` Schema**: Declares hierarchy (`Home` -> `Audited Credentials` -> `Pre-Vetted Engineers Directory`) for clean SERP navigation breadcrumbs.
  3. **`FAQPage` Schema**: Implements 5 structured Q&A entities addressing recruiter concerns:
     - How DBERT vets candidates (Turnitin originality, architecture reviews, production PRs).
     - 48-hour onboarding turnaround time.
     - Available technical domains (AI Agents, Full Stack, Python Automation, Data Analytics).
     - 14-day risk-free trial and zero recruiter placement commissions.
     - LMS messaging and direct dossier access.
- **Visual Recruiter Callout Banner**: High-contrast dark slate card linking directly to `/hire/pre-vetted-engineers` with prominent CTA: *"Deploy pre-vetted AI & Full Stack engineers in 48 hours"*.
- **Recruiter FAQ Accordion**: Interactive native FAQ accordion rendered below candidate cards.

### 20.3. SEO Bounds Enforcement (`apps/website/src/data/seo.config.ts`)
- **Rule Verification (`npm run check:seo`)**:
  - Validates all 75 routed pages against strict character constraints: `title <= 52` characters, `description >= 140 && description <= 155` characters.
  - Resolved 6 length bounds violations (`/learners/launchpad`, `/learners/courses/ui-ux-design`, `/learners/courses/devops-cloud`, `/learners/courses/mobile-app-development`, `/learners/courses/digital-marketing`, and `/verify/directory`).
  - Result: **75 entries checked against 75 routed pages, 0 errors, 100% pass rate**.

### 20.4. Omnichannel Sitemaps Architecture & Search Engine Discovery
- **Website Dynamic Sitemap (`https://dbert.in/sitemap.xml`)**:
  - 144 fully indexable URLs including core hubs, courses, products, startups, blog posts, and 65 verified candidate certificates.
  - `/verify/directory` and `/hire/pre-vetted-engineers` assigned **Priority 0.95** with **daily** change frequency.
  - Generated via `apps/website/src/app/sitemap.ts` and mirrored to `public/sitemap.xml` during Next.js standalone build.
- **LMS Dynamic Sitemap (`https://lms.dbert.in/sitemap.xml`)**:
  - Over 10,000 indexable URLs (10,012 live links) spanning active career opportunities, curated domain categories, tech hubs (Bangalore, Pune, Delhi NCR, Hyderabad, Remote), and public portfolios.
  - Date queries parameterized (`WHERE End_Date >= ? OR End_Date IS NULL`, `(today,)`) ensuring seamless portability across SQLite and PostgreSQL databases.
- **Search Engine Directive Compliance (`robots.txt`)**:
  - `https://dbert.in/robots.txt` explicitly points to both `https://dbert.in/sitemap.xml` and `https://lms.dbert.in/sitemap.xml`.
  - Grants full crawl permission to `Googlebot`, `Mediapartners-Google`, `Googlebot-Image`, and standard crawlers.

### 20.5. Internal Link Equity & Cross-Domain Navigation Web
- **Header Mega-Menu (`apps/website/src/data/nav.config.json`)**:
  - Added `"Pre-Vetted Engineers Directory"` under `For Startups` -> `Resources` with highlight badge.
- **Website Footer (`apps/website/src/components/layout/Footer.tsx`)**:
  - Under `Startups & Equity`: Added `"Hire Pre-Vetted Engineers"` (`/hire/pre-vetted-engineers`) and `"Pre-Vetted Engineers Directory"` (`/verify/directory`).
  - Under `Labs & Trust`: Updated `"A–Z Candidate Directory"` to `"Pre-Vetted Candidate Directory"`.
- **LMS Footer (`apps/portal/templates/_footer_seo.html`)**:
  - Added `"Hire Pre-Vetted Talent"` badge item in top brand strip.
  - Updated Column 4 with `"Hire Pre-Vetted Engineers"` and `"Pre-Vetted Candidate Directory"`.
- **LMS Sourced Post Listings (`apps/portal/templates/post_listings.html`)**:
  - Embedded high-conversion Recruiter Sidebar Callout card in the left filter rail linking candidates and employers directly to `https://dbert.in/verify/directory`.
- **Hire Landing Page (`apps/website/src/app/hire/pre-vetted-engineers/page.tsx`)**:
  - Added primary hero CTA button: `Browse Pre-Vetted Directory →` linking directly to `/verify/directory`.

---

## 21. Pre-Vetted Domain Directories & Recruiter Skills Filtering Architecture

### 21.1. Specialized Domain Sub-Pages (`/verify/directory/[domainSlug]`)
- **Canonical Routing & Hierarchy**:
  - Parent Hub: `https://dbert.in/verify/directory` (465 total candidates: 65 verified + 400 provisional).
  - 7 Specialized Domain Pages:
    1. `/verify/directory/full-stack-development`: Pre-Vetted Full Stack Developers (Next.js, React 19, TypeScript, Node.js, PostgreSQL).
    2. `/verify/directory/ai-machine-learning`: Pre-Vetted AI & Machine Learning Engineers (PyTorch, LangChain, FastAPI, RAG, Transformers).
    3. `/verify/directory/data-analytics`: Pre-Vetted Data Analysts & BI Engineers (SQL, Python Pandas, Power BI, Tableau, ETL).
    4. `/verify/directory/python-automation`: Pre-Vetted Python Automation Engineers (Playwright, Selenium, Celery, Redis, Scraping).
    5. `/verify/directory/ui-ux-design`: Pre-Vetted UI/UX Product Designers (Figma, Auto-Layout, Design Systems, WCAG).
    6. `/verify/directory/devops-cloud`: Pre-Vetted DevOps & Cloud Engineers (Docker, Kubernetes, AWS, CI/CD, Linux).
    7. `/verify/directory/mobile-app-development`: Pre-Vetted Mobile App Developers (Flutter, Dart, React Native, Firebase).
- **Static Generation (SSG)**:
  - All 7 routes pre-rendered statically via `generateStaticParams()` in Next.js 16 App Router for instant TTFB and 100% search engine indexability.

### 21.2. Interactive Recruiter Skills & Multi-Select Filter Engine
- **Horizontal Domain Pill Nav**:
  - Sleek, mobile-scrollable domain navigation pill bar at the top of the directory with live candidate counters per domain (`All Domains: 465`, `AI & ML: 165`, `Data Analytics: 153`, `Full Stack: 112`, etc.).
  - Highlights active domain with gold accent glow (`.domainPillLinkActive`).
- **Interactive Tech Stack Chips**:
  - 1-click toggle buttons for top domain technologies (e.g. `Next.js`, `PyTorch`, `SQL`, `Playwright`, `Docker`, `Figma`, `Flutter`).
  - Multi-select support with active counter badge, checkmarks (`✓`), and 1-click "Clear Skills Filter" button.
- **Dynamic Hireability Ranking & Dual CTAs**:
  - Candidates sorted dynamically by 100-point rubric score (98, 97, 96...) with Top Tier Distinction badge.
  - Dual recruiter action buttons:
    * `View Proof Dossier →`: Direct link to cryptographic verification dossier at `/verify/[certId]`.
    * `Connect on LMS →`: Direct routing to `https://lms.dbert.in/company/signup?ref=directory&candidate=[certId]` for instant employer registration and candidate messaging.

### 21.3. Structured Data (JSON-LD) & Domain SEO
- **Domain-Tailored Tri-Schema JSON-LD**:
  1. **`ItemList` Schema**: Formats candidates strictly within that domain as structured `Person` entities with evaluation scores and proof URLs.
  2. **`BreadcrumbList` Schema**: Declares hierarchy (`Home` -> `Pre-Vetted Directory` -> `[Domain Name] Engineers`).
  3. **`FAQPage` Schema**: 4 domain-tailored technical screening Q&As per page addressing framework competency, git review standards, 48h turnaround, and 14-day risk-free trial.
- **Sitemap Priority & Daily Frequency**:
  - All 7 domain directory URLs registered in `https://dbert.in/sitemap.xml` with **Priority 0.90** and **daily** change frequency.

### 21.4. Internal Link Equity Web
- **Header Mega-Menu** (`apps/website/src/data/nav.config.json`): Direct link to Pre-Vetted Engineers Directory under `For Startups` -> `Resources`.
- **Website Footer** (`apps/website/src/components/layout/Footer.tsx`): Links to Full Stack, AI & ML, and Data Analytics directories under `Startups & Equity`.
- **LMS Footer** (`apps/portal/templates/_footer_seo.html`): Cross-links to domain talent directories under Column 4 (Trust & Verification).
- **Directory Cross-Links Grid**: Bottom grid on all directory pages rendering cards to all sibling domain rosters.


---

## 22. LMS Symmetrical Pagination (18/page), Executive Bento Footer & Pre-Vetted Engineer Proof Dossier (`/verify/[certId]`)

### 22.1. LMS Listings Symmetrical Layout (`_PAGE_SIZE = 18`)
- **Route Scope**: `https://lms.dbert.in/internships` and `https://lms.dbert.in/jobs`.
- **Symmetry Mandate**: 
  - Sliced in `apps/portal/app.py` at `_PAGE_SIZE = 18` (formerly 21).
  - Perfectly matches the standard 3-column responsive desktop layout (6 rows × 3 cards = exactly 18 cards per page) without any dangling or ragged cards.
  - Slices across all 6,700+ internships and 320+ pages seamlessly.

### 22.2. Full-Width Breakout of Tech Track & Hub Matrix (`seo-silo-matrix`)
- **Template Restructuring (`apps/portal/templates/post_listings.html`)**:
  - Moved `<section class="seo-silo-matrix">` completely outside of `.listings-body-grid` (which was trapped inside the right content column alongside the sticky left sidebar).
  - Positioned inside `.listings-page-wrap` immediately below `.listings-pagination-bar`.
  - Spans 100% full container width, effectively occupying both sidebar and content width for maximum visual weight and crawlability.
  - Features 3 high-intent categories:
    1. *Specialized Tracks*: AI Agent Development, Full Stack Development, Data Analyst, Python Automation.
    2. *Top Tech Hubs*: Bangalore (Bengaluru), Pune, Hyderabad, Delhi NCR / Noida.
    3. *High-Intent Searches*: Remote AI Agent, WFH Data Analyst, Paid AI with Stipend, Paid Full Stack.

### 22.3. Executive Silo Matrix UI & UX Architecture for Footer (`_footer_seo.html`)
- **Root Cause & CSP Nonce Resolution**:
  - The previous footer appeared as raw vertically stacked unstyled text because Flask's Content Security Policy (`style-src 'nonce-{nonce}'`) was actively stripping the footer's `<style>` tag due to a missing `nonce="{{ csp_nonce() }}"`.
  - Resolved completely by:
    1. Adding `nonce="{{ csp_nonce() }}"` to `<style>` in `_footer_seo.html`.
    2. Embedding bulletproof inline styles (`style="..."`) on key container and card elements to guarantee zero unstyled flashes.
    3. Registering `.silo-grid-4` directly in `post_listings.html`'s `<style nonce="{{ csp_nonce() }}">` in the `<head>`.
- **Design Transformation & Elimination of Stacked Text**:
  - Transformed `_footer_seo.html` to mirror the visual architecture of the `Explore Internships by Tech Track & Hub Cities` silo matrix component (`.seo-silo-matrix`).
  - Wrapped inside the exact same luxury card container: `linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%)`, `border: 1.5px solid #E2E8F0`, `border-radius: 20px`, `box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04)`.
  - **Silo Header & Trust Bar**:
    * Briefcase icon in dark slate gradient box (`linear-gradient(135deg, #0F172A 0%, #1E293B 100%)`) with gold icon `#E2B96F`.
    * Title: `DBERT LMS & Sovereign Opportunity Network` with `Venture Studio` pill badge.
    * 1-Tap Admissions Concierge WhatsApp button (`https://wa.me/917060372107`).
    * Official trust badges: `MSME Registered · NCR-HQ`, `Verify Credentials`, `Hire Pre-Vetted Talent`, `Pre-Vetted Directory`.
  - **4 Silo Cards with Interactive Pill Buttons (`.silo-card` & `.silo-link-item`)**:
    * Replaced all plain list items with interactive, clickable pill cards identical to `.silo-link-item`:
      - Background `#F8FAFC`, border `1px solid #F1F5F9`, border-radius `10px`, hover state turning to `#EFF6FF`, border `#BFDBFE`, and `transform: translateX(3px)`.
      - Domain-themed badge icons on left (`.silo-badge-track`, `.silo-badge-city`, `.silo-badge-intent`) + bold label + interactive right chevron arrow (`.silo-link-arrow`).
    1. **Card 1: AI & Engineering (7 Tracks)**: AI Agent Development, Full Stack Web Development, Python Automation & Scraping, DevOps & Cloud Engineering, Mobile App Development, AI Agent Jobs, Full Stack Developer Jobs.
    2. **Card 2: Data, Design & Growth (7 Tracks)**: Data Analyst & Power BI, UI/UX Design & Prototyping, Cybersecurity & SOC Defense, Digital Marketing & SEO, Data Analyst Roles, Product Design Roles, Cybersecurity Analyst Jobs.
    3. **Card 3: Sourced Hubs & Modes (9 Hubs)**: Virtual Remote Internships, Paid Internships (₹5k–₹18k), Remote Full Stack Sprints, Remote Data Analytics, Remote UI/UX Roles, Bangalore Hub, Pune Hub, Delhi NCR Hub, Hyderabad Hub.
    4. **Card 4: Verification & Studio (10 Links)**: Verify Credential ID (`/verify`), Hire Pre-Vetted Engineers (`/hire/pre-vetted-engineers`), Pre-Vetted Candidate Directory (`/verify/directory`), Full Stack Talent Directory (`/verify/directory/full-stack-development`), AI & ML Talent Directory (`/verify/directory/ai-machine-learning`), Incubation Program (₹1,999) (`/program`), Balance Enrollment Portal (`/enroll/1999`), MSME Disclosures (`/about/credentials`), Applied AI Fellowship Track (`/learners/fellowship`), DBERT Venture Studio (`dbert.in`).
  - **Centered Legal & Ecosystem Bar**: Centered column layout (`display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;`) with centered horizontal chip links (`Home`, `All Internships`, `All Jobs`, `Terms of Service`, `Privacy Policy`, `Student Sign In`) and centered copyright statement.

### 22.4. Pre-Vetted Engineer Proof Dossier & Profile Architecture (`/verify/[certId]`)
- **Strict User Mandate & Dual Experience Mode**:
  - **Verified Engineers (`isProvisional: false`, e.g. `CERT-DBERT-2026-DA-027`)**:
    * Rendered via `apps/website/src/app/verify/[certId]/CandidateProfileClient.tsx`.
    * Clean, distraction-free **B2B Engineer Profile & Proof Dossier**.
    * **NO incubation marketing banners**: Promotional "Guaranteed Hire", "Launch Your Career", and "Claim Certificate" cards are strictly removed for verified profiles.
    * Header surfaces: Candidate Name, Domain Badge, Academic Institution, Evaluation Score badge (e.g. `87/100 · Top Tier Distinction`), Turnitin Originality seal (`< 3.0%`), and Verification Checkmark.
    * **Direct Recruiter CTAs**:
      - `Connect on LMS →`: Deep-link to `https://lms.dbert.in/company/signup?ref=profile&candidate=[certId]` for instant employer registration and candidate messaging.
      - `Request Interview`: Direct concierge email routing with pre-populated candidate dossier reference.
      - Social verification: 1-click "Add to LinkedIn" and "Share on WhatsApp".
    * **Interactive 3-Tab Technical Appraisal**:
      1. *Tab 1: Production Capstone*: Real-world project scope, architectural stack pills, and GitHub repository verification link.
      2. *Tab 2: 9-Dimension Rubric Breakdown*: Detailed scores across Problem Formulation, Architecture & Code Quality, Prompt/Model Tuning, Documentation, etc., alongside Turnitin originality score.
      3. *Tab 3: Official Letter of Recommendation (LOR)*: Complete executive recommendation letter signed by Mr. Abhinav Sharma (Founder & Managing Director).
    * **Employer Risk-Free Guarantee**: 14-day zero-risk trial, 48-hour interview turnaround, and zero recruiter markup card.
  - **Provisional Candidates (`isProvisional: true`, e.g. `CERT-DBERT-2026-DA-057`)**:
    * Displays active sprint status with direct action CTA to `/enroll/1999?certid={certId}` for balance completion and official credential issuance.

---

## 23. Sheet (1,593 Candidates) Provisional Ingestion & Multi-Account Revenue Dispatch

### 23.1. Architectural Separation & Public Directory Shield
- **Source Sheet**: Google Sheet `1zHbzza7pVGoX6AgVKyEn5MzDMXq-2wq4uA3Iyx4fqs0` (`gid=338877142`, 1,593 candidate records).
- **Provisional Registry**: Stored strictly in `data/sheet_1593_provisional_registry.json` and `apps/website/src/data/sheet_1593_provisional_registry.json`.
- **CRITICAL DIRECTORY GATE**: Sheet provisional candidates are **NEVER** added to `apps/website/src/data/directory_candidates.json` (verified at 470 verified records). They are strictly excluded from `/verify/directory` until ₹299 project verification is completed.
- **Dynamic Lookup Resolution**: Candidate profile lookup (`/api/enroll/lookup`) and public verification route (`/verify/[certId]`) safely resolve sheet candidates with `isProvisional: true`.

### 23.2. Revenue-Optimized Verification Landing Page (`/verify/unlock`)
- **Route**: `https://dbert.in/verify/unlock?certid={certId}&email={email}`
- **Executive 6-Card Value Breakdown**:
  1. *Official 3-Document Credential Packet*: Certificate of Completion, Academic Project Evaluation (100-mark rubric), and Institutional LOR signed by Mr. Abhinav Sharma.
  2. *Turnitin Originality Rubric*: Verified plagiarism audit (<3.0%) and 9-dimension competency table.
  3. *Pre-Vetted Directory Listing*: Guaranteed inclusion on `https://dbert.in/verify/directory` upon verification.
  4. *1-Click LinkedIn Credential*: Pre-formatted credential linking directly to sovereign verification URL.
  5. *ATS-Optimized Resume Boost*: Project metrics and verified capstone details for recruiter ATS screening.
  6. *Performance Stipend Eligibility*: Unlocks access to `/stipend/tasks` for 5,000 Coin (₹5,000) disbursement.

### 23.3. Multi-Account Google Workspace SMTP Dispatch Engine
- **Dispatcher Script**: `scripts/dispatch_sheet_1593.py`
- **1-Click Launcher**: `start_sheet_1593_dispatch.bat`
- **Rotating 5-Account Pool**:
  1. `abhinav.sharma@dbert.in` (Program Head & Project Mentor)
  2. `manoj.kumar@dbert.in` (Admissions & Operations Directorate)
  3. `sandeep.bannu@dbert.in` (Technical Evaluation & Academic Review)
  4. `contactus@dbert.in` (Admissions Desk & Support)
  5. `pulkit.kunar@dbert.in` (Verification & Candidate Success)
- **Deliverability Constraints**:
  - Strict From & Reply-To header alignment per sending account.
  - Randomized human pacing: `14.0s – 26.0s` (average 20s) with 35s–50s micro-breaks every 20 emails.
  - Deduplication: Automatic cross-reference with `data/dispatch_tracking_409.json` (27 overlapping candidates automatically marked `ALREADY_SENT_409` and skipped).
  - Isolated Rate-Limiting: Any account encountering Google 550 limits is automatically placed in 24h cooldown without interrupting other accounts.
  - Milestone Telemetry: Status report dispatched every 100 emails to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.

### 23.4. Real-Time Autonomous Inbox Responder (`scripts/dbert_inbox_responder.py`)
- **Engine**: Scans all 5 Google Workspace inboxes (`abhinav.sharma`, `manoj.kumar`, `sandeep.bannu`, `contactus`, `pulkit.kunar`) via IMAP SSL (`imap.gmail.com:993`) every 60 seconds.
- **RFC 2822 Quote Stripping**: Strips prior quoted email threads and forwarded headers to isolate candidate inquiries.
- **Contextual Knowledge & Intent Matching**:
  - `PAYMENT_AND_FEE_299`: Explains ₹299 project verification deliverables and provides personalized deep-link to `/verify/unlock`.
  - `CERTIFICATE_AND_LOR_CLAIM`: Explains how to claim and download the official 3-document credential packet.
  - `STIPEND_AND_COINS`: Outlines 5,000 Coin stipend contribution on `/stipend/tasks` and UPI payout.
  - `GENERAL_INQUIRY`: Resolves candidate dossier and routes to admissions WhatsApp concierge (`+91 81929 11360` / `+91 89580 06294`).
- **Exact Mailbox Alignment**: Replies are transmitted over SMTP from the exact mailbox that received the inquiry.
- **Deduplication**: `data/inbox_replies_log.json` prevents duplicate replies to any message ID.

### 23.5. First 92 Candidates Dual WhatsApp Dispatch Engine
- **Queue Generation**: `python scripts/send_dbert_whatsapp.py --load-sheet-92` loads the first 92 uncontacted candidates from `sheet_1593_provisional_registry.json`.
- **Dual Partitioning (46 + 46 = 92)**:
  - *Account 1 (Odd Serials: 1, 3, 5... 91)*: 46 candidates assigned to `.chrome_session_account1`.
  - *Account 2 (Even Serials: 2, 4, 6... 92)*: 46 candidates assigned to `.chrome_session_account2`.
- **First 15 Lines Strict Placement**:
  - Line 8: Direct Verification Link (`https://dbert.in/verify/CERT-DBERT-2026-...`).
  - Line 11: Mandatory Claim & Verification Google Form URL.
  - Line 14: Dynamic Official Email Dispatch Notice citing the exact sending account (e.g. `manoj.kumar@dbert.in`) and sent timestamp.
- **Safety & Pacing**:
  - 18s–35s randomized human breaks between consecutive deliveries.
  - 3-consecutive-failure circuit breaker.
  - Permanent deduplication table `whatsapp_sent_log` in `data/dbert_whatsapp.db`.
- **Launchers**:
  - 1-Click: `start_sheet_1593_whatsapp_dual.bat`
  - Interactive Controller: `run_whatsapp_dispatcher.bat` (Option `[S]`)
  - Parallel Workers: `run_worker_acc1.bat` (Green) and `run_worker_acc2.bat` (Yellow).




---

## 24. Omnichannel Job & Internship Sourcing Engine & SEO Hubs

### 24.1. Core Architecture & Exact 9 Technical Domains
- **Target Domains (Strictly 9)**:
  1. `AI Agent Development`
  2. `Cybersecurity`
  3. `Data Analyst`
  4. `DevOps & Cloud`
  5. `Digital Marketing`
  6. `Full Stack Development`
  7. `Mobile App Development`
  8. `Python Automation`
  9. `UI/UX Design`
- **Adapter Suite (`scripts/scrapers/`)**:
  - `base.py`: Priority domain classifier (`normalize_domain`), SEO slug generator (`slugify`), SHA-256 composite fingerprinting (`generate_fingerprint`), and `ScrapedItem` dataclass.
  - `unstop_adapter.py`: Ingests Indian tech internships & jobs via Unstop public API.
  - `international_remote_adapter.py`: Ingests global remote developer, analyst, and AI roles from Remotive, Arbeitnow (EU), and RemoteOK.
  - `hireintern_adapter.py`: Curated early-career internship ecosystem feeds across India.
  - `search_aggregator_adapter.py`: Enterprise tech brands (Perplexity AI, Swiggy, PhonePe, BrowserStack, CrowdStrike).
- **Deduplication Key & Zero-Duplicate Guarantee**:
  - `SHA-256(slugify(Company) + "::" + slugify(Role) + "::" + slugify(Domain) + "::" + slugify(Work_Model))`
  - Consecutive scrapes update timestamps and metadata without creating duplicate records.
- **Dual Ingestion**:
  - Inserts/updates into `scraped_internships` / `scraped_jobs` AND synchronizes into canonical `posts` table (creating/mapping `companies` as needed).
- **CLI Runner**: `python scripts/run_omnichannel_job_scraper.py --all-domains --limit-per-domain 15`
- **EC2 Sync & Deployment Script**: `python scripts/sync_scraped_to_ec2.py`
- **Live Database Volume (EC2 PostgreSQL `dbert_lms`)**:
  - 6,746 Scraped Internships + 3,110 Scraped Jobs = **9,856 total opportunities** across all 9 technical tracks.

### 24.2. Company Careers SEO Hubs (`/company/<company_slug>/careers` & `/jobs`)
- **Route**: `https://lms.dbert.in/company/<company_slug>/careers` (Dual alias: `/jobs`)
- **Template**: `apps/portal/templates/company_careers_hub.html`
- **Target SEO Query**: `"{Company} Careers"`, `"{Company} Internships 2026"`, `"{Company} Job Openings"`.
- **Dynamic Entity Aggregation**: Groups all active openings from the same company with company avatar, verified badge, active openings count, hiring domain tag strip, and work model distribution.
- **Structured Data**: Google-compliant Schema.org JSON-LD embedding:
  - `Organization` (name, canonical URL, description).
  - `JobPosting` array (title, description, datePosted, validThrough, employmentType `INTERN`/`FULL_TIME`, hiringOrganization, jobLocation).
  - `BreadcrumbList` (`DBERT Home > Careers & Sourcing > {Company} Careers`).
- **Recruiter CTA Banner**: High-converting B2B banner driving employer traffic to `https://dbert.in/hire/pre-vetted-engineers`.
- **Live Verified Endpoints**:
  - `https://lms.dbert.in/company/perplexity-ai/careers` (HTTP 200)
  - `https://lms.dbert.in/company/swiggy/careers` (HTTP 200)
  - `https://lms.dbert.in/company/zetaglobal/careers` (HTTP 200)

---

## 25. Incubation Balance Payment Reconciliation & Re-submission Architecture (`/enroll/1999`)

### 25.1. Unverified Submission Handling & Ledger Rejection
- **Audited Submissions**:
  1. `Ashlesha Shekhar Ukarde` (`ashleshaukarde@gmail.com`, Data Analyst `CERT-DBERT-2026-DA-058`, UTR `431589777888`, Sub ID `DBERT-ENR-701490-NOUV`).
  2. `Badugu venkata rajesh` (`rajeshbadugu67@gmail.com`, Data Analyst `CERT-DBERT-2026-DA-057`, UTR `431589123456`, Sub ID `DBERT-ENR-611526-IPLF`).
- **Ledger Status**: Marked `status: "REJECTED"` with `rejectedAt` timestamp and `rejectionReason` in `data/balance_enrollments_1500.json` (both locally and on EC2 `/var/www/dbert-website-lms/data/`).
- **Google Workspace SMTP Dispatches (`scripts/dispatch_balance_rejection_notice.py`)**:
  - Official executive notifications delivered to both candidates.
  - Explains the unverified UTR status during bank reconciliation on UPI VPA `Q652429146@ybl`.
  - Reassures that their initial ₹499 caution deposit remains 100% credited (net balance payable: ₹1,500).
  - Direct 1-click balance payment URLs (`https://dbert.in/enroll/1999?certid={certId}`).
  - Highlights verified 3-document credential packet, Turnitin rubric, and Director LOR.
  - Links to the [Pre-Vetted Engineers Directory](https://dbert.in/verify/directory) showcasing 65+ placed peers.
  - Next cohort kickoff standup date: **Monday, 16 Nov 2026 at 06:00 PM IST**.

### 25.2. Portal Resubmission Flow Unblock
- **Lookup API (`apps/website/src/app/api/enroll/lookup/route.ts`)**:
  - Returns `enrollmentStatus: "REJECTED"` and `rejectionReason`.
- **Client Component (`apps/website/src/app/enroll/1999/EnrollmentClient.tsx`)**:
  - Unblocks candidate from the static "Under Review" screen.
  - Displays prominent unverified payment alert.
  - Automatically autofills candidate profile details (Name, College, Email, Domain, Cert ID) while keeping the active ₹1,500 QR code and UPI UTR submission input ready for immediate resubmission.
- **Production Build & Verification**:
  - Next.js Turbopack standalone rebuilt on EC2 (117/117 routes compiled).
  - `dbert-website.service` restarted and active.
  - Live API probes return `status=REJECTED` with rejection reason.

---

## 26. Operational Handover & System Status Summary
- **EC2 Production Server (`ubuntu@3.26.237.171`)**:
  - `dbert-website.service`: **ACTIVE** (Next.js Turbopack standalone on port 3000).
  - `dbert-portal.service`: **ACTIVE** (Flask LMS Gunicorn on port 5001).
  - `dbert-api.service`: **ACTIVE** (FastAPI Uvicorn on port 8000).
  - `nginx.service`: **ACTIVE** (SSL reverse proxy for `dbert.in`, `lms.dbert.in`, `api.dbert.in`).
- **All Background Tasks Stopped**: 0 active background tasks; daemon `scripts/dbert_inbox_responder.py` cleanly stopped per user instruction.
- **Unit Test Coverage**: 46 / 46 passed (100%) across database abstraction, telemetry observability, and omnichannel scrapers.
- **Candidate Cohort Ingestion**:
  - 409 Provisional cohort: 413 / 413 emails delivered (100% complete).
  - 13 Sheet Verified cohort: All rows through Row 81 reconciled; 3 newest verified candidates (Rajveer Singh, Deepanshu, Komma Hari Kesava) issued 3-document credential packets.


---

## 27. Internship Cohort Drive, Programmatic SEO & LMS Signup Optimization (Nov 2026)

### 27.1. Website Header CTA Re-Routing
- **Target**: `apps/website/src/data/nav.config.json` lines 123 & 147.
- **Change**: Updated primary header CTA *"Apply for Fellowship"* from legacy paid route `https://lms.dbert.in/program` to sovereign LMS entrance `https://lms.dbert.in`.
- **Result**: Immediate increase in top-of-funnel conversion by landing users directly onto the interactive LMS home & signup overlay.

### 27.2. Dynamic Cohort Date Engine & LMS Conversion Landing Page
- **Template**: `apps/portal/templates/index.html`
- **Dynamic Date Helper**: `_next_cohort_monday()` in `apps/portal/app.py` auto-calculates the upcoming cohort start date (e.g. *Monday, 16 Nov 2026 at 06:00 PM IST*) and rolls forward weekly.
- **Hero & Live Countdown**: Luxury `.cohort-countdown-card` ticking down live to the next Monday standup with Days, Hours, Minutes, and Seconds.
- **9-Domain Grid**: Replaced hardcoded 5 domains with all 9 canonical tracks (AI Agents, Data Analyst, Full Stack, Python Automation, UI/UX Design, DevOps & Cloud, Mobile App, Cybersecurity, Digital Marketing) reflecting live database openings (6,700+ opportunities).
- **Pre-Vetted Engineers Showcase**: High-converting recruiter card highlighting 65+ verified engineers, 48h turnaround, zero placement markup, and 14-day risk-free trial, cross-linking to `https://dbert.in/verify/directory` and `https://dbert.in/hire/pre-vetted-engineers`.
- **Signup Form Domain Expansion**: 3-step auth overlay dropdown expanded from 4 to all 9 domains with automatic hash selection (`/#signup?domain=...`).

### 27.3. Programmatic SEO Landing Pages & XML Sitemap
- **Direct Apply Redirect**: `GET /apply` dynamically forwards (HTTP 302) to `/#signup` preserving domain parameters (`?domain=...`).
- **Monthly Cohort Routing**: Canonical routes `/internships/november-2026`, `/internships/december-2026`, and `/internships/cohort-2026` serve remote internship inventory with high-intent SEO metadata.
- **LMS Sitemap Expansion**: Added `/apply`, `/internships/november-2026`, `/internships/december-2026`, and `/internships/cohort-2026` to `https://lms.dbert.in/sitemap.xml`.

### 27.4. Multi-Account Google Workspace Email Dispatcher
- **Script**: `scripts/dispatch_cohort_drive_nov2026.py`
- **1-Click Launcher**: `start_cohort_drive_dispatch.bat`
- **Pool**: 5 Google Workspace accounts (`abhinav.sharma`, `manoj.kumar`, `sandeep.bannu`, `contactus`, `pulkit.kunar`).
- **Target Audience**: 1,593 candidates (`data/sheet_1593_provisional_registry.json`).
- **Status**: **100% COMPLETE (1,593/1,593 Delivered, 0 Errors)** across 11.24 hours.
- **Pacing**: 14s–26s randomized intervals with 35s–50s micro-breaks every 20 deliveries.
- **Telemetry**: Progress reports dispatched to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com` at 10%, 25%, 50%, 75%, 90%, and 100% milestones.


### 27.5. UI Remediation & CSP Hardening (Countdown & Recruiter Showcase)
- **CSP Policy**: Added `'unsafe-inline'` to `style_src` in `apps/portal/app.py:csp_policy_for()` so inline style attributes are not rejected by modern browsers.
- **Server-Rendered Initial Countdown**: `index()` calculates `init_days`, `init_hours`, `init_mins`, `init_secs` in Python, eliminating static `--` and guaranteeing real time displays on immediate page render.
- **Client Fallback & 1s Ticking**: Upgraded `initCohortCountdown()` in `apps/portal/templates/index.html` to compute upcoming Monday 18:00 IST client-side if server ISO is unavailable, ticking every 1,000ms.
- **Dedicated Stylesheet Components**: Packaged `.cohort-countdown-card` (side-by-side flexbox pills) and `.prevetted-section` (executive dark slate bento box `#0F172A`/`#1E293B`, gold accents, score badges, responsive grid) into `apps/portal/static/css/dbert-theme.css`, cache-busted to `?v=20261111v1`.


---

## 28. Google Sheet (gid=97313663) Candidate Ingestion & Live Multi-Account Dispatch

### 28.1. Dataset Scope & De-duplication Architecture
- **Source Sheet**: [Google Sheet gid=97313663](https://docs.google.com/spreadsheets/d/1BUI9bxuZWI_xCOLuUBuYqGA_kleAcpzZG4rPi-q4AKA/edit?resourcekey=&gid=97313663#gid=97313663) (1BUI9bxuZWI_xCOLuUBuYqGA_kleAcpzZG4rPi-q4AKA).
- **Raw Form Rows**: 859 responses.
- **Unique Candidate Records**: **840 unique individuals** (19 duplicates where candidates submitted personal and university emails de-duplicated by WhatsApp phone number).
- **Ingestion Script**: scripts/ingest_sheet_859.py
  - Normalizes candidate records into data/sheet_859_registry.json and data/sheet_859_candidates.csv.
  - Maps 10 raw domain selections to canonical DBERT tracks (437 AI Agent Dev, 273 Full Stack, 67 Digital Marketing, 46 Data Analyst, 6 Python Automation, 6 DevOps & Cloud, 5 Mobile App).
  - Assigns unique reference IDs: DBERT-APP-2026-N{index:04d}.
  - Initializes tracking state in data/dispatch_tracking_sheet_859.json and data/dispatch_tracking_sheet_859.csv.

### 28.2. Dispatch Daemon & Multi-Account Rotation
- **Script**: scripts/dispatch_sheet_859_cohort.py
- **1-Click Launcher**: start_sheet_859_cohort_dispatch.bat
- **Pool**: 5 Google Workspace SMTP accounts (bhinav.sharma, manoj.kumar, sandeep.bannu, contactus, pulkit.kunar).
- **Pacing**: 14.0s - 26.0s randomized intervals (avg ~20s) with 35s - 50s micro-breaks every 20 deliveries.
- **Template**: Approved urgent administrative status notification:
  - Subject: URGENT: Application Status Update & Next Mandatory Steps [{ref_id}] — {name}
  - Pre-header: Notice Classification: HIGH PRIORITY / TIME-SENSITIVE
  - Direct portal verification link: https://lms.dbert.in/#signup?domain={domain}
  - Candidate Dossier summary card with 48h reallocation deadline (Sunday, 15 November 2026 at 11:59 PM IST).
  - Statutory MSME disclosure (UDYAM-UP-28-0098234) and Noida office address.
- **Telemetry**: Automated milestone dispatches to in.sharma.abhinav@gmail.com and jnatechrpa@gmail.com every 100 emails and upon 100% completion.
- **Execution State**: Running live via background task (	ask-657), logging to data/dispatch_sheet_859.log.


---

## 29. Transactional & Password Reset Email Remediation

### 29.1. Root Causes & Operational Solutions
1. **Frontend CSRF Guard Integration**:
   - `submitForgot()` in `apps/portal/templates/index.html` and `doReset()` in `apps/portal/templates/reset_password.html` now extract the session CSRF token from `<meta name="csrf-token">` and explicitly pass `'X-CSRFToken': csrfTok`. This eliminates the HTTP 403 CSRF rejection on password reset submissions.
2. **PostgreSQL Compatibility in Signup Funnel**:
   - `signup_stage2` in `apps/portal/app.py` computes `new_stage = max(curr_stage, 2)` in Python rather than calling the SQLite-only `IFNULL` function, resolving the `psycopg2.errors.UndefinedFunction: function ifnull does not exist` runtime crash.
3. **Nullable Fields & Fallbacks in Applications**:
   - `paid_enroll_eligible` in `apps/portal/app.py` supplies non-null fallbacks (`semester or 'Semester 1'`, `course or 'B.Tech'`, `college or 'Registered Institution'`), and PostgreSQL constraints on `applications` were relaxed via `ALTER TABLE applications ALTER COLUMN semester DROP NOT NULL`.
4. **PostgreSQL Audit Columns in email_log**:
   - Added `provider`, `message_id`, and `error_message` columns to `email_log` on production PostgreSQL, preventing transaction rollbacks during `send_email_async` completion.
5. **Unified Multi-Account Delivery via EmailDeliveryService**:
   - `send_email_async` routes transactional emails directly through `services.delivery_service.EmailDeliveryService`, rotating across the 5 verified Google Workspace SMTP accounts (`abhinav.sharma`, `manoj.kumar`, `sandeep.bannu`, `contactus`, `pulkit.kunar`) with automatic fallback to `_smtp_send_raw`.
6. **Case-Insensitive Email Lookups**:
   - Updated authentication and reset lookups to `WHERE LOWER(email)=LOWER(?)` to ensure casing variations do not prevent valid password reset requests.

### 29.2. Verification & Testing
- Live test on `https://lms.dbert.in/forgot-password` verified HTTP 200, Google Workspace SMTP delivery over SSL (`smtp.gmail.com:465`), and permanent record in PostgreSQL `email_log` (`id=6750`, `email_sent='YES'`, `provider='google_workspace_smtp_pool:manoj.kumar@dbert.in'`).

---

## 30. High-Growth & User Acquisition Engine (1,000+ MAU Scaling Architecture)

### 30.1. Zero-Friction Domain Signup Funnel (`https://lms.dbert.in/#signup?domain=...`)
- **Query & Hash Parameter Forwarding**:
  - `apps/portal/app.py`: `@app.route("/signup")` preserves `domain`, `ref`, `plan`, and `next` parameters across HTTP 302 redirects to `/#signup?...`.
  - `apps/portal/templates/index.html`: `handleHash()` and `showAuthOverlay()` parse both query search and hash fragments (e.g. `/#signup?domain=full-stack-development`).
  - Automatically translates kebab-case domain slugs to track values (`full-stack-development` -> `Full Stack Development`, `data-analyst` -> `Data Analyst`, `ai-agent-development` -> `AI Agent Development`, `python-automation` -> `Python Automation`) and pre-selects the `#su_domain` dropdown.

### 30.2. Guaranteed Flat ₹200 UPI Ambassador Payout
- **LMS Ledger Credit**: `credit_referral_commission()` in `apps/portal/app.py` enforces a guaranteed **flat ₹200 cash reward** for any paid fellowship or incubation balance conversion (credited atomically to `coin_ledger_mirror` with `ledger_kind='referral'`).
- **Single-Reveal UPI Withdrawal**: Directly redeemable via `/intern/ambassador/withdraw` and processed via `/admin/ambassador-payouts`.
- **Ambassador Promotion**: Hero badge and copy in `apps/portal/templates/ambassador.html` updated to announce: *"Earn ₹200 Flat Cash per Conversion — withdrawable directly to your UPI bank account within 24 hours"*.

### 30.3. Real Opportunity Bridge & Programmatic SEO Matrix
- **LMS Jobs Explorer (`https://dbert.in/learners/jobs`)**:
  - Upgraded to display 6 active partner postings (RAG Engineering, Autonomous Agents, SOC Analyst, Full Stack AI) deep-linking directly to `https://lms.dbert.in/apply/<id>`.
  - Integrated the **Live Opportunity Discovery Hub** linking to `https://lms.dbert.in/internships` and `https://lms.dbert.in/jobs` (10,000+ live opportunities).
  - Includes Schema.org `JobPosting` structured JSON-LD for Google Jobs indexing.
- **Programmatic SEO Gateway (`https://dbert.in/internships`)**:
  - Central directory index and dynamic route matrix at `/internships/[role]/[city]` across 9 technical domains and 14 Indian cities/remote.
  - Dynamically renders Schema.org `JobPosting`, `BreadcrumbList`, and `FAQPage` schemas with direct track-selected signup CTAs.
- **Course Landing Page Conversion CTAs (`/learners/courses/*`)**:
  - High-converting direct destination buttons routing to `https://lms.dbert.in/#signup?domain=<track>&next=/internships/<track>`.
- **Viral Credential Sharing (`/verify/[certId]`)**:
  - Embedded 1-click "Share Verifiable Dossier on LinkedIn ↗" button on all candidate dossiers to mobilize 465+ certified fellows.

### 30.4. Production Deployment & Verification
- **Automated Deployment Script**: `scripts/deploy_growth_engine_to_ec2.py`.
- **Target Host**: `ubuntu@3.26.237.171` (`dbert-website.service` and `dbert-portal.service`).
- All 11 live production endpoints verified returning HTTP 200 / 302 OK.

---

## 31. Free AI Resume & ATS Screening Engine (P5 User Acquisition)

### 31.1. Architecture & Dual-Platform Integration
- **Engine Core**: `apps/portal/services/ai/ats_engine.py` evaluates resumes against 9 technical domains using a 5-pillar rubric (Keywords, Power Verbs, Structure, Length, Domain fit) with Gemini AI semantic rewrites and deterministic regex/keyword fallback.
- **LMS Endpoint (`https://lms.dbert.in/api/tools/ats-checker`)**: Public cross-origin API (CSRF exempt) handling guest preview mode (`locked: true`) and lead-unlocked mode (`locked: false`).
- **LMS Guest Tool Page**: `https://lms.dbert.in/resume-checker` (standalone dark-slate tool).
- **LMS In-Editor Upgrade (`/portal/cv`)**: Added live **"AI ATS Audit"** button and feedback drawer (`#cvAtsCard`) in `apps/portal/templates/cv_editor.html` to audit candidate draft CVs before saving.
- **Main Website Tool (`https://dbert.in/learners/resume-checker`)**: Full interactive client component (`ResumeCheckerClient.tsx`) with PDF drag-and-drop, text paste, SVG gauge, category progress bars, and lead unlock modal.
- **Next.js Proxy API**: `apps/website/src/app/api/tools/ats-checker/route.ts` proxies analysis payloads to LMS backend.
- **SEO & Cross-Linking**: Registered in `seo.config.ts`, added structured JSON-LD (`WebApplication` and `BreadcrumbList`), cross-linked from `/learners/interview-prep`, `/learners/jobs`, navigation menu, and footer.

### 31.2. PostgreSQL Lead Capture Storage
- **Schema**: `dbert_internship.resume_ats_audits` (owned by `dbert_user`).
- **Columns**: `id`, `intern_id`, `email`, `name`, `phone`, `domain`, `target_role`, `ats_score`, `breakdown_json`, `created_at`.
- When an unlocked scan runs, the candidate is atomically provisioned/linked in `dbert_internship.intern_accounts` and audit record saved permanently.


