# DBERT Engineering & Agent Brain (AGENTS.md)
================================================================================
Universal Context, Architectural Rules, and Operational Playbook for Antigravity & AI Agents
================================================================================

---

## 1. Domain Authority & SEO Mandate (CRITICAL)
- **Active Sovereign Domain**: `https://dbert.in`
- **Legacy Retired Domain**: `dbert.online` (Redirects to `dbert.in`).
- **NEVER use `dbert.online`** as the active origin, baseUrl, canonical tag, or in any newly generated code, API endpoints, emails, certificate PDFs, or WhatsApp copy.
- **Dual SEO Headlines**: Maintain migration notice phrasing ("DBERT.online is now DBERT.in" / "dbert.online is not the active platform") across Header, Footer, About Credentials, Learners, and Verification pages.
- **Migration Page**: Dedicated landing page at `/dbert-online` with FAQPage and BreadcrumbList JSON-LD schemas.
- **Google Analytics 4 (GA4)**: Measurement ID is strictly `G-MN7ME9X518` across `apps/website`, `apps/portal`, and deployment templates.

---

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
   # Sync dynamically generated sitemap into static standalone public paths
   if [ -f .next/server/app/sitemap.xml.body ]; then
     cp .next/server/app/sitemap.xml.body public/sitemap.xml
   fi
   cp -r public .next/standalone/ 2>/dev/null || true
   cp -r public .next/standalone/apps/website/ 2>/dev/null || true
   if [ -f .next/server/app/sitemap.xml.body ]; then
     cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true
     cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true
   fi
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

---

## 4. Pre-Vetted Engineers Directory (`/verify/directory`)

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

---

## 5. ₹1,999 Enrollment & Balance Completion Portal (`/enroll/1999`)

### 5.1. Financial Ledger Breakdown
- **Total Program Fee**: ₹1,999
- **Caution Deposit Paid**: -₹499 (Credited in full)
- **Net Remaining Balance Payable**: **₹1,500**
- Prominent notice informs candidates that as they already paid the ₹499 caution deposit, they only need to complete the remaining ₹1,500 balance to finalize enrollment and unlock official credentials.

### 5.2. Candidate Autofill API (`GET /api/enroll/lookup`)
- Supports query parameters `?certid=` or `?email=` (e.g., `https://dbert.in/enroll/1999?certid=CERT-DBERT-2026-DA-057`).
- Queries the candidate database and auto-populates Full Name, Email, WhatsApp Phone, College, Domain Track, and Certificate ID.

### 5.3. Payment & Submission Engine
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

---

## 6. WhatsApp Dual-Account Dispatch System

### 6.1. Architectural Constraints
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

---

## 7. Key CLI Commands Reference

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

---

## 8. Historical Batch Ingestion & Dispatch Campaign Registry

### 8.1. Master Historical Campaign Matrix
The following table documents completed and ongoing programmatic batch dispatches, data reconciliations, and candidate cohort ingestions across DBERT platforms.

| Campaign / Batch Identifier | Source Reference | Candidate Volume | Deliverables & Artifacts | Primary Dispatch Script | State & Tracking Files |
|---|---|:---:|---|---|---|
| **409 Provisional Batch** | Oct 2026 Provisional Cohort | 409 candidates | DNS pre-flight audit (SPF/DKIM/DMARC), 30s rate pacing, milestone telemetry to admins | `scripts/dispatch_409_provisional.py` | `data/dispatch_tracking_409.json`, `data/all_409_provisional_registry.json` |
| **9 Verified Candidates Upgrade** | Google Sheet `gid=1265293201` (Rows 57–65) | 9 candidates (7 upgraded, 2 new) | ₹299 fee verified, official 3-doc PDF credential packets generated, preview PNGs deployed | `scripts/dispatch_9_verified_certificates.py` | `data/dispatch_tracking_9_verified.json`, `outputs/cohort_2026/` |
| **Approved Incubation (Bhargavi Poola)** | ₹1,500 Balance Completion (`DBERT-ENR-703685-TYN6`) | 1 candidate | Marked `APPROVED` in ledger; live real-time countdown to Nov 9, 2026 deployed on `/eroll` | N/A (Web UI & Lookup API) | `data/balance_enrollments_1500.json` |
| **Google SMTP Quota Watchdog** | Google Workspace Daily User Limit | Automation daemon | Cooldown probe (`smtp.gmail.com:465`) every 300s, automated exit code 55 circuit breaker, phased triggers | `scripts/quota_watchdog_and_dispatcher.py` | `data/quota_watchdog_state.json`, `data/quota_watchdog.log`, `start_quota_watchdog.bat` |
| **1,593 Sheet Provisional Ingestion** | Google Sheet `gid=338877142` | 1,593 candidates | Directory shield gate (never added to `directory_candidates.json`), `/verify/unlock` landing page | `scripts/dispatch_sheet_1593.py` | `data/sheet_1593_provisional_registry.json`, `data/sheet_1593_dispatch_tracking.json` |
| **Sheet gid=97313663 Ingestion** | Google Sheet `gid=97313663` | 859 raw -> 840 unique | 19 phone duplicates merged, normalized into 7 canonical tracks, multi-account rotation | `scripts/ingest_sheet_859.py` | `data/sheet_859_registry.json`, `data/dispatch_tracking_sheet_859.json` |
| **Stipend ₹299 WhatsApp Campaign** | LinkedIn Cohort pending ₹299 Gate | 41 candidates (40 sent, 1 auto-linked) | Sent via logged-in Account 2 with 18s–35s pacing; both URLs in first 15 lines; ₹499 caution deposit and ₹5,000 stipend withholding warning | `scripts/dispatch_stipend_custom_whatsapp.py` | `data/whatsapp_stipend_299_pending.json`, `data/dispatch_tracking_stipend_299.csv` |
| **4 Verified Candidates Upgrade (Nov 19, 2026)** | Website ₹299 Gateway (Shrey Patel, Kethavath Sruthi) & Google Sheet `gid=1265293201` Rows 89–90 (Bhavya Balchandani, Tehreem Fatima) | 4 candidates (3 upgraded, 1 new) | ₹299 fee verified, official 3-doc PDF credential packets generated, preview PNGs deployed, synced to PostgreSQL `intern_certificates` with `tier='verified'` | `scripts/issue_4_verified_certificates.py`, `scripts/deploy_4_verified_certificates_to_ec2.py` | `data/verification_submissions_299.json`, `apps/website/src/data/certificates_registry.json`, `apps/website/src/data/directory_candidates.json` |
| **43 Expiring Posts Renewal (Nov 20, 2026)** | Posts expiring <= 2026-11-27 (IDs 24–33, 37–51, 55–69, 73–75) | 43 internship posts | Extended `apply_by` to 2027-01-15 and `expires_at` to 2027-02-15; refreshed SEO-rich 2026/2027 titles; standardized DBERT Incubation `/enroll/1999` pathway; synced to `https://lms.dbert.in/sitemap.xml` with lastmod `2026-11-20` | `scripts/renew_43_expiring_posts.py` | `data/expiring_43_posts.json` |

### 8.2. Operational Protocols & Safety Governance
1. **409 Provisional Batch Delivery Rules**:
   - Google Workspace SMTP (`smtp.gmail.com:465`) authenticated as `abhinav.sharma@dbert.in`.
   - Strict 30s delays between dispatches; automated telemetry dispatched every 100 deliveries to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.
2. **Verified Candidates Upgrade Rules**:
   - Reconciles ₹299 payments from Google Drive proofs; updates `certificates_registry.json` to `status: "VERIFIED"`, `isProvisional: false`.
   - Generates full 3-document PDF packets (Certificate, Academic Evaluation, LOR) and generates preview PNGs at `apps/website/public/certificates/previews/{certId}.png`.
3. **Directory Shield Gate (Sheet 1,593 & Sheet 859)**:
   - Candidates from external bulk sheets are strictly excluded from `/verify/directory` until individual ₹299 project evaluation or ₹1,500 incubation fee is verified.
   - Dynamic lookup via `/api/enroll/lookup` safely resolves them with `isProvisional: true`.

---

## 9. Persistent Documentation Directory
- Comprehensive architectural records and changelogs:
  - [`ARCHITECTURE_ROADMAP.md`](file:///c:/Users/user/Desktop/dbert-website-lms/ARCHITECTURE_ROADMAP.md)
  - [`DOMAIN_MIGRATION_AND_GA4_CHANGELOG.md`](file:///c:/Users/user/Desktop/dbert-website-lms/DOMAIN_MIGRATION_AND_GA4_CHANGELOG.md)
  - [`new_certifications_reconciliation_and_dispatch_plan.md`](file:///C:/Users/user/.gemini/antigravity/brain/542c2e0b-55d0-41c9-9b46-721bf0724211/new_certifications_reconciliation_and_dispatch_plan.md)
  - [`enrollment_1999_deployment_walkthrough.md`](file:///C:/Users/user/.gemini/antigravity/brain/542c2e0b-55d0-41c9-9b46-721bf0724211/enrollment_1999_deployment_walkthrough.md)
  - [`intern_directory_alphabetical_verification_plan.md`](file:///C:/Users/user/.gemini/antigravity/brain/542c2e0b-55d0-41c9-9b46-721bf0724211/intern_directory_alphabetical_verification_plan.md)

---

---

## 10. Stipend Contribution & Verification Gating System (`/stipend/tasks`)

### 10.1. Business Rules & 3-Step Eligibility Checklist
- **Strict Verification Gate**: Stipend eligibility and technical contribution submission are **strictly restricted to candidates with VERIFIED credentials** (`status: "VERIFIED"`, `verified: true`, `isProvisional: false`).
- **Completion Date Gate**: Interns can only apply for stipend **on or after their official completion date** (`joining_date + 60 days` from LMS enrollment, fallback to certificate `endDate`). Before this date, an informative countdown timer is displayed.
- **Payout Setup Requirement**: Intern must configure and verify their Fernet-encrypted UPI ID on their profile before submitting their contribution dossier.
- **Provisional Candidates Locked View**: Candidates with provisional status (`isProvisional: true`) see a locked stipend dashboard:
  - Prominent alert: *"Verification Required: Your certificate is currently Provisional"*.
  - Action CTA button: *"Complete Verification to Unlock Stipend"* deep-linking to `https://dbert.in/enroll/1999?email={email}` (or `/eroll?email=...`).
  - No access to submit contributions until verified.
- **LMS Authentication & Tracking**: Interns must authenticate at LMS portal (`https://lms.dbert.in`). All milestone submissions, AI reviews, and payout disbursements are tracked within their individual student profile. Seamless onboarding allows verified certified candidates without an LMS account to activate with 1-click password setup.

### 10.2. Technical Contribution, AI Pre-Screening & 5,000 Coins Payout Engine
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

---

## 11. Unified 3-Document Certificate Generation & Executive Print Dossier (`/portal/certificate/<cert_id>/print`)

### 11.1. Visual & Structural Parity Mandate
- **Exact Email Parity**: Web-rendered printable certificates on `/portal/certificate/<cert_id>/print` must match the official 3-document credential packet sent via authenticated Google Workspace SMTP:
  1. **Document 1 (Certificate of Completion)**: 640 × 495 Landscape canvas with `targets12.png` luxury slate artwork, gold hairline rules, Palatino/Georgia typography, Mr. Abhinav Sharma's signature, and verification QR code.
  2. **Document 2 (Academic Project Evaluation)**: US Letter Portrait with double navy/gold border, 9-dimension rubric table, 100-mark scoring (`score/100`), Turnitin originality validation seal, and signatory sign-off.
  3. **Document 3 (Letter of Recommendation)**: US Letter Portrait with official letterhead, ref `LOR-DBERT-{certId}`, 4-paragraph technical endorsement, and executive signature.
- **Engine**: Encapsulated in `apps/portal/services/certificate_packet_service.py` using ReportLab and PyMuPDF (`fitz`).
- **Dynamic Master PDF Generation**: Merges all 3 documents into a single 3-page vector master PDF (`/portal/certificate/<cert_id>/pdf`).
- **Individual Downloads**: Dedicated routes for standalone documents (`/portal/certificate/<cert_id>/download/1`, `/2`, `/3`) and high-res previews (`/portal/certificate/<cert_id>/preview/1`, `/2`, `/3`).
- **Executive Dossier UI**: `apps/portal/templates/certificate_dossier.html` provides interactive tab switching between all 3 documents, 1-click "Print Master PDF", standalone download dropdown, and deep-link to public verification (`https://dbert.in/verify?certid={cert_id}`).

### 11.2. Global LMS Navigation Bar & Responsive Routing
- **LMS Integration Mandate**: The printable credential dossier (`/portal/certificate/<cert_id>/print`) is an integral LMS portal feature (`lms.dbert.in`), not an external static website page.
- **Top Navigation Bar (`.lms-navbar`)**: Positioned sticky at the top (`z-index: 60`), providing direct navigation across LMS routes:
  - Home (`/`), My Portal (`/portal`), Courses (`/courses`), Sprint Tasks (`/tasks`), Stipend Milestone (`/stipend/tasks`), 1:1 Mentorship (`/mentors/slots`), and Placements & Jobs (`/jobs`).
  - Mobile responsive drawer with burger menu toggle (`#lmsMenuBtn`, `#lmsMobileMenu`).
  - Sub-header (`.dossier-header`) and tab switcher (`.dossier-tabs`) smoothly stack below the LMS navbar.
- **Strict Print Isolation**: `@media print` cleanly suppresses both `.lms-navbar` and `.dossier-header` to output unblemished, full-page credential certificates.

### 11.3. Document Security & Right-Click Prevention
- **Anti-Tampering & Asset Integrity**: Right-click context menus (`contextmenu` event) and drag-and-drop (`dragstart` event) are strictly intercepted and prevented across all document stages, preview canvases, and cards (`.dossier-stage`, `.doc-card`, `.doc-frame`, `.doc-frame img`).
- **CSS Anti-Selection**: `user-select: none; -webkit-user-drag: none;` applied to all rendered credential previews.
- **Interactive Security Toast (`#protectionToast`)**: When right-click or `Ctrl+S` is attempted on the document view, an executive floating security badge informs the user that official credentials are protected and directs them to use the authorized Master PDF / Print buttons.

---

---

## 12. Group Mentorship Sessions & Cascading Calendar Booking System (`/mentors/slots`)

### 12.1. Cascading 3-Step Booking Engine (`session_booking.html`)
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

### 12.2. Group Capacity & Concurrency Protection
- **Capacity**: Sessions support **up to 30 interns simultaneously** (`capacity INTEGER DEFAULT 30`, `seats_booked INTEGER DEFAULT 0`).
- **Compound Uniqueness**: `UNIQUE(slot_id, intern_id)` on `mentor_session_bookings` prevents duplicate reservations while enabling cohort scalability.
- **Atomic Reservation (PAY-001 / RAC-002)**: Check-and-increment transaction prevents race conditions and ensures total bookings never exceed slot capacity under concurrent load.

### 12.3. Mentor Faculty Console (`/staff/mentor-slots`)
- **Session Publisher**: Mentors set start/end times within 14:00 – 20:15 IST, domain track, topic agenda, and capacity up to 30.
- **Live Roster**: Mentors can view all registered interns (Name, Email, Booked timestamp) for each of their scheduled sessions.
- **CSRF Protection**: `bookSlot()` incorporates `X-CSRF-Token` header to ensure seamless, error-free booking transactions.

---

---

## 13. College Ambassador & Referral Subsystem (`/ambassador`, `/intern/ambassador`)

### 13.1. Defect Remediation & Security Hardening
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

### 13.2. Referral Attribution, Wallet & Payout Engine
- **Anonymous Tracking**: Referral clicks via `/r/click?ref=<code>` tracked without session dependencies.
- **Attribution & Anti-Fraud**: `attach_referral_on_signup` safely binds new students to their referrer; blocks self-referrals and duplicate attributions.
- **10% Commission Calculation**: When an attributed student enrolls (e.g., ₹1,999), 10% (₹200) is atomically credited to the ambassador's withdrawable wallet (`coin_ledger_mirror` with `ledger_kind='referral'`).
- **Fernet Encrypted UPI ID**: Payout destinations stored with Fernet symmetric encryption; only revealed to authorized administrators during single-reveal payout processing with full audit logging.
- **Double-Spend & Overdraw Prevention**: Validates withdrawal amounts against available balance; enforces atomic ledger debits upon admin execution at `/admin/ambassador-payouts`.
- **E2E Test Suite**: Verified via `scripts/test_ambassador_e2e.py` covering all 10 lifecycle stages with 100% pass rate.

---

---

## 14. Sovereign REST API Developer Platform & Instructions Hub (`https://api.dbert.in`)

### 14.1. Public Developer Hub & Onboarding Landing Page (`GET /`, `/instructions`)
- **Sovereign Domain**: `https://api.dbert.in` (FastAPI Uvicorn running on port 8000 reverse-proxied through Nginx with HTTP/2 and TLS 1.3).
- **Interactive Developer Portal**: Replaces former 404 response on `/` with a comprehensive, responsive, executive developer portal:
  - **4-Step Quickstart Instructions**: Base URL setup (`https://api.dbert.in/api/v1`), JWT Bearer Token acquisition (`/api/v1/auth/*`), header specification (`Authorization: Bearer <token>`), and idempotent JSON response handling.
  - **Multi-Language Interactive Code Snippets**: Tabbed copy-paste examples in cURL, Python (requests/httpx), JavaScript (fetch), and Node.js (axios).
  - **Core Architectural Modules**: Deep-dive summaries for 15 domains including Credentials Verification, Job Marketplace (6,600+ vetted openings), Application State Machine, Courses & AI Guided Tutor, Ambassador Referrals, and Payments.
  - **Interactive Searchable Endpoint Catalog**: Table covering primary production endpoints with HTTP method pills (`GET`, `POST`, `PUT`, `DELETE`), authorization level, description, and direct links to test within Swagger UI.
  - **Direct Documentation Launchers**: One-click links to Swagger UI (`/docs`), ReDoc (`/redoc`), OpenAPI 3.1 JSON (`/openapi.json`), and Liveness Probes (`/health`, `/ready`, `/status`).

### 14.2. Dual Content Negotiation & Machine Discovery (`/`, `/api`, `/api/v1`)
- **JSON Negotiation**: If client header includes `Accept: application/json` or query param `?format=json`, `/` returns a structured JSON API Manifest instead of HTML, allowing CLIs, SDKs, and automated agents to discover capabilities instantly.
- **API Version Discovery**: Dedicated routes `GET /api` and `GET /api/v1` provide machine-readable discovery indices of all available routes and modules.
- **OpenAPI Schema Metadata**: Enhanced `FastAPI` instance configuration with server endpoints (`https://api.dbert.in`, `http://127.0.0.1:8000`), detailed markdown description, and support contact coordinates (`engineering@dbert.in`).

---

---

## 15. Multi-Sector Domain Architecture (9 Core Technical & Growth Domains)

### 15.1. Scope & 9 Standardized Career Tracks
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

### 15.2. Database Segregation & Automated Seeding
- **Active Posts Table**: Segregated in PostgreSQL (`dbert_internship.posts`) on EC2 (`3.26.237.171`) and local SQLite (`internship.db`).
- **Post Distribution**: Minimum 5-16 verified internships and 2-3 jobs per domain (111 active published postings total).
- **Migration Script**: `scripts/migrate_and_seed_9_domains.py` supports dual modes:
  ```powershell
  # Local SQLite migration
  python scripts/migrate_and_seed_9_domains.py --sqlite apps/portal/internship.db

  # Production EC2 PostgreSQL migration
  python scripts/migrate_and_seed_9_domains.py --pg-url "postgresql://dbert_user:...@localhost:5432/dbert_lms" --schema "dbert_internship"
  ```

### 15.3. Cross-Service Domain Integration
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

---

## 16. Institutional Trust, Program Transparency & Credibility Standards
================================================================================

### 16.1. Canonical Terminology & Program Durations
1. **Single Unified Incubation Duration**: All cohort references, course schema JSON-LD, FAQs, and marketing copy strictly use **2 Months (8 Weeks)** (`P2M` / `P60D`). Legacy mentions of "three months" are completely retired.
2. **Guaranteed Placement Disambiguation**:
   - DBERT strictly guarantees **Active Production Codebase Assignment** under senior engineer code review, 1-on-1 technical mentorship, and an independently verifiable 3-document credential packet.
   - DBERT **does not claim or guarantee unconditional permanent corporate employment**. Unconditional job guarantees are misleading and prohibited across all copy.
3. **Zero Application Fee Guarantee**: DBERT never charges application, registration, screening, or interview fees. Initial selection is 100% merit-based.

### 16.2. Performance Stipend Governance & Audited Rubrics
- Stipends (₹5,000–₹18,000) are performance-based and earned against delivery milestones submitted through the LMS task portal (`/stipend/tasks`).
- Evaluated against 4 objective engineering dimensions:
  1. *Code Quality & Cleanliness*: Linting (PEP8/ESLint), typing, modular separation, error boundaries.
  2. *Architecture & Security*: Database migrations, parameterization, zero hardcoded secrets.
  3. *Practical Feasibility & Testing*: Unit/integration tests, live deployability.
  4. *Technical Documentation*: Comprehensive READMEs, architecture decision records.
- Approved disbursements are released atomically via UPI directly to the fellow's verified account.

### 16.3. Statutory Disclosure & Entity Clarification
- **Parent Legal Enterprise**: *Digital Blinc Education Research And Technology* (MSME / UDYAM compliant).
- **Official Government Verification**: Direct link to `https://udyamregistration.gov.in/Udyam_Verify.aspx`.
- **Statutory Distinction**: MSME registration establishes formal legal entity compliance under Indian law; it does not replace UGC/AICTE degree accreditation. DBERT credentials represent audited production software engineering evidence.
- **Entity Advisory**: Zero affiliation with discontinued third-party operations or unofficial recruitment agencies soliciting fees under similar legacy names.

### 16.4. Published Metrics Hierarchy
To maintain mathematical consistency across all web portals:
- **1,500+ Evaluated Learners**: Developers and university students upskilled across open hackathons, masterclasses, and foundational assessments.
- **465+ Certified Fellows in Sovereign Directory**: Formally registered candidates with verifiable UUID credentials in our public [Alphabetical Credential Directory](https://dbert.in/verify/directory).
- **120+ Venture Incubation Fellows**: Selective cohorts deployed on live venture client repos and multi-agent systems.

---

---

## 17. Comprehensive 9-Domain SEO Architecture, Sitemaps & Cross-Domain Link Mesh

### 17.1. Architecture & Keyword Silos Across 9 Domains
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

### 17.2. Sitemaps Generation & Canonical Indexing
- **`https://dbert.in/sitemap.xml`**:
  - Dynamically generated from `apps/website/src/data/seo.config.ts`, `apps/website/src/lib/blog.ts`, and verified candidates in `certificates_registry.json`.
  - All 9 course tracks mapped at `/learners/courses/<domain>` with priority `0.9` and weekly change frequency.
  - Automatically synced to `public/sitemap.xml` and standalone build assets on EC2.
- **`https://lms.dbert.in/sitemap.xml`**:
  - Programmatically indexed across all 9 domains for category hubs (`/internships/<domain>`, `/jobs/<domain>`), work-from-home filters (`/internships/work-from-home/<domain>`), paid filters (`/internships/paid/<domain>`), remote filters (`/internships/remote/<domain>`), and programmatic city corridors (Bangalore, Pune, Delhi NCR, Hyderabad, Mumbai, Chennai, Remote).
  - Indexes all live direct company postings and active curated job/internship leads for Google Jobs search indexing.

### 17.3. Cross-Domain Footers & Structured Data Parity
- **Website Global Footer (`Footer.tsx`)**:
  - Multi-column layout featuring all 9 domain course paths under **AI Academy** and deep linking to live sourced opportunities on `lms.dbert.in` (`/internships/remote/<domain>`, `/internships/virtual-remote-internships`, `/internships/paid-internships`, `/jobs`).
  - Trust & Verification column cross-linking to `/verify`, `/verify/directory`, and `/enroll/1999`.
- **LMS Global Footer (`_footer_seo.html`)**:
  - Standardized across `post_listings.html`, `post_detail.html`, `scraped_internship_detail.html`, and `index.html`.
  - Responsive 4-column link mesh (AI & Engineering, Data/Design/Growth, Sourced Hubs & Modes, Verification & Studio) targeting high-intent long-tail keywords.
- **Google `JobPosting` Structured Data (`index.html`)**:
  - Full schema JSON-LD covering all 9 technical domains with realistic compensation ranges (₹5,000–₹18,000/month), direct apply links, and telecommute indicators.


---

---

## 18. DBERT Platform Evolution Roadmap Execution & Production Baseline (Phases 0–9)

### 18.1. Phase 0: Baseline Discovery & Audit Artifacts
All canonical system audit deliverables specified in `DBERT_PLATFORM_EVOLUTION_ROADMAP.md` are established in `docs/dbert-roadmap/audit/` and deployed to EC2:
1. **Repository Map (`docs/dbert-roadmap/audit/repository-map.md`)**: Complete infrastructure mapping (Next.js 16 on port 3000, Flask LMS on port 5001, FastAPI on port 8000, Nginx reverse proxy, PostgreSQL 15, and SQLite fallbacks).
2. **Route Inventory (`docs/dbert-roadmap/audit/route-inventory.csv`)**: 533 total cataloged endpoints across `dbert.in`, `lms.dbert.in`, and `api.dbert.in` with handler files and auth requirements.
3. **Data Model Map (`docs/dbert-roadmap/audit/data-model-map.md`)**: Entity-relationship mapping of PostgreSQL tables (`users`, `companies`, `posts`, `scraped_internships`, `intern_applications`, `tasks`, `task_submissions`, `intern_certificates`, `coin_ledger_mirror`), Prisma schemas, and JSON registries.
4. **Integration Map (`docs/dbert-roadmap/audit/integration-map.md`)**: Configuration details, protocols, credentials, rate limits, and circuit breakers for Google Workspace SMTP, GA4 (`G-MN7ME9X518`), WhatsApp Playwright dual-engine, Google Gemini 2.5 AI, Razorpay/UPI (`Q652429146@ybl`), and AWS EC2.
5. **Test Baseline (`docs/dbert-roadmap/audit/test-baseline.md`)**: Automated test suites in `apps/portal/tests/` (12/12 pytest passed), `dbert-api-package/tests/` (remediation security suite), and Next.js static route audits.
6. **Current Public Claims Audit (`docs/dbert-roadmap/audit/current-public-claims.md`)**: Programmatic validation of public claims (₹1,999 program fee with ₹499 caution deposit credit = ₹1,500 net balance; 60-day sprint duration; 65 verified vs 400 provisional candidates; MSME accreditation disclaimer; active Alkame open-source repo).
7. **Risks and Unknowns Log (`docs/dbert-roadmap/audit/risks-and-unknowns.md`)**: Operational mitigations for Google Workspace SMTP 24h rolling quotas, candidate privacy-by-default, and Next.js standalone build symlinks.

### 18.2. Phase 1: Programme Truth & Financial Ledger Alignment
- **Single Source of Truth**:
  - `https://dbert.in/terms` and `https://dbert.in/refund` aligned with `https://lms.dbert.in/terms` and `https://lms.dbert.in/program`.
  - Free Internship Track: Zero application/screening fee; 100% refundable security deposit returned upon milestone completion.
  - Incubation Program: ₹1,999 total committed seat fee (or ₹1,500 balance payable if ₹499 caution deposit was credited).
  - Performance Stipend: ₹5,000–₹18,000 milestone-based, governed by Turnitin/rubrics, submitted via `/stipend/tasks` and approved by senior staff.

### 18.3. Phase 2: Marketplace Sourcing Integrity & Database Type Safety
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

### 18.4. Phases 3–9: End-to-End Operational Continuity & Deployment
- **Pre-Vetted Directory**: Verified candidates surfaced first by hireability rank (98, 97, 96...) at `/verify/directory`, linked from `/hire/pre-vetted-engineers` with dual CTAs (`View Proof Dossier` & `Connect on LMS`).
- **Cryptographic Verification**: Exact-ID lookups on `dbert.in/verify/[certId]` rendering official 3-document credential packets.
- **Production Build & Verification**: Next.js Turbopack standalone successfully rebuilt on EC2, public assets synced, `/data` symlinks preserved, and systemd units (`dbert-website.service`, `dbert-portal.service`) running active (HTTP 200 on all endpoints).

---

---

## 19. Pre-Vetted Engineers Directory, Add-On SEO & Omnichannel Sitemaps Architecture

### 19.1. Strict Add-On Mandate & Zero-Disruption Policy
- **Additive SEO Principle**: All enhancements are strictly additive ("Add-On" only). 100% of pre-existing SEO keywords (`DBERT candidate directory`, `verify DBERT certificate`, MSME statutory disclosures, course hubs), candidate records, routes, and rankings are fully preserved.
- **Dual-Audience Intent**: The candidate directory (`/verify/directory`) serves a dual audience:
  1. **Candidate Verification**: Students and institutions verifying certificate authenticity and academic rubrics.
  2. **B2B Engineering Recruitment**: Startups and enterprise hiring managers looking to onboard pre-vetted AI, Full Stack, and Data engineers with verified Turnitin scores and live GitHub pull requests.

### 19.2. Pre-Vetted Directory Structured Data & Rich Snippets (`/verify/directory`)
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

### 19.3. SEO Bounds Enforcement (`apps/website/src/data/seo.config.ts`)
- **Rule Verification (`npm run check:seo`)**:
  - Validates all 75 routed pages against strict character constraints: `title <= 52` characters, `description >= 140 && description <= 155` characters.
  - Resolved 6 length bounds violations (`/learners/launchpad`, `/learners/courses/ui-ux-design`, `/learners/courses/devops-cloud`, `/learners/courses/mobile-app-development`, `/learners/courses/digital-marketing`, and `/verify/directory`).
  - Result: **75 entries checked against 75 routed pages, 0 errors, 100% pass rate**.

### 19.4. Omnichannel Sitemaps Architecture & Search Engine Discovery
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

### 19.5. Internal Link Equity & Cross-Domain Navigation Web
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

---

## 20. Pre-Vetted Domain Directories & Recruiter Skills Filtering Architecture

### 20.1. Specialized Domain Sub-Pages (`/verify/directory/[domainSlug]`)
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

### 20.2. Interactive Recruiter Skills & Multi-Select Filter Engine
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

### 20.3. Structured Data (JSON-LD) & Domain SEO
- **Domain-Tailored Tri-Schema JSON-LD**:
  1. **`ItemList` Schema**: Formats candidates strictly within that domain as structured `Person` entities with evaluation scores and proof URLs.
  2. **`BreadcrumbList` Schema**: Declares hierarchy (`Home` -> `Pre-Vetted Directory` -> `[Domain Name] Engineers`).
  3. **`FAQPage` Schema**: 4 domain-tailored technical screening Q&As per page addressing framework competency, git review standards, 48h turnaround, and 14-day risk-free trial.
- **Sitemap Priority & Daily Frequency**:
  - All 7 domain directory URLs registered in `https://dbert.in/sitemap.xml` with **Priority 0.90** and **daily** change frequency.

### 20.4. Internal Link Equity Web
- **Header Mega-Menu** (`apps/website/src/data/nav.config.json`): Direct link to Pre-Vetted Engineers Directory under `For Startups` -> `Resources`.
- **Website Footer** (`apps/website/src/components/layout/Footer.tsx`): Links to Full Stack, AI & ML, and Data Analytics directories under `Startups & Equity`.
- **LMS Footer** (`apps/portal/templates/_footer_seo.html`): Cross-links to domain talent directories under Column 4 (Trust & Verification).
- **Directory Cross-Links Grid**: Bottom grid on all directory pages rendering cards to all sibling domain rosters.


---

---

## 21. LMS Symmetrical Pagination (18/page), Executive Bento Footer & Pre-Vetted Engineer Proof Dossier (`/verify/[certId]`)

### 21.1. LMS Listings Symmetrical Layout (`_PAGE_SIZE = 18`)
- **Route Scope**: `https://lms.dbert.in/internships` and `https://lms.dbert.in/jobs`.
- **Symmetry Mandate**: 
  - Sliced in `apps/portal/app.py` at `_PAGE_SIZE = 18` (formerly 21).
  - Perfectly matches the standard 3-column responsive desktop layout (6 rows × 3 cards = exactly 18 cards per page) without any dangling or ragged cards.
  - Slices across all 6,700+ internships and 320+ pages seamlessly.

### 21.2. Full-Width Breakout of Tech Track & Hub Matrix (`seo-silo-matrix`)
- **Template Restructuring (`apps/portal/templates/post_listings.html`)**:
  - Moved `<section class="seo-silo-matrix">` completely outside of `.listings-body-grid` (which was trapped inside the right content column alongside the sticky left sidebar).
  - Positioned inside `.listings-page-wrap` immediately below `.listings-pagination-bar`.
  - Spans 100% full container width, effectively occupying both sidebar and content width for maximum visual weight and crawlability.
  - Features 3 high-intent categories:
    1. *Specialized Tracks*: AI Agent Development, Full Stack Development, Data Analyst, Python Automation.
    2. *Top Tech Hubs*: Bangalore (Bengaluru), Pune, Hyderabad, Delhi NCR / Noida.
    3. *High-Intent Searches*: Remote AI Agent, WFH Data Analyst, Paid AI with Stipend, Paid Full Stack.

### 21.3. Executive Silo Matrix UI & UX Architecture for Footer (`_footer_seo.html`)
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

### 21.4. Pre-Vetted Engineer Proof Dossier & Profile Architecture (`/verify/[certId]`)
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

---

## 22. Omnichannel Job & Internship Sourcing Engine & SEO Hubs

### 22.1. Core Architecture & Exact 9 Technical Domains
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

### 22.2. Company Careers SEO Hubs (`/company/<company_slug>/careers` & `/jobs`)
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

---

## 23. Incubation Balance Payment Reconciliation & Re-submission Architecture (`/enroll/1999`)

### 23.1. Unverified Submission Handling & Ledger Rejection
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

### 23.2. Portal Resubmission Flow Unblock
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

---

## 24. Operational Handover & System Status Summary
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

---

## 25. Internship Cohort Drive, Programmatic SEO & LMS Signup Optimization (Nov 2026)

### 25.1. Website Header CTA Re-Routing
- **Target**: `apps/website/src/data/nav.config.json` lines 123 & 147.
- **Change**: Updated primary header CTA *"Apply for Fellowship"* from legacy paid route `https://lms.dbert.in/program` to sovereign LMS entrance `https://lms.dbert.in`.
- **Result**: Immediate increase in top-of-funnel conversion by landing users directly onto the interactive LMS home & signup overlay.

### 25.2. Dynamic Cohort Date Engine & LMS Conversion Landing Page
- **Template**: `apps/portal/templates/index.html`
- **Dynamic Date Helper**: `_next_cohort_monday()` in `apps/portal/app.py` auto-calculates the upcoming cohort start date (e.g. *Monday, 16 Nov 2026 at 06:00 PM IST*) and rolls forward weekly.
- **Hero & Live Countdown**: Luxury `.cohort-countdown-card` ticking down live to the next Monday standup with Days, Hours, Minutes, and Seconds.
- **9-Domain Grid**: Replaced hardcoded 5 domains with all 9 canonical tracks (AI Agents, Data Analyst, Full Stack, Python Automation, UI/UX Design, DevOps & Cloud, Mobile App, Cybersecurity, Digital Marketing) reflecting live database openings (6,700+ opportunities).
- **Pre-Vetted Engineers Showcase**: High-converting recruiter card highlighting 65+ verified engineers, 48h turnaround, zero placement markup, and 14-day risk-free trial, cross-linking to `https://dbert.in/verify/directory` and `https://dbert.in/hire/pre-vetted-engineers`.
- **Signup Form Domain Expansion**: 3-step auth overlay dropdown expanded from 4 to all 9 domains with automatic hash selection (`/#signup?domain=...`).

### 25.3. Programmatic SEO Landing Pages & XML Sitemap
- **Direct Apply Redirect**: `GET /apply` dynamically forwards (HTTP 302) to `/#signup` preserving domain parameters (`?domain=...`).
- **Monthly Cohort Routing**: Canonical routes `/internships/november-2026`, `/internships/december-2026`, and `/internships/cohort-2026` serve remote internship inventory with high-intent SEO metadata.
- **LMS Sitemap Expansion**: Added `/apply`, `/internships/november-2026`, `/internships/december-2026`, and `/internships/cohort-2026` to `https://lms.dbert.in/sitemap.xml`.

### 25.4. Multi-Account Google Workspace Email Dispatcher
- **Script**: `scripts/dispatch_cohort_drive_nov2026.py`
- **1-Click Launcher**: `start_cohort_drive_dispatch.bat`
- **Pool**: 5 Google Workspace accounts (`abhinav.sharma`, `manoj.kumar`, `sandeep.bannu`, `contactus`, `pulkit.kunar`).
- **Target Audience**: 1,593 candidates (`data/sheet_1593_provisional_registry.json`).
- **Status**: **100% COMPLETE (1,593/1,593 Delivered, 0 Errors)** across 11.24 hours.
- **Pacing**: 14s–26s randomized intervals with 35s–50s micro-breaks every 20 deliveries.
- **Telemetry**: Progress reports dispatched to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com` at 10%, 25%, 50%, 75%, 90%, and 100% milestones.


### 25.5. UI Remediation & CSP Hardening (Countdown & Recruiter Showcase)
- **CSP Policy**: Added `'unsafe-inline'` to `style_src` in `apps/portal/app.py:csp_policy_for()` so inline style attributes are not rejected by modern browsers.
- **Server-Rendered Initial Countdown**: `index()` calculates `init_days`, `init_hours`, `init_mins`, `init_secs` in Python, eliminating static `--` and guaranteeing real time displays on immediate page render.
- **Client Fallback & 1s Ticking**: Upgraded `initCohortCountdown()` in `apps/portal/templates/index.html` to compute upcoming Monday 18:00 IST client-side if server ISO is unavailable, ticking every 1,000ms.
- **Dedicated Stylesheet Components**: Packaged `.cohort-countdown-card` (side-by-side flexbox pills) and `.prevetted-section` (executive dark slate bento box `#0F172A`/`#1E293B`, gold accents, score badges, responsive grid) into `apps/portal/static/css/dbert-theme.css`, cache-busted to `?v=20261111v1`.


---

---

## 26. Transactional & Password Reset Email Remediation

### 26.1. Root Causes & Operational Solutions
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

### 26.2. Verification & Testing
- Live test on `https://lms.dbert.in/forgot-password` verified HTTP 200, Google Workspace SMTP delivery over SSL (`smtp.gmail.com:465`), and permanent record in PostgreSQL `email_log` (`id=6750`, `email_sent='YES'`, `provider='google_workspace_smtp_pool:manoj.kumar@dbert.in'`).

---

---

## 27. High-Growth & User Acquisition Engine (1,000+ MAU Scaling Architecture)

### 27.1. Zero-Friction Domain Signup Funnel (`https://lms.dbert.in/#signup?domain=...`)
- **Query & Hash Parameter Forwarding**:
  - `apps/portal/app.py`: `@app.route("/signup")` preserves `domain`, `ref`, `plan`, and `next` parameters across HTTP 302 redirects to `/#signup?...`.
  - `apps/portal/templates/index.html`: `handleHash()` and `showAuthOverlay()` parse both query search and hash fragments (e.g. `/#signup?domain=full-stack-development`).
  - Automatically translates kebab-case domain slugs to track values (`full-stack-development` -> `Full Stack Development`, `data-analyst` -> `Data Analyst`, `ai-agent-development` -> `AI Agent Development`, `python-automation` -> `Python Automation`) and pre-selects the `#su_domain` dropdown.

### 27.2. Guaranteed Flat ₹200 UPI Ambassador Payout
- **LMS Ledger Credit**: `credit_referral_commission()` in `apps/portal/app.py` enforces a guaranteed **flat ₹200 cash reward** for any paid fellowship or incubation balance conversion (credited atomically to `coin_ledger_mirror` with `ledger_kind='referral'`).
- **Single-Reveal UPI Withdrawal**: Directly redeemable via `/intern/ambassador/withdraw` and processed via `/admin/ambassador-payouts`.
- **Ambassador Promotion**: Hero badge and copy in `apps/portal/templates/ambassador.html` updated to announce: *"Earn ₹200 Flat Cash per Conversion — withdrawable directly to your UPI bank account within 24 hours"*.

### 27.3. Real Opportunity Bridge & Programmatic SEO Matrix
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

### 27.4. Production Deployment & Verification
- **Automated Deployment Script**: `scripts/deploy_growth_engine_to_ec2.py`.
- **Target Host**: `ubuntu@3.26.237.171` (`dbert-website.service` and `dbert-portal.service`).
- All 11 live production endpoints verified returning HTTP 200 / 302 OK.

---

---

## 28. Free AI Resume & ATS Screening Engine (P5 User Acquisition)

### 28.1. Architecture & Dual-Platform Integration
- **Engine Core**: `apps/portal/services/ai/ats_engine.py` evaluates resumes against 9 technical domains using a 5-pillar rubric (Keywords, Power Verbs, Structure, Length, Domain fit) with Gemini AI semantic rewrites and deterministic regex/keyword fallback.
- **LMS Endpoint (`https://lms.dbert.in/api/tools/ats-checker`)**: Public cross-origin API (CSRF exempt) handling guest preview mode (`locked: true`) and lead-unlocked mode (`locked: false`).
- **LMS Guest Tool Page**: `https://lms.dbert.in/resume-checker` (standalone dark-slate tool).
- **LMS In-Editor Upgrade (`/portal/cv`)**: Added live **"AI ATS Audit"** button and feedback drawer (`#cvAtsCard`) in `apps/portal/templates/cv_editor.html` to audit candidate draft CVs before saving.
- **Main Website Tool (`https://dbert.in/learners/resume-checker`)**: Full interactive client component (`ResumeCheckerClient.tsx`) with PDF drag-and-drop, text paste, SVG gauge, category progress bars, and lead unlock modal.
- **Next.js Proxy API**: `apps/website/src/app/api/tools/ats-checker/route.ts` proxies analysis payloads to LMS backend.
- **SEO & Cross-Linking**: Registered in `seo.config.ts`, added structured JSON-LD (`WebApplication` and `BreadcrumbList`), cross-linked from `/learners/interview-prep`, `/learners/jobs`, navigation menu, and footer.

### 28.2. PostgreSQL Lead Capture Storage
- **Schema**: `dbert_internship.resume_ats_audits` (owned by `dbert_user`).
- **Columns**: `id`, `intern_id`, `email`, `name`, `phone`, `domain`, `target_role`, `ats_score`, `breakdown_json`, `created_at`.
- When an unlocked scan runs, the candidate is atomically provisioned/linked in `dbert_internship.intern_accounts` and audit record saved permanently.




---

---

## 29. Repository Hygiene, Tri-Target File Inventory & Pristine Layout

### 29.1. Pristine Root Mandate
The repository root contains strictly 4 required files:
- `README.md`: Ecosystem architecture and quickstart guide.
- `AGENTS.md`: Universal architectural brain and playbook for all AI agents.
- `GEMINI.md`: Mirror of AGENTS.md for Gemini agents.
- `.gitignore`: Production-grade exclusions (excluding databases, archives, temp screenshots, and vendor folders).

All other loose files previously in root have been organized or purged:
- **Windows Batch Files**: Moved to `scripts/bat/` (paths updated to run seamlessly from repo root).
- **Candidate CSV Datasets**: Moved to `data/sources/` (safely ignored by Git).
- **Presentations & Slide Decks**: Moved to `docs/presentations/`.
- **Sample Certificates & Assets**: Moved to `docs/samples/`.
- **External QA / Audit Reports**: Moved to `docs/reports/` and `docs/audit/`.
- **Obsolete Scratch DBs & ZIPs**: Deleted (`internship.db`, `target_test.db`, `dbert-api-package-v1.zip`, `DBERT_Fieldwork_UI_UX_Agent_Handoff.zip`, etc.).

### 29.2. Curated Production Scripts (`scripts/`)
From 510 legacy scripts, **483 ad-hoc one-off inspection, probe, and patch scripts** were safely archived and removed. Exactly **35 Canonical Production Scripts** are actively maintained:
1. **EC2 Deployment Automation (10)**: `deploy_website_updates_to_ec2.py`, `deploy_enrollment_1999_to_ec2.py`, `deploy_directory_to_ec2.py`, `deploy_new_certificates_to_ec2.py`, `deploy_stipend_system_to_ec2.py`, `deploy_bhargavi_approval_to_ec2.py`, `deploy_footer_and_verify_notice.py`, `deploy_sitemap_and_jobs_to_ec2.py`, `full_production_deployment.py`, `fast_sync_to_ec2.py`.
2. **Delivery Daemons & Candidate Dispatchers (6)**: `dispatch_409_provisional.py`, `dispatch_9_verified_certificates.py`, `dispatch_cohort_drive_nov2026.py`, `dispatch_sheet_1593.py`, `dispatch_sheet_859_cohort.py`, `quota_watchdog_and_dispatcher.py`, `dbert_inbox_responder.py`.
3. **WhatsApp Automation Suite (5)**: `send_dbert_whatsapp.py`, `verify_and_launch_dbert_whatsapp.py`, `send_ambassador_whatsapp.py`, `send_rejected_payments_whatsapp.py`, `verify_and_launch_16nov_whatsapp.py`.
4. **Registry & Certificate Generation (4)**: `generate_provisional_registry.py`, `issue_9_verified_certificates.py`, `generate_all_packets.py`, `generate_sample_packet.py`.
5. **Database Migration, Seeding & Scraping (6)**: `sync_verified_certificates_to_portal.py`, `migrate_stipend_schema_and_tasks.py`, `migrate_mentor_group_capacity.py`, `seed_mentor_slots.py`, `run_omnichannel_job_scraper.py`, `scripts/scrapers/` (All 6 core scraping adapters).
6. **Live Production Health & Verification (5)**: `verify_production_live.py`, `verify_admin_routes_live.py`, `verify_stipend_flow_e2e.py`, `verify_ec2_deployment.py`, `production_preflight.sh`.

### 29.3. Pre-Deletion Safety Backups
- **Local Archive**: `archive/pre_cleanup_backup_20261113.zip` (**220 MB**, 6,388 archived files).
- **EC2 Production Backup**: `/home/ubuntu/pre_cleanup_ec2_20261113.tar.gz` (**180 MB**).

---

---

## 30. Intern Lifecycle, Payment Blocking Analysis & 4-Gate Stipend Architecture

### 30.1. The 5-Stage Candidate Lifecycle & Payment Gating
The LMS platform enforces a strict 5-stage lifecycle state machine in `apps/portal/app.py` (`get_intern_flow_state()`):

```mermaid
stateDiagram-v2
    [*] --> Stage1_Applied: Candidate registers & submits profile
    Stage1_Applied --> Stage2_UnderReview: Application submitted
    Stage2_UnderReview --> Stage3_Selected: Admin approval (or Auto-Selection Bridge)
    Stage3_Selected --> Stage4_PaymentPending: Candidate selects joining Monday & uploads ₹499 receipt / UTR
    Stage4_PaymentPending --> Stage5_Confirmed: Admin verifies transaction (or Auto-Verify via Razorpay/UTR API)
    Stage5_Confirmed --> [*]: Full Access, Course Auto-Enrolled, Certificate Unlocked
```

#### Why Interns Are "Unable to Complete ₹499 Payments" (Root Cause Analysis):
1. **The Silent Fail / Gate Block**:
   - When a candidate signs up and submits their profile, their record in the `applications` table is created with `status = 'Under Review'`.
   - In `app.py:get_intern_flow_state()`:
     ```python
     # Stage 3: Selected (Admin Approved Application -> Deposit Required)
     is_selected = bool(app_row and app_row["status"] in (STATUS_SELECTED, STATUS_ENROLLMENT_PENDING))
     ```
   - If `is_selected` is False (which it is for all candidates in Stage 2 `UNDER_REVIEW`), `can_upload_payment` is set to `False`.
   - In `apps/portal/templates/portal.html`, the entire payment interface (`#ovSelected`, payment QR code, 1-tap UPI buttons, and receipt upload input) is wrapped in `<div class="glass-card hidden" id="ovSelected">`.
   - It is only rendered if `_status === 'Selected' || _status === 'Enrollment Pending'`.
2. **The Operational Disconnect**:
   - Outreach campaigns (WhatsApp & Email) invite candidates to "Confirm your enrollment & deposit".
   - Candidates click the login link and arrive on `/portal`.
   - They see: *"Application Under Review by Mentors"* with a disabled state.
   - There is NO payment CTA, NO QR code, and NO submit button visible!
   - Unless an admin manually logs into `/admin` and transitions the candidate from `UNDER_REVIEW` to `SELECTED`, or a script runs `promote_*_selected.py`, candidates are completely blocked from completing their payments!

### 30.2. The 4-Gate Stipend Release Funnel (`/stipend/tasks`)
Stipend claims (worth ₹5,000 / 5,000 coins withdrawable via UPI) are gated behind 4 strict sequential gates in `apps/portal/routes/stipend.py`:

```mermaid
flowchart LR
    G1["Gate 1:<br/>Verified Certificate<br/>(isProvisional: false)"] --> G2["Gate 2:<br/>60-Day Maturity<br/>(today >= joining + 60d)"]
    G2 --> G3["Gate 3:<br/>Encrypted UPI Setup<br/>(Profile UPI Verified)"]
    G3 --> G4["Gate 4:<br/>Capstone Deliverable<br/>(GitHub + Live Demo + Report)"]
    G4 --> Release["Staff Approval &<br/>₹5,000 UPI Release"]
```

#### Why Interns Are "Unable to Complete Stipend Release Forms" (Root Cause Analysis):
1. **Gate 1 Block (Provisional Status)**:
   - `CertificateService.is_intern_verified()` checks if `status == 'VERIFIED'` and `isProvisional == false`.
   - 400 out of 465 candidates hold provisional certificates (`isProvisional: true`).
   - For all provisional candidates, Gate 1 fails immediately, locking the submission form and displaying a red banner: *"Verification Required: Your certificate is currently Provisional"*.
2. **Gate 2 Block (Maturity Date Countdown)**:
   - `CertificateService.get_intern_completion_info()` enforces that interns must serve their full 60-day tenure (`today >= joining_date + 60 days`).
   - For candidates who joined recently (e.g. October or November 2026 cohorts), their 60-day date is in December 2026 or January 2027.
   - The form displays a real-time countdown clock and disables the submission button until the maturity date is reached.
3. **Gate 3 Block (UPI Missing)**:
   - The intern must configure their encrypted UPI ID on `/profile` before submitting.
4. **Lack of In-App Guidance & Feedback**:
   - The stipend dashboard does not currently show an interactive 4-step checklist on the main `/portal` page, so candidates do not realize which exact gate is pending until they discover `/stipend/tasks`.

---

---

## 31. Dual Sidebar Discrepancy & Unified Dashboard Redesign Blueprint

### 31.1. The Dual Sidebar Conflict
The LMS portal currently possesses two completely separate, conflicting sidebar implementations:

| Feature | Sidebar A: Legacy Monolith (`portal.html`) | Sidebar B: Responsive Shell (`_app_shell.html` / `_intern_sidebar.html`) |
| :--- | :--- | :--- |
| **Location** | Hardcoded in `apps/portal/templates/portal.html` (lines 25–59) | Shared partial in `apps/portal/templates/_intern_sidebar.html` |
| **Element ID** | `<aside class="sidebar" id="sidebar">` | `<aside class="sidebar" id="appSidebar">` |
| **Drawer Logic** | `toggleSidebar()` / `#scrim` | `toggleAppSidebar()` / `#appBurger` |
| **Navigation Model** | 18 SPA JavaScript tabs (`data-tab="overview"`, `learning`, `coins`, etc.) | Semantic categorized routes (`/courses`, `/stipend/tasks`, `/jobs`, etc.) |
| **Width & Spacing** | Variable CSS width | Fixed 240px clearance (`.has-sidebar`) |
| **Used On** | `/portal` only | All subpages (`/courses`, `/stipend/tasks`, `/tasks`, `/ambassador`, etc.) |

**User Experience Breakdown**:
When an intern is on `/portal`, they see Sidebar A. When they click "Micro-Tasks" (`/tasks`) or "Stipend Milestone" (`/stipend/tasks`), the page reloads with Sidebar B, which has different icons, different grouped headers, and different responsive behavior. Clicking back to `/portal` reverts to Sidebar A.

### 31.2. Unified Navigation & Dashboard Redesign Architecture
To resolve the discrepancy and modernize the intern experience:
1. **Unify under `_app_shell.html`**:
   - Remove the hardcoded `<aside id="sidebar">` from `portal.html`.
   - Standardize `portal.html` to use `{% include '_intern_sidebar.html' %}` with `.has-sidebar`.
2. **Harmonize the 4 Nav Groups**:
   - **Learn**: Learning Dashboard (`/portal`), Course Catalog (`/courses`), 1:1 Mentorship (`/mentors/slots`).
   - **Practice & Earn**: 4-Gate Stipend Milestone (`/stipend/tasks`), Sprint Tasks (`/tasks`), Coins Ledger (`/account/coins`), Ambassador Program (`/ambassador`).
   - **Career Outcomes**: Placements & Jobs (`/jobs`), Engineering Articles (`/intern/articles`), AI Resume & ATS Audit (`/learners/resume-checker`).
   - **Account**: AI Tutor Key (`/account/gemini-key`), Profile & UPI Settings (`/profile`), Logout.
3. **Dashboard Modernization (`portal.html`)**:
   - **Hero Progress Tracker**: Real-time 5-stage application status with instant 1-tap "Confirm Seat & Pay ₹499" action button.
   - **4-Gate Stipend Milestone Card**: Visual checklist (Gate 1: Credential, Gate 2: Tenure, Gate 3: UPI, Gate 4: Capstone) with progress percentage.
   - **Course Learning Progress Widget**: Dynamic progress bar showing enrolled modules, completed lessons, and next assignment.
   - **Fast Action Drawer**: Direct 1-click access to Book Mentor, View Tasks, and Withdraw Coins.

---

---

## 32. Google Search Console JobPosting Structured Data Remediation & Unified SEO Schema Service

### 32.1. Problem Diagnosis & Google Search Console Trigger
Google Search Console flagged 4 non-critical `JobPosting` structured data issues across `dbert.in` and `lms.dbert.in`:
1. `Missing field 'addressCountry' (in 'jobLocation.address')`
2. `Missing field 'streetAddress' (in 'jobLocation.address')`
3. `Missing field 'postalCode' (in 'jobLocation.address')`
4. `Missing field 'value' (in 'baseSalary.value')`

**Root Cause**: The site exposes `https://dbert.in/sitemap-lms.xml` (proxied to `lms.dbert.in/sitemap.xml`) indexing 10,393 scraped internship and job lead pages (`/internship/lead/<id>/<slug>` and `/job/lead/<id>/<slug>`). The template in `apps/portal/app.py` emitted incomplete `PostalAddress` objects (lacking country, street address, and PIN code) and passed textual descriptions into `baseSalary.value` instead of numeric values.

### 32.2. Architecture & Solution Principles
1. **Zero Sitemap Disturbance**:
   - Strictly preserved all 170 URLs in `apps/website/src/app/sitemap.ts` (`dbert.in/sitemap.xml`).
   - Strictly preserved all 10,393 URLs in `apps/portal/app.py` (`lms.dbert.in/sitemap.xml` / `dbert.in/sitemap-lms.xml`).
   - Corrected the JSON-LD schemas generated on the pages themselves.
2. **Unified SEO Schema Service (`apps/portal/services/seo_schema_service.py`)**:
   - `INDIAN_CITY_DIRECTORY`: Maps 30+ Indian tech hubs (Chennai, Bengaluru, Mumbai, Pune, Hyderabad, Delhi NCR, Gurgaon, Noida, etc.) to exact postal coordinates, street corridors, states, and PIN codes.
   - `get_postal_address_for_city(city, region)`: Generates complete Schema.org `PostalAddress` with `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`, and `addressCountry: "IN"`.
   - `parse_base_salary_schema(stipend_text)`: Automatically extracts numeric compensation into valid `MonetaryAmount` with `QuantitativeValue` (`value: int` or `minValue: int, maxValue: int`, and `unitText: "MONTH"` / `"YEAR"`). For undisclosed or performance-based stipends, `baseSalary` is cleanly omitted per Google Search Central specifications to prevent "Missing field value" warnings.
3. **Remote vs. Onsite Distinction**:
   - **Remote Roles**: Emits `jobLocationType: "TELECOMMUTE"` and `applicantLocationRequirements: {"@type": "Country", "name": "IN"}` with `jobLocation: null`.
   - **Onsite / Hybrid Roles**: Emits `jobLocation` containing complete 5-field `PostalAddress`.
4. **Cross-Service Coverage**:
   - Applied to dynamic lead details in `apps/portal/app.py`.
   - Applied to canonical post details (`_job_posting_jsonld`).
   - Applied to company careers hubs (`company_careers_hub`).
   - Applied to marketplace generator (`MarketplaceService.generate_google_jobs_json_ld`).
   - Applied to Next.js programmatic city pages in `apps/website/src/app/internships/[role]/[city]/page.tsx`.
   - Deployed and live validated on EC2 (`3.26.237.171`).

---

---

## 33. Autonomous Multi-Inbox Triage, Inquiry Classification, & Threaded Dispatch Engine

### 33.1. Operational Purpose & Mailbox Inventory
Autonomous triage and customer/candidate response system operating across active project inboxes.
- **Google Workspace Inboxes via IMAP (`imap.gmail.com:993`)**:
  - `abhinav.sharma@dbert.in`: Program Head & Project Mentor.
  - `manoj.kumar@dbert.in`: Academic Lead & Admissions.
  - `sandeep.bannu@dbert.in`: Technical Program Operations.
  - `contactus@dbert.in`: Admissions & Verification Concierge.
  - `pulkit.kunar@dbert.in`: Technical Mentorship & Verification.
- **Outlook Desktop MAPI Stores**:
  - `manpreet@vayanai.in.net`: Vayan AI / November interview inquiry store.
  - `contactus@gayatrieducation.info`, `support@...`, `connect@...`: Legacy credential packets and domain migration notices.

### 33.2. Dispatch Architecture (`scripts/dispatch_inbox_action_replies.py`)
- **Multi-Account SMTP Routing**: Sends directly from the authenticated Google Workspace account owning the thread or student relationship.
- **Thread Header Preservation**: Injects standard RFC 2822 `In-Reply-To` and `References` headers matching the candidate's existing conversation.
- **Deliverability-First Templates**: Single-card responsive HTML (max 600px width, `#0B0F17` background, `#141A23` inner card, `#E2B96F` gold typography, zero white-text contrast traps) paired with matching UTF-8 plain text and 1-tap WhatsApp concierge routing (`+91 81929 11360`).
- **Pacing & Safety Controls**: Strict 15-second rate-limiting between consecutive candidate deliveries.
- **Persistent State**: Full delivery audit logged to `data/inbox_action_dispatch.log` and idempotent state tracked in `data/inbox_action_dispatch_tracking.json`.

### 33.3. Executed Actions & Candidates Resolved (11/11 Dispatched)
1. **Suraj Upadhyay** (`surajup5756@gmail.com`): AI Agent Development portal login, direct activation link, and 16 Nov sprint orientation brief.
2. **Gundeti Vaishnavi** (`gundetivaishnavi634@gmail.com`): Full Stack Development ₹499 caution deposit clarification (100% credited/refundable) and 1-tap UPI details.
3. **C S Kavana** (`kavana200518@gmail.com`): SOC Analysis & Threat Defense 10h/wk flexible schedule, Wireshark/SIEM curriculum, and seat lock procedure.
4. **Chinnamgari Sumanjali** (`chinnamgarisumanjali13@gmail.com`): Remote Internship ₹499 caution deposit credit breakdown and WhatsApp verification.
5. **Nishant Makwane** (`nishantmakwane04@gmail.com`): Data Analyst Milestone form fix, providing native LMS submission portal (`/stipend/tasks`) and direct Google Form.
6. **Hariom Yadav** (`imhariom25@gmail.com`): Clarification that ₹299 is strictly optional for physical framed courier dispatch; standard academic evaluation and ₹5,000 stipend eligibility are 100% free.
7. **Prakash A** (`prakash.a2878@gmail.com`): AI & Machine Learning onboarding verification and Week 1 sprint task guidance.
8. **Astha Arya** (`asthaarya42@gmail.com`): Data Analytics onboarding server connectivity resolution and direct portal verification.
9. **Gurka Vinay Kumar Reddy** (`gurkavinay22@gmail.com`): Recorded UPI ID `9014147134@upi` into ledger, confirmed Capstone submission, and verified dossier `CERT-DBERT-2026-AIML-169`.
10. **Shanu Sri Gowtham** (`shanusrigowtham17@gmail.com`): Performance stipend milestone status explanation, 4-gate verification criteria, and `/stipend/tasks` portal.
11. **Rosmi Reji** (`rosmireji556@gmail.com`): Official LOR, background verification contacts (`admissions@dbert.in`), and employer cryptographic verification dossier `CERT-DBERT-2026-FSD-103`.
- **Administrative Telemetry**: Dispatched automated summary report to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.
---

---

## 34. Universal Autonomous Email Response Skills & Operational Playbook

### 34.1. Email Classification Taxonomy & Standard Business Policies
Every incoming student, intern, and client inquiry received across DBERT inboxes is classified into one of eight standardized operational scenarios. Future agents must execute the exact governing business policy, response structure, and action links detailed below:

| Inquiry Type | Typical Candidate Triggers | Governing Business Policy | Action & Response Strategy | Direct Action Links |
| :--- | :--- | :--- | :--- | :--- |
| **Type 1: ₹499 Seat Caution Deposit** | *"Why do I need to pay ₹499?", "Is ₹499 refundable?", "How to confirm seat?", "Payment receipt upload"* | **100% Credited / 100% Refundable**. Credited in full against the incubation program fee (net balance ₹1,500) or refunded upon milestone completion. Secures reserved cohort slot and provisions dedicated cloud compute sandbox. | Re-affirm selection, explain zero-loss credit/refund policy, provide UPI VPA, and offer instant WhatsApp receipt submission. | • UPI VPA: `Q652429146@ybl`<br/>• Portal: [`dbert.in/enroll/1999`](https://dbert.in/enroll/1999)<br/>• WhatsApp: [`+91 81929 11360`](https://wa.me/918192911360) |
| **Type 2: Milestone Fee Clarification (₹299 vs Free)** | *"I am unable to pay ₹299", "Do I need to pay for stipend?", "Is certificate free?", "Payment failed for certificate"* | **100% FREE Standard Evaluation**. Academic evaluation, LMS grading, cryptographic credential verification on `dbert.in/verify`, and ₹5,000 stipend eligibility are completely free. The ₹299 fee is strictly an optional courier and framing charge for physical hard-copy delivery. | Reassure candidate that zero payment is required for digital credentials or stipend eligibility. Provide direct digital verification link and LMS capstone submission portal. | • Verification: [`dbert.in/verify`](https://dbert.in/verify)<br/>• Tasks: [`lms.dbert.in/stipend/tasks`](https://lms.dbert.in/stipend/tasks) |
| **Type 3: Portal Login & Onboarding Server Errors** | *"Cannot log in", "Server error during onboarding", "Form response not recording", "Account locked"* | **Zero-Friction Candidate Access**. Automated activation fallback; self-healing direct portal access. Candidates must never be blocked by credential or CSRF glitches. | Provide direct links to LMS portal, registration bypass, and 1-click password reset with registered email. Offer instant manual activation via WhatsApp Concierge. | • Portal: [`lms.dbert.in/portal`](https://lms.dbert.in/portal)<br/>• Apply: [`lms.dbert.in/apply`](https://lms.dbert.in/apply)<br/>• Tasks: [`lms.dbert.in/stipend/tasks`](https://lms.dbert.in/stipend/tasks) |
| **Type 4: Performance Stipend Release (4-Gate Rule)** | *"Where is my stipend?", "When will I get paid?", "Stipend status update", "Completed tasks but no coins"* | **Strict 4-Gate Verification Rule**:<br/>1. **Verified Credential**: `status: "VERIFIED"`, `isProvisional: false`.<br/>2. **60-Day Maturity**: Intern completion date (`joining_date + 60 days`).<br/>3. **Encrypted UPI**: Verified VPA bound to profile.<br/>4. **Capstone Contribution**: Domain deliverables submitted on `/stipend/tasks` with AI rubric score and staff approval. | Detail the 4-gate status checklist, direct candidate to `/stipend/tasks` dashboard, explain 5,000 coins wallet credit, and provide Admissions helpline for expedited staff review. | • Tasks: [`lms.dbert.in/stipend/tasks`](https://lms.dbert.in/stipend/tasks)<br/>• Wallet: [`lms.dbert.in/intern/ambassador/withdraw`](https://lms.dbert.in/intern/ambassador/withdraw) |
| **Type 5: Payout Setup & UPI Submission** | *"My UPI ID is...", "Unable to add payout method on profile", "Update payment details"* | **Idempotent Financial Ledger Recording**. Candidate payment VPA is recorded directly into `intern_accounts.upi_id` and synced to `balance_enrollments_1500.json`. Duplicate submissions are rejected idempotently. | Record and validate 12-character VPA/UTR, confirm wallet binding, and notify candidate that disbursement will route directly to their confirmed VPA upon capstone sign-off. | • Profile: [`lms.dbert.in/intern/profile`](https://lms.dbert.in/intern/profile) |
| **Type 6: Official LOR & Employer Work References** | *"Need work reference for new job", "Employer background verification", "HR verification request", "LOR copy"* | **Institutional Verification Guarantee with 24h SLA**. Official employer background verification and signed Letter of Recommendation (LOR) from Program Head Mr. Abhinav Sharma. | Provide candidate's cryptographic proof dossier, official HR verification email, and mentor sign-off. | • Dossier: `https://dbert.in/verify?certid={certId}`<br/>• HR Email: `admissions@dbert.in`<br/>• Mentor: `abhinav.sharma@dbert.in` |
| **Type 7: Domain Migration & Brand Queries** | *"Verification page not opening on gayatrieducation.info", "dbert.online inquiry", "Is DBERT legitimate?"* | **Active Sovereign Domain Mandate**. All services, portals, and cryptographic registries operate strictly under `https://dbert.in`. Legacy domains `gayatrieducation.info` and `dbert.online` are fully retired/redirected. | Explain domain migration, provide direct link to active verification engine, and re-issue updated 3-document credential packet with active `dbert.in` seals. | • Migration Notice: [`dbert.in/dbert-online`](https://dbert.in/dbert-online)<br/>• Verification: [`dbert.in/verify`](https://dbert.in/verify) |
| **Type 8: Program Curriculum & Schedule Details** | *"What are the working hours?", "Is this compatible with college?", "Track syllabus", "Can I switch track?"* | **Flexible Asynchronous Execution**. 10 hours/week flexible, self-paced tasks designed specifically for university students, backed by weekend mentor code reviews. | Outline flexible format, practical GitHub deliverables, real-world tools (Wireshark, LangGraph, React, Power BI), and next cohort kickoff orientation details. | • Programs: [`dbert.in/programs`](https://dbert.in/programs)<br/>• LMS Portal: [`lms.dbert.in/portal`](https://lms.dbert.in/portal) |

---

### 34.2. Multi-Account Infrastructure & Routing Architecture
DBERT operates a multi-account outbound communication pool. Any agent executing dispatch must route replies through the exact authenticated sender matching the candidate's thread or institutional domain:

```mermaid
flowchart TD
    Inbound["Incoming Candidate Email"] --> IntentFilter{"Intent & Thread Analysis"}
    
    IntentFilter -->|"Program Head / Capstones / LOR"| Acc1["abhinav.sharma@dbert.in<br/>(Google Workspace SMTP:465)"]
    IntentFilter -->|"Admissions / Caution Deposit / ₹499"| Acc2["manoj.kumar@dbert.in<br/>(Google Workspace SMTP:465)"]
    IntentFilter -->|"Technical Ops / Onboarding / Sprints"| Acc3["sandeep.bannu@dbert.in<br/>(Google Workspace SMTP:465)"]
    IntentFilter -->|"Verification / General / Support"| Acc4["contactus@dbert.in<br/>(Google Workspace SMTP:465)"]
    IntentFilter -->|"Code Reviews / Rubric Scoring"| Acc5["pulkit.kunar@dbert.in<br/>(Google Workspace SMTP:465)"]
    IntentFilter -->|"Outlook Desktop Local MAPI"| MAPI["win32com.client<br/>(Account Matching & Sent Items Sync)"]
    
    Acc1 --> SMTPRelay["Authenticated SMTP Relay<br/>(RFC 2822 Threading + Pacing)"]
    Acc2 --> SMTPRelay
    Acc3 --> SMTPRelay
    Acc4 --> SMTPRelay
    Acc5 --> SMTPRelay
    
    SMTPRelay --> Candidate["Candidate Inbox<br/>(Single-Card HTML + Plain Text Alternative)"]
    MAPI --> Candidate
```

#### Multi-Account Credentials & Role Definitions:
- `abhinav.sharma@dbert.in` (App Password: `rsupmvvvvwrsuxuh`): Program Head & Project Mentor. Owns high-level academic evaluations, capstone technical reviews, official LORs, and executive escalations.
- `manoj.kumar@dbert.in` (App Password: `fnevtpseplwibckr`): Academic Lead & Admissions. Owns cohort selections, ₹499 caution deposit reconciliations, milestone evaluations, and initial onboarding.
- `sandeep.bannu@dbert.in` (App Password: `qtqzlmrynbcxvyjy`): Technical Program Operations. Owns developer workspace setups, server access, batch orientation schedules, and sprint tasks.
- `contactus@dbert.in` (App Password: `llvmaajmrljpcwru`): Admissions & Verification Concierge. Owns public verification queries, domain migration questions, and general student support.
- `pulkit.kunar@dbert.in` (App Password: `vzefecwpggxuaztr`): Technical Mentorship & Verification. Owns AI/ML and Data Analytics code reviews and submission rubrics.

#### Outlook Desktop Local MAPI Integration (`win32com.client`):
When dispatching from a Windows desktop session where local Outlook accounts are loaded:
```python
import win32com.client

outlook = win32com.client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")

def send_via_desktop_outlook(target_account_email, recipient, subject, html_body):
    account_to_use = None
    for acc in outlook.Session.Accounts:
        if acc.SmtpAddress.lower() == target_account_email.lower():
            account_to_use = acc
            break
    
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    mail.HTMLBody = html_body
    if account_to_use:
        mail.SendUsingAccount = account_to_use
    mail.Send()
```

---

### 34.3. RFC 2822 Deliverability & Design System
All automated email dispatches must strictly comply with deliverability best practices to guarantee inbox placement and zero white-text contrast traps:

1. **Thread Continuity & Header Alignment**:
   - `In-Reply-To` and `References` headers MUST be set to the inbound email's `Message-ID`.
   - Outbound `Message-ID` must be generated using `make_msgid(domain="dbert.in")`.
   - `Reply-To` MUST match the authenticated sender email exactly.

2. **Single-Card Responsive HTML Container**:
   - Centered container constrained to `max-width: 600px; margin: 0 auto;`.
   - Outer container background: `#0B0F17` (Luxury Deep Obsidian).
   - Inner card background: `#141A23` (Dark Navy Slate) with subtle border `1px solid #232D3F; border-radius: 8px;`.
   - Header accent: Top stripe `border-top: 4px solid #E2B96F;` (DBERT Gold).
   - Primary text: Clean, high-contrast `#E0E6ED` (Never `#ffffff` on white, preventing Outlook/Gmail dark mode inversion contrast traps).
   - Secondary text: `#94A3B8` (Muted Slate).
   - CTA buttons: Inline styled with high contrast (`background: #E2B96F; color: #0B0F17; font-weight: 700; text-decoration: none; padding: 12px 24px; border-radius: 6px; display: inline-block;`).

3. **Multipart UTF-8 Plain Text Parity**:
   - Every outbound MIME transmission MUST be `multipart/alternative`.
   - The `text/plain` part must be attached first, followed by `text/html`.
   - Plain text must contain identical actionable URLs and WhatsApp numbers to satisfy SpamAssassin / Barracuda anti-spam heuristics.

4. **Dual 1-Tap WhatsApp Concierge Footer**:
   - Every email footer must feature direct WhatsApp links to:
     - Admissions Concierge: `https://wa.me/918192911360` (`+91 81929 11360`)
     - Technical Mentorship: `https://wa.me/918958006294` (`+91 89580 06294`)

---

### 34.4. Outbound Safeguards & Suppression Protocol
To safeguard domain reputation and prevent bot loops, agents must enforce strict suppression filters:

1. **Internal Domain Suppression**:
   - NEVER send automated replies to `@dbert.in` addresses.
2. **Job Board Relay Suppression**:
   - NEVER send automated replies to proxy relay masks (e.g. `@indeedemail.com`, LinkedIn messaging relays).
3. **Automated Daemon Suppression**:
   - Skip all messages originating from `mailer-daemon@`, `postmaster@`, `no-reply@`, or containing header `Auto-Submitted: auto-generated`.
4. **Anti-Spam Pacing**:
   - Enforce a strict delay of 15 to 30 seconds between consecutive dispatches.
5. **Administrative Milestone Telemetry**:
   - Dispatches automatically send audit reports to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com` at startup, every 100 messages, and upon batch completion.

---

### 34.5. Universal AI Agent Self-Evolution Protocol
When candidates submit unhandled questions or novel edge cases, agents must actively evolve the knowledge base rather than failing silently:

1. **Candidate Quote-Stripping Algorithm**:
   - Extract only the candidate's latest message before classification:
   ```python
   def extract_latest_candidate_message(body: str) -> str:
       lines = body.splitlines()
       clean_lines = []
       for line in lines:
           stripped = line.strip()
           if stripped.startswith(">") or stripped.startswith("-----Original Message-----") or " wrote:" in stripped:
               break
           clean_lines.append(line)
       return "\n".join(clean_lines).strip()
   ```

2. **Dynamic Scenario Registry Pattern**:
   - Avoid long, fragile `if/elif` ladders. Register new intent scenarios dynamically:
   ```python
   SCENARIO_REGISTRY = {}

   def register_scenario(name, intent_keywords, policy_fn):
       SCENARIO_REGISTRY[name] = {
           "keywords": intent_keywords,
           "handler": policy_fn
       }
   ```

3. **Unhandled Inquiry Clustering**:
   - When 2 or more candidates submit inquiries classified with low confidence (`GENERAL_INQUIRY`), extract noun phrases and cluster them.
   - Synthesize a new scenario entry, draft response template adhering to the 600px single-card design system, and append the rule to `AGENTS.md` and `GEMINI.md`.
---

---

## 35. Article Publication Deduplication, Automated Sitemap Integration & Trust Mesh Architecture

### 35.1. Operational Context & 1-Intern-1-Topic Rule
To prevent database bloat, race-condition duplicates, and fragmented reading experiences, DBERT enforces a strict **Single-Article-Per-Topic** constraint for all technical capstones and case studies:
1. **Deduplication Baseline**:
   - Production PostgreSQL database (`dbert_internship.intern_articles`) on EC2 was audited and purged of 19 redundant duplicates (resulting from rapid multi-clicks or lingering drafts after approval).
   - Exactly **22 canonical, unique articles** are retained (13 `PUBLISHED`, 9 `PENDING_REVIEW`).
   - Safety backup table maintained at `dbert_internship.intern_articles_backup_20261114`.
2. **Backend Submission Gating (`apps/portal/app.py` & `routes/stipend.py`)**:
   - In `/intern/articles/save`, before inserting, the engine checks if an article for that `intern_id` and normalized title/slug already exists.
   - If an unapproved draft or pending review exists, it automatically updates the existing record rather than creating a duplicate row.
   - If an article on that topic is already `APPROVED` or `PUBLISHED`, new submissions for that topic are rejected with HTTP 400 (`"You have already published an article for this milestone/topic. Only one article per topic is permitted."`).
   - In `/intern/articles/scaffold`, Gemini case study scaffolding checks existing drafts by submission ID and title, redirecting directly to the editor rather than duplicating.
   - In `/admin/articles/review`, approving or publishing automatically cleans up any dangling drafts for that `(intern_id, topic)` and synchronizes `published_articles.json`.

### 35.2. URL Normalization & Automated XML Sitemaps
1. **Sovereign Blog URL Standard**:
   - All articles live strictly on `https://dbert.in/blog/{slug}`.
   - Legacy and accidental `/insights/{slug}` paths are normalized in the database and permanently redirected via Next.js (`apps/website/next.config.js` with HTTP 308 from `/insights/:slug*` to `/blog/:slug*`).
2. **Synchronized Sitemaps**:
   - **`dbert.in/sitemap.xml`**: Next.js `sitemap.ts` calls `getBlogSlugs()` which reads `apps/website/src/data/published_articles.json` plus static markdown files, assigning `priority: 0.85` and `changeFrequency: 'weekly'`.
   - **`lms.dbert.in/sitemap.xml`**: Flask `sitemap_xml()` queries `intern_articles WHERE status IN ('APPROVED', 'PUBLISHED')` and dynamically emits all canonical `/blog/{slug}` entries.

### 35.3. Bidirectional Trust Mesh Architecture
The technical writing platform functions as an interconnected **Trust Mesh** designed to build institutional credibility for DBERT, prove candidate competency to recruiters, and drive high-intent fellowship enrollments:
1. **Case Study &rarr; Credential Dossier**:
   - `AuthorDossierBox` on `/blog/[slug]` features verified badges linking directly to `https://dbert.in/verify/{certId}`.
   - Displays Turnitin originality validation score (< 3.0% similarity index) and GitHub repo / live deployment links.
2. **Case Study &rarr; Incubation Program & Recruitment Mesh**:
   - Every article includes an **Academic Peer-Review Seal** from the DBERT Academic Board.
   - Features contextual **Fellowship Application CTA** (`/enroll/1999`) to convert organic search readers into candidates.
   - Features direct **Talent Acquisition CTA** (`/verify/directory`) for tech recruiters seeking verified engineers.
3. **Credential Dossier &rarr; Published Case Study**:
   - On `https://dbert.in/verify/[certId]`, when a candidate has a published article, `CandidateProfileClient` renders a prominent gold banner: *"Published Peer-Reviewed Case Study: [Title] &rarr;"* deep-linking to `/blog/[slug]`.
4. **Talent Directory &rarr; Case Study**:
   - In `/verify/directory`, candidate cards render a `📝 Case Study ↗` pill linking to the candidate's published writing.
5. **Schema.org Rich Results**:
   - `ArticleSchema.tsx` injects both `TechArticle` (with `author.hasCredential` linked to `/verify/[certId]`, `publisher` as DBERT India) and `BreadcrumbList` (`Home` &rarr; `Blog` &rarr; `Article Title`).

---

---

## 36. All 9 Platform Domains 7-Day Course Curricula & Seeding Engine

### 36.1. Complete 9-Domain Coverage Mandate
- **All 9 Platform Domains Covered**:
  1. AI Agent Development
  2. Data Analyst
  3. Full Stack Development
  4. Python Automation
  5. UI/UX Design
  6. DevOps & Cloud
  7. Mobile App Development
  8. Cybersecurity
  9. Digital Marketing
- Eliminates the previous domain isolation block where interns in UI/UX Design, DevOps & Cloud, Mobile App Development, Cybersecurity, or Digital Marketing received 0 courses on /courses.

### 36.2. Pedagogical Architecture & Database Schema Parity
- **Course Catalog Module**: pps/portal/config/courses_7day_catalog.py
  - Defines ALL_9_DOMAIN_COURSES (63 total chapters, 189 subtopics, 63 daily quizzes).
- **Curriculum Schema**:
  - courses: domain matching VALID_DOMAINS, is_active=1, content_status='approved', source='custom', is_paid=0.
  - course_chapters: Sequential day_number (1..7) with milestone titles.
  - course_subtopics: Exactly 3 subtopics per day (sort_order 1..3), each containing a concept rief and key_takeaways_json (JSON list of 3 concrete learning outcomes).
  - course_day_quizzes: 1 multiple-choice quiz per day (day_number 1..7) with 4 options and verified correct_index (0..3).

### 36.3. Idempotent Seeding & Deployment Scripts
- **Seeding Daemon**: scripts/seed_all_9_domains_7day_courses.py
  - Runs idempotently on local SQLite and remote EC2 PostgreSQL.
  - Defensively queries IDs instead of relying on driver cur.lastrowid.
- **Production Deployment Daemon**: scripts/deploy_7day_courses_to_ec2.py
  - Deploys updated pp.py and courses_7day_catalog.py to /var/www/dbert-website-lms/apps/portal/.
  - Seeds PostgreSQL database and restarts dbert-portal.service.
  - Verifies all 9 domains and live HTTP 200 health.
- **Automated Pytest Suite**: pps/portal/tests/test_7day_courses_ecosystem.py (100% pass across 7 tests).


---

---

## 37. Dynamic Gemini Model Discovery & Zero Hardcoding Engine

### 37.1. Core Architectural Mandate
- **Zero Model Hardcoding**: NEVER hardcode model strings (e.g., `gemini-1.5-flash`, `gemini-2.0-flash`) in validation loops, default fallbacks, or test endpoints. Models deprecate and vary by API version and project tier.
- **Dynamic Discovery Protocol**: Always query Google's Model Service (`GET https://generativelanguage.googleapis.com/v1beta/models?key=...`), discover all supported generation models live for that specific key, rank them dynamically, and select the best fitted working model.

### 37.2. Dynamic Discovery & Ranking Architecture (`services/ai/gemini_discovery.py`)
1. **Live Discovery**:
   - Fetches available models from Google Generative Language API via `discover_gemini_models(api_key=clean_key)`.
   - Filters models where `"generateContent"` is present in `supportedGenerationMethods`.
   - Strictly excludes non-text models (`tts`, `audio`, `image`, `imagen`, `embedding`, `transcribe`, `clip`, `lyria`, `robotics`, `customtools`).
2. **Semantic Model Ranking (`_rank_models`)**:
   - Stable Flash models prioritized first, sorted by semantic version descending (e.g. 2.5 -> 2.0).
   - Stable aliases (e.g. `gemini-flash-latest`) prioritized alongside current generation.
   - Non-experimental models prioritized over experimental/previews (`exp`, `preview`, `8b`).
   - Stable Pro models next, followed by preview Pro and other text generation models.

### 37.3. Live Validation & Best Fitted Model Selection (`_validate_gemini_key_live`)
- **Discovered Model Testing**:
  - Assembles `candidate_models` directly from `discover_gemini_models` results.
  - Tests minimal live generation (`generateContent` with 1 output token) against the top dynamically discovered candidates (`candidate_models[:5]`).
  - The first candidate model that returns `HTTP 200` is atomically selected as the `best_working_model` and stored at index 0 of `available_models_json`.
- **Project Tier & Billing Interception**:
  - Catches Google's `HTTP 403: The Gemini API free tier is not available for this project` and presents instant guidance to create a key in a new Google AI Studio project with Free Tier enabled.
- **Dynamic Error Reporting**:
  - If all candidate models fail, the error details the exact discovered models tested (`gemini-2.5-flash`, etc.) and Google's actual response, never referencing unqueried or retired models.

### 37.4. Automated Pytest Verification
- `apps/portal/tests/unit/test_gemini_discovery.py` (4 tests)
- `apps/portal/tests/unit/test_gemini_provider.py` (6 tests)
- `apps/portal/tests/test_course_learn_chat_integration.py` (3 tests)
- Total 13 tests verify dynamic discovery, ranking, caching, fallback chains, and live candidate selection.


---

---

## 38. AI Tutor Technical Rigor, Anti-Sycophancy & Causal Reasoning Architecture

### 38.1. Problem Context & Root Cause
- **Sycophancy Bug**: Previously, the AI tutor could pose a question about sequence (e.g. "Which pillar of the CIA Triad is breached first?"), sloppily tack on an ambiguous suffix ("Or is it all of them?"), and then falsely praise a superficial one-word answer ("all") with "Spot on! You nailed it!".
- **Root Cause**: The prompt lacked strict anti-sycophancy guardrails, check questions allowed ambiguous fallbacks, and the model failed to distinguish primary root causes from downstream cascade fallout.

### 38.2. Pedagogical & Prompt Guardrails Implemented (`apps/portal/app.py`)
1. **Zero Sycophancy & False Praise Elimination**:
   - The tutor is strictly prohibited from falsely validating incorrect, ambiguous, or incomplete answers.
   - Phrases like "Spot on!", "You nailed it!", or "Correct!" are forbidden unless the student's answer is factually and technically 100% accurate.
2. **Causal Sequence & Root Cause Analysis**:
   - In questions asking which component, layer, or pillar is breached *first* or represents the root cause, the tutor strictly distinguishes between the initial breach and downstream fallout.
   - Example (CIA Triad): Unauthorized database record tampering / privilege escalation is strictly an **Integrity** breach first. Confidentiality (unauthorized data access) and Availability (data deletion) are downstream consequences that occur after Integrity has been violated.
   - If a student answers "all" or names a downstream consequence, the tutor does not accept "all"; it gently acknowledges the intuition regarding the overall blast radius, but firmly explains why the root breach was Integrity.
3. **Question Formulation Integrity**:
   - Check questions must have a single, definitive, unambiguous technical answer. Vague cop-out suffixes like "Or is it all of them?" or "Or something else?" are strictly forbidden.
4. **Evaluator Schema Alignment (`services/learning/evaluator.py`)**:
   - `StructuredEvaluator` prompt incorporates the same anti-sycophancy and root cause rules, preventing catch-all guesses from receiving passing correctness scores.


---

---

## 39. Gayatri AI Production Deployment & Domain Infrastructure (`gayatrieducation.tech`)

### 39.1. Infrastructure & Co-location Architecture
- **Host**: `ubuntu@3.26.237.171` (AWS EC2)
- **Directory**: `/var/www/gayatri`
- **Internal Port**: `127.0.0.1:5002` (Isolated from Next.js 3001, Flask LMS 5001, FastAPI 8000)
- **Service Name**: `gayatri.service` managed via systemd (`User=ubuntu`, `Group=ubuntu`, `Restart=always`)
- **Process Manager**: Gunicorn WSGI with 2 gthread workers and 2 threads (`--worker-class gthread`)
- **Memory Consumption**: ~158 MB
- **Database Engine**: SQLite in WAL mode at `/var/www/gayatri/instance/gayatri.db` (83 tables preserved)
- **Log Files**: `/var/log/gayatri/access.log` and `/var/log/gayatri/error.log`

### 39.2. Nginx Reverse Proxy Configuration
- **Config Path**: `/etc/nginx/sites-available/gayatri.conf` (Symlinked to `sites-enabled/`)
- **Hostnames Served**: `gayatrieducation.tech`, `www.gayatrieducation.tech`, `gayatreeducation.tech`, `www.gayatreeducation.tech`, `gayatrieducation.info`, `www.gayatrieducation.info`
- **Direct Static Assets**: `/static/` mapped to `/var/www/gayatri/app/static/` (30-day cache)
- **Direct Uploads**: `/uploads/` mapped to `/var/www/gayatri/uploads/` (7-day cache)
- **Reverse Proxy**: Dynamic requests proxied to `http://127.0.0.1:5002` with 180s read timeout for Gemini AI streaming
- **ACME Path**: `/.well-known/acme-challenge/` mapped to `/var/www/certbot` for Let's Encrypt renewal

### 39.3. Key Deployment & Verification Commands
```powershell
# Deploy/Update Gayatri AI codebase to EC2
python scripts/deploy_gayatri_to_ec2.py

# Check Gayatri systemd service status
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" ubuntu@3.26.237.171 "sudo systemctl status gayatri.service --no-pager"

# Probe internal Gunicorn listener
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" ubuntu@3.26.237.171 "curl -I -s http://127.0.0.1:5002/"

# Probe Nginx reverse proxy on port 80
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" ubuntu@3.26.237.171 "curl -I -s -H 'Host: gayatrieducation.tech' http://127.0.0.1/"

# Provision SSL Certificate (Run once DNS A-record points to 3.26.237.171)
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" ubuntu@3.26.237.171 "sudo certbot --nginx -d gayatrieducation.tech -d www.gayatrieducation.tech --non-interactive --agree-tos -m abhinav.sharma@dbert.in --redirect"
```

---

---

## 40. Unified Job Application Flow & External Lead Redirection Engine

### 40.1. Core Architectural Rules
1. **Authentication Gate & Funnel Auto-Resume**:
   - Applying for any internal job or external lead requires candidate authentication.
   - For unauthenticated users hitting `/apply/<post_id>` or clicking "Apply Now", the system stores the target with `?apply=1` into `session['next']` and redirects to `/signup?next=<destination>%3Fapply%3D1` (with an explicit `"Already registered? Sign In"` linking to `/signin?next=...`).
   - After authentication, the user returns to the job page with `?apply=1` automatically expanding the Application Modal on DOM ready.
2. **Suitability Pitch Modal Requirement**:
   - The modal explicitly queries: *"Why are you suitable for this opportunity? \*"*.
   - Strictly enforces a **minimum of 15 characters** (and maximum 2,000 characters) on both client-side and backend (`POST /posts/<id>/apply` and `POST /api/lead/<id>/comment`).
   - A live dynamic character counter (`0 / 15 min`) turns green when the threshold is reached.
3. **Dual Routing & Conversion Preservation**:
   - **Internal LMS Postings (`posts` table)**:
     - Application note recorded in `post_applications` with status `'Applied'`.
     - Outbound applicant notification emails are disabled (applications visible to companies directly in `/company/posts/<id>/applicants`).
     - On-screen confirmation card rendered with links to *My Applications* and *Browse more openings*.
   - **External Curated Leads (`scraped_jobs` / `scraped_internships`)**:
     - Suitability pitch saved to `scraped_job_comments` / `scraped_internship_comments`.
     - Clicks tracked asynchronously via `/api/lead/<id>/click`.
     - Automatically launches the employer's official link in a new tab (`window.open(TARGET_URL, '_blank', 'noopener,noreferrer')`).
     - Transforms the on-screen apply zone into an unblockable fallback card (*"Application Note Recorded! Continue to Official Application ↗"*), eliminating lost conversions caused by aggressive browser pop-up blockers.


---

---

## 41. Universal BYOK Gemini API Key Architecture & Course-Style Bounty Stepper

### 41.1. Single Source of Truth for Gemini API Keys
- **Primary Source**: https://lms.dbert.in/account/gemini-key
- **Database Tables**:
  - user_api_keys (provider='gemini', pi_key Fernet-encrypted). This table holds all candidate-entered BYOK keys.
  - Mirrored / synchronized to intern_accounts.gemini_api_key_encrypted upon save.
- **Rule for All Future Agents & Portal Features**:
  - **NEVER prompt the intern/user for an API key on individual tasks, forms, modals, or pages.**
  - All portal features requiring Gemini AI (Bounty content generation, Stipend task evaluation, ATS resume scans, RAG tutor chats, case study generator) MUST resolve the key via get_intern_active_gemini_context(intern_id) or get_intern_gemini_key(intern_id).
  - These helper functions inspect user_api_keys first, decrypt via _decrypt_gemini_key, and verify functionality against Google's API via discover_gemini_models.
  - Models are dynamically ranked by capability and freshness (gemini-2.5-flash preferred over legacy models). Hardcoding gemini-1.5-flash or deprecated endpoints is strictly prohibited.
  - If a user visits an AI-powered feature without an active key, they are redirected to /account/gemini-key?next=<current_route> with an informative message. Upon saving their key, they are automatically returned to their originating task.

### 41.2. Course-Style Stepper Workflow (/tasks/<id>/guide)
- Replaces cramped popup modals with a dedicated full-page guided experience styled after LMS courses (/courses/<id>/learn).
- **Social Media Bounties (Tasks 101–104)**:
  - **Step 1: Assigned Angle & Case Study Context**: Dynamically selects domain-specific angle and capstone case study.
  - **Step 2: 1-Click AI Post Synthesis**: Generates platform-optimized copy (LinkedIn / X) using the intern's saved Gemini BYOK key in one click.
  - **Step 3: Publish to Platform**: 1-click 'Copy Post & Open Platform ↗' button opening the candidate's profile/post composer with pre-filled hashtags.
  - **Step 4: Submission & Verification**: Submits live URL to /tasks/<id>/submit for mentor review and coin disbursement.
- **Domain Micro-Tasks**: 3-step technical workflow (Briefing & Rubric -> Implementation Guidelines -> Verification Submission).

---

---

## 42. Official Internship Offer Letter, Preview Gating & Digitally Signed PDF Engine (`/portal/offer`)

### 42.1. System Overview & Gating Architecture
- **Target Route**: `https://lms.dbert.in/portal/offer` (Executive Print View: `/portal/offer/print`).
- **Access Rule**: Requires authenticated intern session (`require_role('intern')`).
- **Gating Lifecycle**:
  1. **Under Review / Unselected Candidates (Stage 1 & 2)**:
     - Candidates without selection or enrollment see the **Official Offer Letter Gated: Seat Confirmation Required** card (`locked=True`).
     - Includes direct links to application status, verification form, and Admissions WhatsApp concierge (`+91 81929 11360`).
     - Eliminates raw 404 errors by explaining current review state and required next steps.
  2. **Selected Candidates with Caution Deposit Pending (Stage 3 & 4)**:
     - Rendered with `locked=False`, `preview_mode=True`.
     - Displays **Appointment Terms Preview** and diagonal **PREVIEW ONLY** watermarks.
     - **Read & Sign First**: Candidates can review terms and execute digital acceptance (`POST /portal/offer/sign`).
     - PDF download `/portal/offer/print` remains gated (`requires_deposit=True`) until ₹499 caution deposit is verified.
  3. **Verified Candidates with Caution Deposit Reconciled (Stage 5 - Confirmed)**:
     - Rendered with `locked=False`, `preview_mode=False`.
     - Displays `STATUS: ACCEPTED & SIGNED`, Offer Ref ID, and active **Download Official Signed PDF** button unlocking `/portal/offer/print`.
- **Deterministic ID Generation**:
  - Format: `DBERT-OFR-2026-{TRACK_CODE}-{ENROLLMENT_ID:04d}` (e.g. `DBERT-OFR-2026-AIML-9204`, `DBERT-OFR-2026-DA-0127`).
- **Dedicated Relational Table (`intern_offer_letters`)**:
  - Tracks candidate ID, offer reference ID, batch start/end dates, tenure (2 months), stipend amount (₹5,000), digital signature name, acceptance timestamp, IP address, and `pdf_unlocked`.

### 42.2. Official Offer Terms & Governance
- **Issuing Entity**: DBERT Technical Council (MSME Registered: `UDYAM-UP-29-0109046`).
- **Council Signatory**: Mr. Abhinav Sharma (Founder & Executive Director).
- **Tenure**: Two (2) Months — Fully Remote.
- **Fixed Stipend**: ₹5,000, governed by 3 transparent milestones:
  1. Minimum 10 hours per week login attendance recorded on the LMS platform.
  2. Earning at least two (2) verified course certifications on the platform.
  3. Completing at least 75 mentor-reviewed bounty tasks.
- **Caution Deposit**: ₹499 (100% Credited / Refundable upon milestone completion).

### 42.3. Interactive Digital Signing & Executive Print Export
- **Digital Signing Engine (`POST /portal/offer/sign`)**:
  - Candidate executes legal acceptance by typing their full legal name and agreeing to terms.
  - Records candidate legal name in `signature_name`, current IST timestamp in `accepted_at`, signer IP, and sets `pdf_unlocked=1` if deposit is verified.
- **A4 PDF Export (`/portal/offer/print`)**:
  - Embeds high-fidelity legal styles with `@media print` (`size: A4 portrait; margin: 12mm 15mm 12mm 15mm`).
  - Pre-renders formal DBERT header, candidate appointment rubric, QR verification code (`https://dbert.in/verify/offer/{offer_id}`), and executive signature seal.
  - CSS rules prevent page breaks across tables, terms, and signatures (`break-inside: avoid`).

### 42.4. Local Google Workspace SMTP Dispatch Bot
- **CLI Script**: `scripts/dispatch_offer_letters_local.py`
- **Execution Mode**: Strictly local via authenticated Google Workspace SMTP (`smtp.gmail.com:465`) authenticated as `manoj.kumar@dbert.in` (Academic Lead & Admissions).
- **Deliverability & Safety**:
  - Paced delivery with configurable pauses (default 30s) to avoid spam rate limits.
  - Multipart MIME (text-forward HTML + plain-text RFC fallback).
  - Idempotent tracking recorded in `data/dispatch_tracking_offers.json` and `.csv`.
  - Commands:
    ```powershell
    # Check queue stats (eligible verified candidates)
    python scripts/dispatch_offer_letters_local.py --stats

    # Dry-run inspection
    python scripts/dispatch_offer_letters_local.py --dry-run

    # Send 1 test dispatch to personal inbox
    python scripts/dispatch_offer_letters_local.py --test-to your_email@gmail.com

    # Send batch of 10 with 30s pacing
    python scripts/dispatch_offer_letters_local.py --batch 10 --delay 30
    ```

### 42.5. Staged Offer Review, Transparent Watermark & Payment Execution Flow
- **Screen 1 (`#screenOfferReview`) — Appointment Letter Review**:
  - **Transparent Watermark**: Styled with `background: rgba(254, 243, 199, 0.10)`, delicate dashed border `rgba(217, 119, 6, 0.22)`, and zero blur (`backdrop-filter: none !important`), ensuring every clause, compensation milestone, and legal term is razor-sharp while retaining preview stamping.
  - **Review Completion Bar**: Positioned at the document footer with Step 1 check and prominent `#btnAcceptAndSignBottom` (`Accept & Sign Offer Letter →`) transitioning candidates directly to Screen 2.
- **Screen 2 (`#screenActionSteps`) — Staged Execution & Seat Confirmation**:
  - **Back Navigation**: Includes `#btnBackToReview` (`← Review Appointment Letter`) and candidate reference chips.
  - **Step 2 (Digital Acceptance)**:
    - *Unsigned State*: Displays `#offerSignCard` with Full Legal Name input, Indian IT Act 2000 acceptance checkbox, and `#signSubmitBtn`.
    - *Signed State*: Immediately renders green `#signedBanner` (`STEP 2 COMPLETED: AGREEMENT EXECUTED`) with verified signature name and timestamp.
  - **Step 3 (Seat Confirmation)**:
    - Unfolds upon digital signature execution or lands directly for previously signed candidates.
    - Sized-down compact QR code (115px × 115px) with dedicated `#btnDownloadOfferQr` (`/static/img/qrcode.jpeg`) and `#copyVpaBtn` (`Q652429146@ybl`).
    - High-contrast, brand-distinct 1-Tap UPI Launchers: GPay (`#ffffff`), PhonePe (`#5f259f`), Paytm Electric Cyan (`#00baf2` with `#002970` deep navy text to eliminate dark card blending), and Any UPI radiant gold gradient.
    - 12-digit UTR submission form with real-time regex validation and instant admissions ledger reconciliation.
- **Strict Nonce CSP Compliance**:
  - Converted all triggers from `<a>` anchors with pseudo-URLs (`javascript:void(0)`) to `<button type="button">`.
  - Exactly **0 inline `onclick` or pseudo-protocol handlers** across the template.
  - All interactive listeners (`btnReviewSignTop`, `btnConfirmSeatTop`, `btnAcceptAndSignBottom`, `btnBackToReview`, `stepperStep1-3`, `copyVpaBtn`, `btnPrintOfferTop`, `btnPrintOfferDossier`) are bound programmatically in `DOMContentLoaded` within `<script nonce="{{ csp_nonce() }}">`.

---

## 43. Web Push Strict Nonce CSP Compliance & Seeded Lifecycle QA Matrix

### 43.1. Architectural Mandate: Strict Nonce CSP Event Binding
- **Strict Nonce Enforcement**: DBERT LMS enforces `Content-Security-Policy: script-src 'self' 'nonce-{nonce}' ...`. Under modern browser security specifications, **all inline event handlers (`onclick`, `onchange`, `onsubmit`) are unconditionally blocked by the browser engine**.
- **Zero Inline Event Handlers**: All UI actions on `https://lms.dbert.in/account/notifications`, `/portal/offer`, and throughout `apps/portal/templates/` must be bound via standard DOM `addEventListener` inside `<script nonce="{{ csp_nonce() }}">`.
- **Root Service Worker Route (`/sw-push.js`)**:
  - Serves directly at origin root with header `Service-Worker-Allowed: /` and `Content-Type: application/javascript`.
  - Configured in Nginx (`deploy/dbert-unified-nginx.conf`) and Flask (`@app.route("/sw-push.js")`).
  - Fallback: `dbert-push-client.js` automatically attempts fallback to `/static/sw-push.js` if root registration encounters unexpected network issues.

### 43.2. Seeded Personas Lifecycle QA Matrix (Uniform Password: `TestPass123!`)
All 8 personas are seeded on production EC2 PostgreSQL (`dbert_lms`):

| Persona Role | Email Address | Intended Stage & Platform Features | Live Verification URL |
| :--- | :--- | :--- | :--- |
| **Staff Reviewer** | `mentor_staff@dbert.test` | Review Capstones, release 5,000 coins, send Push Broadcasts, Mentor slot 901 | `/staff/tasks`<br>`/admin/push-broadcast` |
| **Super Admin** | `dbert_admin@dbert.test` | Executive system overview, System Health Cards | `/admin` |
| **Enrolled Fellow** | `fellow_enrolled@dbert.test` | Active Sprint Fellow (Day 2 of FSD), Social Bounties (101–104), Push Settings | `/portal`<br>`/tasks`<br>`/account/notifications` |
| **Stipend Ready** | `stipend_ready@dbert.test` | 3-Step checklist all green (`CERT-DBERT-2026-AIML-904`, 65 days elapsed, UPI), Capstone submission form open | `/stipend/tasks` |
| **Withdrawable Wallet** | `stipend_wallet@dbert.test` | 5,000 Coins in Referral/Stipend balance, encrypted UPI, 1-tap payout request | `/account/coins`<br>`/ambassador` |
| **Provisional Fellow** | `stipend_gate1_locked@dbert.test` | Gate 1 LOCKED, alert banner with CTA to [dbert.in/enroll/1999](https://dbert.in/enroll/1999) | `/stipend/tasks` |
| **Stage 3 Selected** | `stage3_selected@dbert.test` | Selection banner with Monday cohort start date and ₹499 caution deposit reconciliation instructions | `/portal` |
| **Offer Letter Ready** | `offer_pending@dbert.test` | Official Letter of Offer (`DBERT-OFR-2026-PA-991`), digital signature, terms agreement, A4 print export | `/portal/offer` |

### 43.3. Automated CLI Verification Script
```powershell
# Run end-to-end automated session audit across all 8 personas on EC2
python scripts/test_persona_routes_on_ec2.py
```

---

---

## 44. Multi-Stage Signup Funnel Diagnostics & "Pending Profile" Root Cause Analysis

### 44.1. Incident Context & User Query
- **Issue Description**: In the LMS Admin Application Queue (`/admin`), a cluster of recent applicants (IDs 5190–5207: Nakshathiraa A, chundi kowshikreddy, RAVIRANJAN KUMAR, Gowtham B, Shorya saini, MD RAZA, Addagatla Laxman vikram, RIMJHIM KANAUJIA, etc.) appeared with:
  - **College**: `Pending Profile`
  - **Domain**: `AI Agent Development`
  - **Status**: `Under Review`
- **Contrast**: Other applicants (e.g. 5203 Rabiya, 5198 Anuj Khajuria, 5196 Chandradeep Saxena, 5195 Bipin Banala) had authentic college names and specific domain preferences.

### 44.2. Root Cause Discovery & Architectural Breakdown
1. **Funnel Redirect Hijack (`next_url` / `?apply=1`)**:
   - Candidates arrive at specific internship listings (e.g. *Python Automation API Intern at Zoho*, *Threat Intelligence Intern at VigilantGuard*, *Figma Design System Intern*).
   - Clicking "Apply Now" while logged out sets `next=<job_url>?apply=1` in query parameters or Flask session (`session["next"]`).
   - The user fills **Step 1** (Name, Email, Phone, Password).
   - In `apps/portal/app.py:11159-11175` (`signup_stage1`):
     ```python
     pending_next = _safe_portal_next(request.args.get("next") or session.pop("next", None) or data.get("next"))
     if pending_next:
         resp = make_response(jsonify({
             "status": "success",
             "message": "Account created! Redirecting to application...",
             "stage": 1,
             "redirect": pending_next
         }))
     ```
   - In `apps/portal/templates/index.html:964-967`:
     ```javascript
     if(data.redirect){
       showToast('Account created! Redirecting to application...','success');
       setTimeout(()=>{window.location.href=data.redirect;},400);
       return;
     }
     ```
   - **Result**: The browser immediately redirects the user back to the internship page. The multi-step wizard (`suGoStep(2)`) is completely bypassed. Step 2 (Academics/College) and Step 3 (Statement/Links) are never rendered.

2. **Hardcoded Domain Fallback (`app.py:11101-11103`)**:
   - Stage 1 form payload in `index.html:959` only collects identity fields and does not include `domain`.
   - `chosen_domain = clean_text(data.get("domain"))` evaluates to `None`.
   - The fallback condition triggers:
     ```python
     if chosen_domain not in VALID_DOMAINS:
         chosen_domain = "AI Agent Development"
     ```
   - **Result**: 100% of Stage 1 signups are assigned "AI Agent Development", even when applying for Python Automation, Cybersecurity, or UI/UX Design.

3. **Eager Application Insertion in `STATUS_UNDER_REVIEW` (`app.py:11107-11125`)**:
   - Upon Stage 1 submission, an application row is prematurely inserted into the `applications` table:
     - `college`: `clean_text(data.get("college")) or "Pending Profile"`
     - `domain`: `chosen_domain` ("AI Agent Development")
     - `status`: `STATUS_UNDER_REVIEW`
     - `source`: `'direct_signup'`
     - `why_join`: `'Enrolled via DBERT portal direct registration.'`
   - **Result**: Incomplete accounts are immediately flagged as active applications "Under Review", polluting the admin queue.

4. **Step 2/3 Drop-Off & Lack of Portal Profile Gate**:
   - Direct homepage signups without `next_url` (e.g. Kowshikreddy) who abandon the wizard at Step 2 or Step 3 leave behind the provisional row created at Step 1.
   - The student dashboard (`/portal`) does not currently check or prompt users with `signup_stage < 2` or `college = 'Pending Profile'` to complete their academic background.

### 44.3. Verified Production Metrics (EC2 PostgreSQL `dbert_lms`)
- **`intern_accounts` Table**:
  - `signup_stage = 1`: **480 accounts** (account created, academics pending).
  - `signup_stage = 2`: **197 accounts** (academics saved, statement pending).
  - `signup_stage = 3`: **2,207 accounts** (full profile submitted).
- **`applications` Table (`college = 'Pending Profile'`)**:
  - `status = 'Under Review'`: **11 candidates** (the recent cohort observed in Admin).
  - `status = 'Selected'`: **164 candidates** (historical cumulative drop-offs).
  - Domain breakdown for all 175 `Pending Profile` rows: **100% `AI Agent Development`**.

### 44.4. Architectural Remediation & Implementation Plan
1. **Defer Redirect Until Academic Completion**:
   - In `app.py:signup_stage1`: Do not return `redirect: pending_next` at Stage 1. Keep `next_url` stored on the session row, and only return `redirect: pending_next` upon **Stage 2 or Stage 3** completion.
2. **Contextual Domain Capture**:
   - In `index.html`: Ensure `suNext1()` captures and passes the current route/lead track or URL parameter (`?domain=...`) in the Stage 1 payload.
3. **Application Status Hygiene (`Draft` vs `Under Review`)**:
   - Insert Stage 1 records with `status = 'Draft'` or `Incomplete Profile`. Only promote to `STATUS_UNDER_REVIEW` once Stage 2 (Academics & College) is successfully submitted.
4. **In-Portal Academic Profile Completion Gate**:
   - On `/portal`, check if `intern.signup_stage < 2` or `college = 'Pending Profile'`. If true, render an alert banner with a 1-click modal allowing the student to save their real College, Course, and Domain Track.

### 44.5. Implemented Architectural Changes
1. **Backend Engine Refactoring (`apps/portal/app.py`)**:
   - **`signup_stage1`**:
     - Introduced `DOMAIN_SLUG_MAP` to infer target domain from `pending_next` lead URLs (e.g. `python-automation` -> `Python Automation`, `threat-intelligence` / `cybersecurity` -> `Cybersecurity`, `figma` / `ui-ux` -> `UI/UX Design`).
     - Inserts the provisional application with canonical status `STATUS_APPLY_PENDING` (`"Apply Pending"`) rather than `STATUS_UNDER_REVIEW`.
     - Persists `next_url` into `user_sessions` and returns `{ "stage": 1, "next": 2 }` without short-circuiting the wizard.
   - **`signup_stage2`**:
     - Atomically updates academic fields: `city`, `college`, `course`, `semester`, `year_of_passing`, and `domain`.
     - Promotes application status from `STATUS_APPLY_PENDING` to `STATUS_UNDER_REVIEW`.
     - Advances user account to `signup_stage = 2` and returns `redirect: resume` to smoothly route the user to their target internship listing.
   - **`portal_page` (`/portal`) & `/intern/me`**:
     - Added `needs_academic_profile` evaluation (evaluates to `True` if `signup_stage < 2` or `college` is empty/`Pending Profile`).
2. **Frontend Signup Flow (`apps/portal/templates/index.html`)**:
   - **`suNext1()`**: Dynamically extracts target domain from modal select, URL query parameters (`?domain=...`), or lead route, and includes `domain` in `POST /signup/stage1`. Removed premature redirect; advances seamlessly to `suGoStep(2)`.
   - **`suGoStep(2)`**: Pre-selects matching domain pill/dropdown in Step 2.
   - **`suNext2()`**: Saves academic details and navigates user to `data.redirect` if an internship lead was pending.
3. **In-Portal Academic Gate & Modal (`apps/portal/templates/portal.html`)**:
   - Injected `#academicProfileBanner` at the top of the Overview panel for users with pending profiles.
   - Injected `#academicProfileModal` collecting College Name, Degree/Course, Semester, Year of Passing, City, and Domain Track.
   - Strictly Nonce CSP compliant (`<script nonce="{{ csp_nonce() }}">`) with DOM event listeners (`addEventListener`) posting to `POST /signup/stage2`.
4. **Admin Queue Status Filtering (`apps/portal/templates/admin.html`)**:
   - Added `<option value="Apply Pending">Apply Pending (Incomplete)</option>` to `#appStatusFilter`.
   - Styled `college === 'Pending Profile'` rows in `PG_RENDER.app` with an amber badge (`badge-amber`).

### 44.6. Database Backfill & Reconciled Historical Cohort
- Executed `scripts/reconcile_and_backfill_pending_profiles.py` on production EC2:
  - Reclassified 12 incomplete provisional applications from `Under Review` to `Apply Pending` (IDs 5193, 5194, 5197, 5199, 5200, 5201, 5202, 5204, 5205, 5206, 5207, 5208).
  - Accurately backfilled target tracks based on candidate acquisition leads:
    * `Nakshathiraa A` -> `Python Automation`
    * `Ayush bhat` -> `Cybersecurity`
    * `MD RAZA` -> `Data Analyst`
    * `Addagatla Laxman vikram` -> `UI/UX Design`
    * `RIMJHIM KANAUJIA` -> `Cybersecurity`
    * `Vaibhav Gadge` -> `DevOps & Cloud`
    * `JISNA AV` -> `Cybersecurity`
  - Reconciled queue: active `Under Review` queue now strictly contains candidates with verified colleges (e.g. Rabiya, Anuj Khajuria, Chandradeep Saxena, Bipin Banala).

### 44.7. Automated Test Suite & Regression Verification
1. **End-to-End Funnel & Academic Gate Test (`scripts/test_stage_funnel_and_profile_fixes.py`)**:
   - **Stage 1 (Account Creation)**: Verified non-redirecting response (`stage=1`, `next=2`, no premature `redirect`).
   - **Stage 1 DB Verification**: Verified `applications.status = 'Apply Pending'`, `college = 'Pending Profile'`, `intern_accounts.signup_stage = 1`.
   - **Portal Evaluation**: Verified `/portal` renders with `needs_academic_profile = True`.
   - **Stage 2 (Academic Completion)**: Saved college ("Indian Institute of Technology Madras"), course, and domain. Verified promotion to `STATUS_UNDER_REVIEW`, `signup_stage = 2`, and return of `redirect = '/internships/...'`.
   - **Portal Re-evaluation**: Verified `/portal` renders with `needs_academic_profile = False`.
   - **Result**: **100% PASS** across all stages.
2. **Seeded Test Personas Regression Test (`scripts/test_persona_routes_on_ec2.py`)**:
   - Verified all 8 seeded personas (`stipend_gate1_locked`, `stipend_ready`, `stipend_wallet`, `provisional_fellow`, `fellow_enrolled`, `stage3_selected`, `offer_pending`, `mentor_user`) across their dedicated routes on live EC2.
   - **Result**: **100% PASS (8/8 personas active & verified)**.

---

## 45. Dynamic UPI Payment Verification Voucher Engine & Screenshot Architecture

### 45.1. Incident Context & Root Cause Analysis (`ERR_INVALID_RESPONSE`)
- **Reported Incident**: Navigating to `https://lms.dbert.in/admin/screenshot/utr_666501928441.receipt` resulted in Chrome displaying:
  `This site can’t be reached - ERR_INVALID_RESPONSE`.
- **Candidate Affected**: Bhargavi Poola (`bhargavi13032007@gmail.com`, Enrollment ID 453, UTR `666501928441`, ₹499 Caution Deposit).
- **Core Diagnostic Breakdown**:
  1. **Virtual Placeholder Generation Without File Creation**: When candidates enroll with a 12-digit UPI UTR without uploading an image, `apps/portal/app.py:16214` assigned `filename = f"utr_{utr_val}.receipt"` to satisfy the `payment_screenshot` database column, but wrote no physical file to disk.
  2. **Filesystem Route Blindness**: The route `/admin/screenshot/<filename>` strictly attempted to locate physical files under `UPLOAD_FOLDER`. Because `utr_666501928441.receipt` was absent on disk, it returned `404 Not found`.
  3. **Duplicate & Conflicting HTTP Security Headers**:
     - Flask's `after_request` was unconditionally injecting `resp.headers.setdefault("Content-Disposition", "attachment")` and `resp.headers.setdefault("X-Frame-Options", "DENY")`.
     - Nginx simultaneously injected `add_header X-Frame-Options "SAMEORIGIN" always`.
     - The resulting HTTP/2 response contained conflicting duplicate `x-frame-options: DENY, SAMEORIGIN` headers and an attachment disposition without a filename on an error body. Chromium's network stack rejects this as an invalid response (`ERR_INVALID_RESPONSE`).

### 45.2. Dynamic Voucher Engine & Architectural Solution
1. **Dynamic Vector SVG Voucher Generator (`generate_utr_voucher_svg`)**:
   - When a requested filename matches `utr_<digits>.receipt`, starts with `utr_`, or ends with `.receipt`, the backend extracts the 12-digit UTR and executes `get_utr_voucher_record()`.
   - Generates an executive 840×560 vector SVG canvas (`Content-Type: image/svg+xml; charset=utf-8`):
     * DBERT Admissions & Credentials gold-crested header.
     * Candidate Full Name, Email, Phone, College, and Domain Track.
     * Prominent high-contrast gold monospace 12-digit UTR reference card.
     * Transaction Value (₹499 / ₹1,500), timestamp, and verification badge.
     * Cryptographic verification seal.
   - Served with `Content-Disposition: inline`, allowing native in-browser rendering in `<img>` tags, full-size new tabs, and print engines.
2. **Missing Physical Asset Fallback (`generate_missing_asset_svg`)**:
   - If a physical file is referenced but genuinely absent from disk, rather than returning raw text with broken headers, the route serves a graceful, styled vector SVG graphic informing the admin that the asset was recorded as a ledger reference.
3. **HTTP Header Alignment & De-duplication**:
   - In `apps/portal/app.py`: Updated `X-Frame-Options` from `DENY` to `SAMEORIGIN` across Flask.
   - Updated `Content-Disposition` under `/admin/screenshot/` to `inline` for successful previews and eliminated attachment headers on HTTP error responses.
   - In `deploy/dbert-unified-nginx.conf`: Added `proxy_hide_header X-Frame-Options` and `proxy_hide_header X-Content-Type-Options` to eliminate upstream header duplication.

### 45.3. Admin UI Enhancements (`apps/portal/templates/admin.html`)
1. **Differentiated Queue Badges**:
   - In `PG_RENDER.enr`: Detects `utr_*.receipt` records and renders a distinct gold button:
     `<button class="btn-sm ghost" ${actAttr('click','viewScreenshot',[r.payment_screenshot,r.name,r.utr||''])} title="View UPI UTR Digital Receipt"><i class="fas fa-receipt text-gold"></i> UTR</button>`.
   - Real image uploads continue to render the `<i class="fas fa-image"></i>` button.
2. **Interactive Modal Callout & 1-Click Copy**:
   - When a UTR voucher is opened, an amber callout banner displays the 12-digit UTR with a 1-click **"Copy UTR"** button (`copyUtr()`).
   - Deep-link dynamically labels as *"Open Full-Size Digital Voucher"*.

### 45.4. Production Verification & Operational Matrix
- **Automated Route Test (`scripts/test_screenshot_and_voucher_on_ec2.py`)**:
  * `/admin/screenshot/utr_666501928441.receipt` -> **HTTP/2 200 OK** (`image/svg+xml`, `SAMEORIGIN`, Bhargavi Poola, 666501928441).
  * Missing file fallback (`non_existent_12345.png`) -> **HTTP/2 404** (Graceful vector SVG fallback).
  * Unauthenticated navigation -> **HTTP/2 302** (Redirect to `/signin?next=...`).
  * **Result**: **100% PASS**.
- **Seeded Test Personas Regression Test (`scripts/test_persona_routes_on_ec2.py`)**:
  * **Result**: **100% PASS (8/8 personas active & verified)**.

---

## 46. Lifecycle State Synchronization, Auto-Healing Profile Sync & Offer Letter Exclusivity Architecture

### 46.1. Incident Context & Contradiction Analysis
Prior to this remediation, candidates who were formally Selected, Signed, and Confirmed (e.g. `abhinav.sharma@dbert.vom` / ID `5624` with signed appointment ref `DBERT-OFR-2026-FSD-5166`) experienced contradictory state rendering and UI clutter across the LMS platform:
1. **State Fallback Collision on `/portal`**:
   - `/portal` displayed: *"Action Required: Complete Your Academic Profile"* and *"Stage 1: Under Evaluation - Your Immediate Next Action... Application Under Evaluation"*.
   - At the same time, `/portal/offer` displayed: *"Official Selection & Appointment - STATUS: ACCEPTED & SIGNED"*.
   - **Root Cause**: `portal_page()` in `apps/portal/app.py` previously rendered `portal.html` without passing server-side `flow_state`, `current_stage`, or `next_action`. As a result, Jinja evaluated `{{ (next_action and next_action.heading) or 'Application Under Evaluation' }}`, permanently falling back to hardcoded Stage 1 defaults. Furthermore, `/intern/me` did not return `"next_action"` in its JSON response, so client-side `renderNextActionMissionCard()` immediately aborted (`if (!na) return;`), locking `#nextActionMissionCard` on Stage 1 defaults for ALL users regardless of their actual stage.
2. **False Academic Profile Alert**:
   - `needs_academic_profile` in `portal_page()` previously only evaluated `intern_accounts`. If an intern was already in Stage 3, 4, or 5, or if their `college` and `domain` were entered in `applications` or `enrollments` before `intern_accounts` was updated, it erroneously flashed a high-priority warning banner.
3. **Ghost Payment Form on `/portal/offer`**:
   - Even when a candidate's caution deposit was verified and reconciled (`caution_deposit_status == 'VERIFIED'`), `#postSignPaymentSection` (containing Step 3 QR code, 1-tap UPI launchers, and the 12-digit UTR submission form) was rendered into the DOM with inline `style="display:none;"`. This left payment forms accessible in the DOM, creating visual confusion, crawler indexation issues, and text bleeding below the verified dossier card.
4. **Ghost NextStep Card Artifacts**:
   - `#nextStepCard` sat unhidden below `#nextActionMissionCard`, causing empty emoji and dash text (`👋 — —`) to flash on initial load.

---

### 46.2. Architectural Solution & Implementation
1. **Canonical Server-Side State Pipeline (`build_intern_next_action`)**:
   - Implemented `build_intern_next_action(flow_state, hours_logged=0.0)` in `apps/portal/app.py` as the single canonical source of truth for dashboard mission guidance across all 5 lifecycle stages:
     - **Stage 1 (`APPLICATION_REQUIRED`)**: Badge: `"Stage 1: Under Evaluation"`, Heading: `"Application Under Evaluation"`, CTAs: WhatsApp review expediter + Curriculum tracks.
     - **Stage 2 (`UNDER_REVIEW`)**: Badge: `"Stage 2: Fast-Track Available"`, Heading: `"Fast-Track Incubation Review & Seat Allocation"`, CTAs: Review terms & fast-track seat (`/portal/offer`) + Admissions WhatsApp + Curriculum preview.
     - **Stage 3 (`SELECTED`)**: Badge: `"Stage 3: Selection & Appointment"`, Heading: `"Formal Appointment Extended — Seat Confirmation Required"`, CTAs: Review & sign offer letter (`/portal/offer`) + Admissions WhatsApp desk.
     - **Stage 4 (`PAYMENT_PENDING`)**: Badge: `"Stage 4: Verification in Progress"`, Heading: `"₹499 Caution Deposit Under Administrative Verification"`, CTAs: WhatsApp verification expediter + Offer status (`/portal/offer`).
     - **Stage 5 (`CONFIRMED`)**:
       - *Within 7-day grace period*: Badge: `f"Stage 5: Active Intern · Day {days+1} of 7-Day Window"`, Heading: `f"Sprint Workspace Active ({days_left} Days Remaining in Balance Window)"`, CTAs: Continue sprints (`/courses`) + Complete ₹1,500 balance (`/enroll/1999`) + View appointment letter (`/portal/offer`).
       - *Grace period expired (> 7 days)*: Badge: `"Stage 5: Sprint Active · Balance Completion Required"`, Heading: `"Sprints Active · Complete ₹1,500 Balance to Unlock Credentials"`, CTAs: Complete ₹1,500 balance now (`/enroll/1999`) + Resume sprints (`/courses`).
       - *Fully paid (₹1,999)*: Badge: `"Stage 5: Confirmed Fellow · Verified"`, Heading: `"Active Engineering Incubation Fellow"`, CTAs: Launch sprint workspace (`/courses`) + Download signed offer PDF (`/portal/offer`).
   - `portal_page()` computes `flow_state = get_intern_flow_state(conn, email_clean)` and passes `flow_state`, `current_stage`, `next_action`, and `needs_academic_profile` directly to `render_template("portal.html")`. This eliminates all layout shifts, fallback collisions, and client-render delay on initial paint.

2. **Auto-Healing Academic Profile Synchronization**:
   - `portal_page()` checks `intern_accounts` against `applications` and `enrollments`. If `college` or `domain` is missing or marked "Pending Profile" in `intern_accounts` but exists in `applications` or `enrollments`, it automatically backfills `intern_accounts`.
   - Strict stage gating suppresses `needs_academic_profile` entirely for candidates in Stage 3, Stage 4, or Stage 5 (`if flow_state["stage_num"] >= 3: needs_academic_profile = False`).

3. **API Synchronization (`/intern/me`)**:
   - Updated `/intern/me` to return `"next_action": build_intern_next_action(flow_st, hours_logged)` and enriched `"flow_state"` payload (`has_paid_deposit`, `has_paid_balance`, `balance_due`, `days_since_joining`, `balance_grace_expired`).
   - Ensures client-side `renderNextActionMissionCard()` in `portal.html` receives the exact same payload as server-side Jinja, keeping UI 100% in sync across initial render and dynamic client updates.
   - Enforced case-insensitive email lookups (`LOWER(email)=LOWER(?)`) across `intern_me()`, preventing PostgreSQL casing mismatches from producing false 404 "Account not found" errors.

4. **Strict Mutually Exclusive Gating on `/portal/offer`**:
   - Refactored `apps/portal/templates/portal_offer_letter.html` to wrap `#postSignPaymentSection` in `{% if not is_deposit_verified %}`.
   - When a candidate's deposit is verified (`is_deposit_verified == True`), the Step 3 payment container (including the QR code image, 1-tap UPI launchers, and the UTR submission form) is completely excluded from the rendered DOM. The page renders exclusively the Verified Dossier Card (`#verifiedDossierCard`) and the "Download Official Signed PDF" button.
   - Auto-reconciliation in `portal_offer_page()`: If `enrollments` or `applications` has verified deposit/accepted status, `intern_offer_letters` is automatically upgraded to `caution_deposit_status = 'VERIFIED'` and `pdf_unlocked = 1`.

5. **Ghost Element Suppression (`#nextStepCard`)**:
   - Added `hidden` class to `#nextStepCard` by default.
   - Updated `renderOverview()` in `portal.html` so that `#nextStepCard` is only revealed for job-board applicants (`_status === '__JOB_ONLY__'`). For all standard internship lifecycle candidates (Stages 1 through 5), `#nextActionMissionCard` serves as the sole, unified mission container, eliminating all `👋 — —` ghost artifacts.

---

### 46.3. Verification & Live Production Audit
- **Local Automated Test Suite (`scripts/test_stage_synchronization.py`)**:
  - `test_build_intern_next_action_stages`: 100% PASS across all 5 lifecycle states.
  - `test_offer_letter_template_exclusivity`: 100% PASS (Step 3 payment form & QR 100% absent from DOM when verified).
  - `test_portal_template_stage_synchronization`: 100% PASS (Stage 5 renders without Stage 1 fallback or unhidden ghost cards).
- **Offer Letter Portal Test Suite (`apps/portal/tests/test_offer_letter_portal.py`)**:
  - 5/5 unit tests PASS in 0.71s.
- **Live Remote Production Verification (`ubuntu@3.26.237.171`)**:
  - Candidate `abhinav.sharma@dbert.vom` (ID `5624`):
    * Flow State: `stage_num=5`, `stage=CONFIRMED`, `label=Confirmed & Enrolled`.
    * `/portal` -> **HTTP 200** (Stage 5 Active Mission Card: **TRUE**, Stage 1 Fallback: **FALSE**, Visible Complete Profile Banner: **FALSE**, Unhidden Ghost Card: **FALSE**).
    * `/portal/offer` -> **HTTP 200** (Verified Dossier: **TRUE**, Download Signed PDF: **TRUE**, Step 3 Payment Form in DOM: **FALSE**, Step 3 QR in DOM: **FALSE**).
    * `/intern/me` -> **HTTP 200** (`next_action` badge: `"Stage 5: Sprint Active · Balance Completion Required"`, `flow_state` stage: `5`, `needs_academic_profile`: `False`).
  - Seeded Personas Audit:
    * `stage2_review@dbert.test`: Stage 2, `"Stage 2: Fast-Track Available"`.
    * `stage3_selected@dbert.test`: Stage 3, `"Stage 3: Selection & Appointment"`.
    * `stage4_pending@dbert.test`: Stage 4, `"Stage 4: Verification in Progress"`.
    * `stage5_enrolled@dbert.test`: Stage 5, `"Stage 5: Active Intern · Day 4 of 7-Day Window"`.
    * `stage5_grace_expired@dbert.test`: Stage 5, `"Stage 5: Sprint Active · Balance Completion Required"`.

---

## 47. Automated Payment Verification Voucher & Next Steps Roadmap Email upon Enrollment Approval

### 47.1. Architectural Overview & Problem Context
- **Operational Need**: Upon enrollment acceptance (`payment_status = 'Accepted'`), candidates require immediate financial proof of payment reconciliation (a formal Electronic Payment Verification Voucher / Receipt) and a clear, sequential next-steps roadmap guiding them through their multi-stage internship journey.
- **Dual Voucher Transmission**:
  1. **In-Body Executive Voucher Card**: Fully responsive, dark-slate (`#131926`) HTML table card rendering with institutional DBERT header, verified emerald badge (`✓ VERIFIED & ACCEPTED`), candidate metadata, and the recorded 12-digit UPI UTR in a prominent gold monospace box (`#FCD34D`).
  2. **Vector SVG Attachment**: Dispatched directly as an email attachment (`DBERT_Payment_Voucher_{utr}.svg`) using standard RFC-compliant `multipart/mixed` with `MIMEApplication`, allowing permanent offline archiving and printing.
  3. **1-Click Cryptographic Online Access**: A direct link to view and print the official vector SVG voucher at `https://lms.dbert.in/portal/receipt/utr_{utr}.receipt?token={sig}` secured via HMAC SHA256 (`_email_sig("receipt", utr)`).
- **Comprehensive 6-Milestone Next Steps Roadmap**:
  The email delivers a chronological, milestone-by-milestone lifecycle guide:
  - **Milestone 1 (Completed ✓)**: Admission Confirmed & Payment Reconciled on Sovereign Ledger.
  - **Milestone 2 (Action Required)**: Review & Digitally Sign Official Letter of Offer (`/portal/offer`).
  - **Milestone 3 (Week 1)**: Foundational 7-Day Sprint Curriculum & 24/7 AI Tutor Guidance (`/courses`).
  - **Milestone 4 (Ongoing)**: Social Bounties (50 Coins per article) & Ambassador Network (10% commission on peer enrollments) (`/tasks` & `/ambassador`).
  - **Milestone 5 (Weeks 2–8)**: 1:1 Faculty & Group Mentorship Booking via 14-day calendar (`/mentors/slots`).
  - **Milestone 6 (Day 60 · Graduation)**: 60-Day Capstone Milestone & ₹5,000 Stipend Release with AI pre-screening (`/stipend/tasks`).
  - **Milestone 7 (Executive Credential Dossier)**: Sovereign 3-Document Master Credential Packet (Certificate of Completion, Turnitin Academic Evaluation, LOR) indexed on `https://dbert.in/verify`.

### 47.2. Implementation & Integration Points
1. **Candidate-Facing Voucher Route (`GET /portal/receipt/<filename>`)**:
   - Location: `apps/portal/app.py`
   - Authorization:
     * Staff & Admin: Unrestricted access.
     * HMAC Token: Allows instant access if request carries `?token=...` matching `_email_sig("receipt", utr_digits)`.
     * Authenticated Intern: Allows access if the intern's session email matches the enrollment record.
     * Unauthenticated / Tampered: Returns 401 or redirects to `/signin?next=...`.
   - Response: Serves vector SVG with `Content-Type: image/svg+xml; charset=utf-8` and `Content-Disposition: inline`.
2. **Email Dispatch Pipeline (`send_enrollment_acceptance_dossier_email`)**:
   - Updates `_build_email_message` to support optional attachments (`attachments: list[tuple | dict] = None`), building RFC 5322 compliant `multipart/mixed` with `multipart/alternative` body and `MIMEApplication` attachment parts.
   - Updates `send_email_async` to pass attachments through `get_delivery_service().send_email()` with failover to direct raw SMTP (`_smtp_send_raw`).
   - Automatically dispatches high-priority push notification: `🏆 Enrollment Confirmed & Payment Verified`.
3. **Zero-Drop Approval Hooks**:
   - Wired directly into all 4 enrollment approval points:
     * `admin_enrollment_review` (`POST /admin/enrollment/review` where `action == 'accept'`)
     * `admin_enrollment_bulk_review` (`POST /admin/enrollment/bulk-review` where `action == 'accept'`)
     * `admin_enrollment_transition` (`POST /admin/enrollments/<id>/transition` where `nps == 'Accepted'`)
     * `admin_enrollment_edit` (`POST /admin/enrollment/edit` where `payment_status == 'Accepted'`)
     * Fallback router in `send_status_update_email` intercepts `STATUS_ACCEPTED` to automatically redirect to `send_enrollment_acceptance_dossier_email`.

### 47.3. Live Verification & Automated Test Suite
- **Deployment Script**: `scripts/deploy_acceptance_dossier_email_to_ec2.py`.
- **Automated Verification Script (`scripts/test_acceptance_dossier_email_on_ec2.py`)**:
  - `GET /portal/receipt/utr_666501928441.receipt?token={sig}` -> **HTTP 200 OK** (Content-Type: `image/svg+xml`, Valid SVG, UTR `666501928441` present).
  - Unauthenticated access without token -> **HTTP 401 Unauthorized**.
  - Access with invalid forged token -> **HTTP 401 Unauthorized**.
  - MIME builder unit test -> `MIMEMultipart('mixed')` with `alternative` text/html and `application/octet-stream` SVG attachment.
- **Persona Regression Probe (`scripts/test_persona_routes_on_ec2.py`)**:
  - 100% PASS across all 8 seeded personas (`mentor_staff`, `dbert_admin`, `fellow_enrolled`, `stipend_ready`, `stipend_wallet`, `stipend_gate1_locked`, `stage3_selected`, `offer_pending`).

---

## 48. DBERT QA Remediation Master Plan (Phases 0–5) & Production Hardening Governance

### 48.1. Architectural Overview & Problem Context
To eliminate critical operational bottlenecks, silent failures, payment edge cases, and background race conditions across the DBERT monorepo, the comprehensive QA Remediation Master Plan (`DBERT_QA_REMEDIATION_MASTER_PLAN.md`) was executed across six sequential execution phases (Phases 0 through 5).

The remediation resolved 12 baseline architectural defects (`BASE-01` to `BASE-12`) without breaking existing workflows across Next.js (`apps/website`) and Flask LMS (`apps/portal`):
1. **BASE-01 (Next.js Balance Sync Silent Failure)**: Next.js balance submission route `/api/enroll/balance` silently swallowed HTTP errors from the LMS sync endpoint, resulting in unrecorded candidate balances.
2. **BASE-02 (Outbox Concurrent Multi-Worker Race)**: `event_outbox` status query allowed concurrent Celery/Gunicorn workers to claim identical pending events simultaneously, triggering duplicate email and WhatsApp dispatches.
3. **BASE-03 (Direct Bypass of Private File Security via Nginx)**: Nginx configuration on `api.dbert.in` directly routed `/uploads/` to static disk, completely bypassing Flask LMS `FileSecurityService` access controls and HMAC validation.
4. **BASE-04 (Razorpay Raw Exception Stack Trace Leak)**: LMS `/api/payment/razorpay/create-order` returned raw exception strings to the browser on API or database failure.
5. **BASE-05 (SQLite Dialect Specificity in Payment Events)**: `payment_service.py` utilized SQLite-specific `INSERT OR REPLACE` syntax that failed on PostgreSQL deployments.
6. **BASE-06 (PostgreSQL Dead-Letter Case-Sensitivity in Readiness Check)**: `TelemetryService.check_readiness()` executed case-sensitive SQL status checks (`status = 'DEAD_LETTER'`), failing under lowercase PostgreSQL enum strings.
7. **BASE-07 (AI Pre-Screening Fail-Open Vulnerability)**: `stipend_evaluator.py` returned an auto-approved high score (85/100) when `GEMINI_API_KEY` was missing or empty, introducing financial risk.
8. **BASE-08 (Stipend Ledger Double Payout on Duplicate Webhooks)**: `coin_ledger_mirror` lacked idempotent transaction keys during stipend approval, allowing replay attacks or duplicate submissions to mint double rewards.
9. **BASE-09 (Application Endpoint IDOR and Cross-Tenant Data Leak)**: Intern application queries matched on unverified email strings, potentially exposing cross-tenant application data.
10. **BASE-10 (LMS Stage Desynchronization with Offer Status)**: Interns with accepted offers were incorrectly displayed Stage 1 ("Application Under Evaluation") on `/portal`.
11. **BASE-11 (Mutual Exclusivity Violation on Offer Letter View)**: Candidates who had already completed their caution deposit still saw the deposit payment form and QR code on `/portal/offer`.
12. **BASE-12 (Ghost Card & Complete Profile Banner on Advanced Stages)**: Advanced sprint fellows (Stages 3–5) were shown intrusive "Complete Academic Profile" banners and empty ghost cards.

---

### 48.2. Engineering Remediations & Technical Implementation

#### Phase 0: Baseline & Infrastructure Readiness
- **File**: `apps/portal/services/telemetry_service.py`
- Replaced dialect-sensitive status checks with `LOWER(status) = 'dead_letter'` and `LOWER(status) = 'pending'`.
- Validated that `/health` and `/ready` endpoints consistently return HTTP 200 on both SQLite and PostgreSQL.

#### Phase 1: Financial Integrity & Transaction Safety
- **Next.js Balance Sync Route (`apps/website/src/app/api/enroll/balance/route.ts`)**:
  * Implemented explicit validation of `syncRes.ok`.
  * If upstream LMS returns HTTP 4xx/5xx, the API immediately halts and returns HTTP 400 with actionable error payload: `{ error: 'LMS internal synchronization failed', upstreamStatus }`.
  * In case of upstream network timeout, safely flags the submission as `syncStatus: 'QUEUED_FOR_RECONCILIATION'` to prevent user transaction loss while alerting admins.
  * Enforced authorization header `Authorization: Bearer <INTERNAL_SYNC_SECRET>` with production environment validation.
- **Razorpay Order Creation (`apps/portal/routes/payment.py`)**:
  * Wrapped order generation in sanitized error handler returning generic user message: `"Unable to initiate payment transaction. Please contact admissions."`.
  * Retains detailed error logging server-side with structured error contexts.
- **Dialect-Portable Payment Events (`apps/portal/services/payment_service.py`)**:
  * Replaced `INSERT OR REPLACE` with portable existence check and conditional upsert:
    `SELECT id FROM payment_events WHERE event_id = ?`.
  * Updated `is_payment_processed()` to search both top-level `event_id` and payload JSON `order_id` / `payment_id`.
- **AI Pre-Screening Fail-Closed Policy (`apps/portal/services/ai/stipend_evaluator.py`)**:
  * Fixed fail-open bug. When `GEMINI_API_KEY` is missing, unconfigured, or throws API exceptions, the evaluator returns:
    `score: None`, `status: "AI_UNCONFIGURED_MANUAL_REVIEW"`, `verdict: "AWAITING_MANUAL_REVIEW"`, `reason: "AI evaluation unavailable; routed to human staff review queue"`.
  * Halts automatic coin credit or stipend release until verified by an authorized human staff member.
- **Stipend Ledger Idempotency Keying (`apps/portal/app.py`)**:
  * Introduced deterministic idempotency key for stipend milestone credits:
    `idem = f"stipend_reward_{submission_id}"`
  * Introduced deterministic idempotency key for task review credits:
    `idem_key = f"task_reward_{ref_id}"`
  * Checks existing ledger entries via `SELECT 1 FROM coin_ledger_mirror WHERE idem_key = ?` before any balance insertion, preventing duplicate payouts.

#### Phase 2: Identity, Authorization & Private File Access
- **Nginx Private File Security (`deploy/dbert-unified-nginx.conf`)**:
  * Removed static alias `location /uploads/ { alias ...; }` from `api.dbert.in`.
  * Proxied all `/uploads/` requests to `http://127.0.0.1:5001/uploads/` via Gunicorn.
  * Enforces `FileSecurityService.authorize_file_access()`: requires valid HMAC signature (`?sig=...`), authenticated intern session ownership, or admin/staff role.
- **Intern Application Scoping (`apps/portal/routes/applications.py`)**:
  * Hardened query to strictly bind to authenticated session `intern_id`:
    `WHERE (pa.intern_id = ? AND (pa.email IS NULL OR LOWER(pa.email) = LOWER(?))) OR (pa.intern_id IS NULL AND LOWER(pa.email) = LOWER(?))`
  * Completely eliminates cross-account application visibility.

#### Phase 3: Background Processing & Outbox Concurrency
- **Atomic Batch Claiming (`apps/portal/services/outbox_service.py`)**:
  * Added `STATUS_PROCESSING = "PROCESSING"`.
  * Added schema columns `locked_by TEXT` and `lock_expires_at TEXT` to `event_outbox` with automated startup migration in `app.py`.
  * Implemented `claim_outbox_batch(conn, worker_id, limit, lease_seconds)`: selects pending events and atomically claims them with an expiration lease, preventing double worker dispatch.
  * Implemented `reclaim_expired_leases(conn)`: automatically resets orphaned events whose `lock_expires_at < current_timestamp` back to `PENDING`.
  * Updated `mark_event_sent` and `mark_event_failed` to clear locks on completion.

#### Phase 4 & 5: Automated Regression Testing & Verification Gates
- **Automated Regression Suite (`apps/portal/tests/test_qa_remediation_suite.py`)**:
  * 9 comprehensive regression test cases covering all remediation areas:
    1. `test_outbox_atomic_worker_claim_and_recovery`: Validates worker isolation and lease recovery.
    2. `test_stipend_ledger_idempotency_prevents_duplicate_credits`: Validates idempotency rejection.
    3. `test_ai_evaluator_fail_closed_when_unconfigured`: Validates fail-closed behavior when AI key is missing.
    4. `test_payment_event_portable_upsert`: Validates dialect-portable payment event storage and deduplication.
    5. `test_private_file_access_requires_auth_or_hmac`: Validates 401 on unauthenticated private file access.
    6. `test_private_file_path_traversal_blocked`: Validates that path traversal attacks (`../`) are safely rejected with 404/403.
    7. `test_stage_next_action_synchronization_with_accepted_offer`: Validates that Stage 3+ interns see appropriate mission guidance.
    8. `test_offer_letter_template_mutual_exclusivity`: Validates that verified caution deposit suppresses payment QR and UTR form.
    9. `test_academic_profile_suppressed_for_advanced_stages`: Validates that advanced interns do not see profile completion warnings.
  * Test execution result: **9/9 PASS (100%)** in 0.129s.
- **Monorepo Build Verification**:
  * Next.js standalone build: `npm --prefix apps/website run build` passed with 297/297 pages generated and 0 TypeScript errors.
  * Master plan gates `Gate 0` through `Gate 5` marked **CLOSED**.

---

## 14. LMS Dead-End Remediation, Sovereign Leaderboard & Dual-Tier Certificates (`/leaderboard`, `/certificates`)

### 14.1. Lifecycle State Machine Hardening & Profile Desynchronization Remediation
- **Problem Remediated**: Candidates holding an accepted, digitally signed, and deposit-verified appointment letter (e.g. `DBERT-OFR-2026-FSD-5166` on `/portal/offer`) previously displayed *"Action Required: Complete Your Academic Profile"* and fell back to *"Stage 1: Under Evaluation"* on `/portal`.
- **Root Cause & Structural Fixes**:
  1. **Gunicorn In-Memory Process Desync**: `dbert-portal.service` on production EC2 was running stale in-memory workers loaded prior to previous logic deployments. Automated restart added to all future portal deployment scripts.
  2. **Stage Elevation via Offer Letter (`get_intern_flow_state`)**:
     * Stage 5 (`is_confirmed`): Explicitly elevated if `offer_row` has `signature_name` AND (`caution_deposit_status == 'VERIFIED'` OR `pdf_unlocked == 1`).
     * Stage 3 (`is_selected`): Explicitly elevated if `offer_row` has `offer_letter_id`, preventing unverified offer holders from ever falling into Stage 1.
  3. **Academic Profile Auto-Healing & Banner Suppression**:
     * In `portal_page()` and `/intern/me`: Candidate college, course, and domain are auto-synced into `intern_accounts` from `intern_offer_letters`.
     * `needs_academic_profile` is forced to `False` across both Jinja context and client-side JavaScript (`renderOverview`) whenever `flow_state.stage_num >= 3`.

### 14.2. Sovereign Multidimensional Leaderboard Engine (`/leaderboard`)
- **Route**: `https://lms.dbert.in/leaderboard` (Eliminates 404).
- **Backend Scoring Engine (`_tutor_leaderboard`)**:
  * Calculates real-time composite competency via 7 activity metrics within the 8-week cohort tenure window (capped at 80.0 hours):
    $$\text{Score} = 100 \times \text{certs} + 50 \times \text{tasks} + 25 \times \text{lessons} + 5 \times \min(\text{tenure\_hours}, 80.0) + 100 \times \text{articles} + 5 \times \text{quizzes} + 5 \times \text{concepts}$$
- **UI/UX Architecture (`apps/portal/templates/leaderboard.html`)**:
  * **Domain Filtering Pills**: Fast domain-level sorting across All Domains, AI Agent Development, Data Analyst, Full Stack Development, Python Automation, Cybersecurity, and DevOps & Cloud.
  * **Top 3 Podium Cards**: Luxury metallic styling for 1st (Gold 🥇), 2nd (Silver 🥈), and 3rd (Bronze 🥉).
  * **Remaining Standings (Ranks 4–50)**: Table view with sprint hours, approved bounties, completed lessons, and mastered concepts.
  * **Sticky Personal Standing Card**: Highlights the logged-in intern's live rank, total points, sprint hours, and next milestone.
  * **Expandable Scoring Methodology Card (`#rubricCard`)**:
    - Clean accordion header with `#rubricHeader` and `#toggleRubricBtn` (`View Scoring Rules` / `Hide Scoring Rules`).
    - Collapsed by default (`display: none;`) to keep focus on top rankings, expanding smoothly on click with a rotating chevron indicator.
    - Displays detailed 7-dimension scoring badge breakdown with hover interactions:
      * Verified Certification: `+100 pts`
      * Approved Bounty Task: `+50 pts`
      * Completed Sprint Lesson: `+25 pts`
      * Platform Sprint Attendance (Max 80 hrs): `+5 pts/hr`
      * Published Engineering Article: `+100 pts`
      * 100% Score on Daily Quiz: `+5 pts`
      * Mastered Technical Concept: `+5 pts`
    - Strict nonce CSP compliance: zero inline `onclick`, event listeners programmatically bound in `DOMContentLoaded`.

### 14.3. Sovereign Dual-Tier Certificates Portal (`/certificates`)
- **Route**: `https://lms.dbert.in/certificates` (Eliminates 404).
- **Dual-Tier Credential Architecture (`apps/portal/templates/certificates.html`)**:
  * **Tier 1: Pre-Vetted Engineers (Verified · Ready to Hire)** (e.g. `CERT-DBERT-2026-FSD-156`):
    - Full 3-document credential dossier (Certificate of Completion, Turnitin Academic Project Evaluation, Letter of Recommendation).
    - 1-Click Master PDF vector print (`/portal/certificate/{cert_id}/print`) and public verification deep-link (`https://dbert.in/verify/{cert_id}`).
  * **Tier 2: Incubation Fellows In-Sprints (383 Candidates)** (e.g. Gaurav Giri `CERT-DBERT-2026-DA-108`, Gun Soni `CERT-DBERT-2026-AIML-078`, K Tejaswi):
    - High-merit evaluation score badge (e.g. `88/100 · Grade A+ (Outstanding)`).
    - Provisional sprint milestone card with watermarked preview.
    - **Credential Verification Gateway Card**:
      * Option 1: Fast-track unlock via ₹299 Project Verification Fee (`https://dbert.in/enroll/1999?certid={certId}&fee=299`).
      * Option 2: Full fellowship completion via ₹1,500 Incubation Balance (`https://dbert.in/enroll/1999?certid={certId}`).
      * 1-Click direct routing to WhatsApp Admissions Concierge (`+91 81929 11360`).
  * **Section 2: LMS Course Micro-Certifications**:
    - Auto-heals and renders certificates for all completed LMS courses (`intern_certificates` where `course_id IS NOT NULL`).
    - Direct "View & Print" and "Verify Authenticity" action buttons.

### 14.4. Universal Web Push Notification Approval Modal
- **Infrastructure**: Native RFC 8292 NIST P-256 VAPID push engine (`web_push_service.py`), client controller (`dbert-push-client.js`), and PostgreSQL storage (`web_push_devices`).
- **Modal Engagement (`#dbertPushPermissionModal`)**:
  * Automatically prompts interns on `/portal` when `Notification.permission === 'default'`.
  * Communicates direct user value: real-time mentor code review notifications, bounty task approvals, and ₹5,000 stipend release confirmations.
  * Direct 1-click subscription registration via `DBERTPush.requestPermissionAndSubscribe()` with 24-hour dismissal cooldown support.
- **Dual-State Dynamic Prompt & Blocked Address Bar Guide**:
  * **State 1 (`#pushModalStateDefault`)**: Standard value proposition card for `Notification.permission === 'default'`.
  * **State 2 (`#pushModalStateBlocked`)**: Triggered when `Notification.permission === 'denied'` or when a candidate selects "Block" in the browser prompt. Displays a 3-step actionable visual guide directing the intern to the browser address bar Lock 🔒 / Tune 🎛️ icon to change Notifications to "Allow", paired with a 1-click "I've Enabled It — Refresh Page" button (`#dbertPushReloadBtn`).
- **Persistent Dashboard Alert Banner (`#pushBlockedBanner`)**:
  * Rendered at the top of `#panel-overview` above `#nextActionMissionCard` whenever browser notifications are blocked.
  * Warns interns that they will miss ₹5,000 stipend release alerts and mentor code reviews, with an "Unblock Notifications" trigger to open the guidance modal.
- **Real-Time Live Recovery Engine (`navigator.permissions.query`)**:
  * Continuously monitors permission changes via W3C Permissions API. When an intern toggles notifications to "Allow" in site settings, the system immediately detects `'granted'`, auto-dismisses the modal and banner, auto-subscribes the device via `DBERTPush.autoSubscribe()`, and displays a real-time success toast without requiring a manual refresh.
- **Anti-Overlap & Stacking Architecture**:
  * Elevated `z-index: 100001` with `backdrop-filter: blur(8px)` and `rgba(0, 0, 0, 0.82)` overlay spanning the entire viewport.
  * Responsive desktop offset: `@media (min-width: 821px)` applies `padding-left: calc(var(--portal-sidebar, 260px) + 24px)` and `padding-right: 24px`, ensuring the card is centered directly in the active main content workspace with guaranteed 60px–140px clearance from the fixed sidebar.
  * Mobile resilience: `@media (max-width: 820px)` centers card across the mobile screen with 16px padding.
  * Vertical scroll safety: `overflow-y: auto` on overlay and card prevents clipping of action buttons on short laptop screens.

### 14.5. Seeded Test Personas & Verification Matrix
The following accounts are permanently provisioned on production PostgreSQL (`dbert_lms`):

| Stage # | Lifecycle State | Seeded Email | Password | Key Characteristics & Expected Behavior |
|:---:|---|---|---|---|
| **Stage 1** | Application Required | `stage1_apply@dbert.test` | `TestPass123!` | Incomplete application; shows "Complete Academic Profile" banner and domain track selection. |
| **Stage 2** | Under Review | `stage2_review@dbert.test` | `TestPass123!` | Application submitted; awaiting Technical Council review; shows WhatsApp expedite CTA. |
| **Stage 3** | Selected (Deposit Due) | `stage3_selected@dbert.test` | `TestPass123!` | Admin approved; appointment letter issued; requires ₹499 caution deposit to confirm seat. |
| **Stage 4** | Payment Pending | `stage4_pending@dbert.test` | `TestPass123!` | ₹499 UTR submitted; under accounts desk reconciliation; seat confirmation pending. |
| **Stage 5** | Confirmed Fellow (Sprint Active) | `fellow_enrolled@dbert.test` | `TestPass123!` | ₹499 deposit verified; sprint workspace unlocked; 7-day balance window active. |
| **Stage 5** | Grace Expired (Needs Balance) | `stage5_grace_expired@dbert.test` | `TestPass123!` | Sprints active; orientation ended; prompts ₹1,500 balance completion to unlock credentials. |
| **Stage 5** | Fully Paid Incubation Fellow | `fellow_paid_1999@dbert.test` | `TestPass123!` | ₹1,999 fully paid; all sprint modules, verified credentials, and stipend unlocked. |
| **Active** | Signed Offer Holder (User Reported) | `abhinav.sharma@dbert.vom` | `TestPass123!` | Offer `DBERT-OFR-2026-FSD-5166` signed & verified; sprint workspace active. |
| **Stipend** | 5,000 Coins in Wallet | `stipend_wallet@dbert.test` | `TestPass123!` | Completed milestones; 5,000 coins credited; withdrawable to encrypted UPI. |
| **Provisional** | 383 Fellow Persona (Gun Soni) | `gun.soni.test@dbert.test` | `TestPass123!` | In Sprints; score 88/100; shows course certificates + ₹299 upgrade card on `/certificates`. |

---

---

## 15. Domain Funnel Auto-Resolution & Unified Dashboard Architecture

### 15.1. Canonical Domain Normalization Engine
- **Master Tracks**: Exactly 9 canonical domains in `VALID_DOMAINS`:
  `AI Agent Development`, `Data Analyst`, `Full Stack Development`, `Python Automation`, `UI/UX Design`, `DevOps & Cloud`, `Mobile App Development`, `Cybersecurity`, `Digital Marketing`.
- **Normalization Engine (`normalize_domain_string(raw_domain)`)**:
  Maps all non-canonical entries from external Google Sheets, Typeform funnels, candidate inputs, and legacy abbreviations:
  * `"Data Analytics"`, `"data-analytics"`, `"data science"`, `"da"` &rarr; `"Data Analyst"`
  * `"Full Stack Web Development"`, `"web development"`, `"fsd"`, `"full-stack"` &rarr; `"Full Stack Development"`
  * `"AI & Machine Learning"`, `"aiml"`, `"ai-agent"` &rarr; `"AI Agent Development"`
  * `"Python Developer"`, `"python"`, `"pa"` &rarr; `"Python Automation"`
  * `"UI/UX"`, `"ui design"`, `"figma"` &rarr; `"UI/UX Design"`
  * `"DevOps"`, `"cloud computing"` &rarr; `"DevOps & Cloud"`
  * `"Android"`, `"flutter"`, `"mobile"` &rarr; `"Mobile App Development"`

### 15.2. Multi-Table Auto-Healing & Auto-Enrollment
- **Automatic Sync (`get_intern_flow_state()` & `portal_page()`)**:
  When an intern logs in or accesses `/portal`, the system inspects linked records across `intern_accounts`, `applications`, `enrollments`, `intern_offer_letters`, and `intern_certificates`.
  * Normalizes the candidate's domain string.
  * Auto-updates `intern_accounts.domain` in PostgreSQL.
  * Automatically enrolls the intern into domain-specific courses via `auto_enroll_intern_in_domain_courses()`.
  * Auto-heals missing college and course from linked records.

### 15.3. Dashboard Stacked Visual Hierarchy (`/portal`)
The Overview dashboard (`#panel-overview`) enforces a strict, clean vertical layout:
1. **Top**: `#nextActionMissionCard` (Immediate next action mission card: Stage badge, weekly attendance hours vs 10h target, and 3 high-contrast action CTAs).
2. **Directly Below**: `#academicProfileBanner` (Onboarding Step 1: Academic Background & Domain Verification with real-time status chips for College, Course, and Domain). Automatically hidden when all profile fields are completed.
3. **Directly Below**: `#overviewStepBar` (Unhidden 8-Week Milestone Roadmap from Week 1 Induction to Week 8 Graduation).
4. **Directly Below**: `#ovAccepted` (Full legacy active dashboard including Bounty Accelerator 200 coins, Guided Learning Workspace, Cognitive Progress & Mastery, Micro-Tasks & Reward Coins, Learning Analytics, AI Directives, Weekly Attendance Hub with 10h target & audit log, Enrollment Profile, and Recommended Internships).
5. **Suppression of Duplicate Banners**: Cleaned up redundant JavaScript injection of `ovBalanceGraceBanner` since `#nextActionMissionCard` officially renders the Stage 5 balance message at the top.

### 15.4. Fallback 1-Click Domain Confirmation Modal
- **Modal Component (`#domainSelectionModal`)**:
  For interns who have no domain record across any linked table upon login, a sleek modal prompts them to choose one of the 9 canonical tracks in a single click.
- **API Endpoint (`POST /api/intern/select-domain`)**:
  Validates track via `normalize_domain_string()`, updates `intern_accounts.domain`, `applications.domain`, and `enrollments.domain`, auto-enrolls into domain courses, and returns `{ "status": "success", "domain": "..." }`.

---

## 16. Staged Offer Letter Review, Transparent Watermark & Seat Confirmation Flow (`/portal/offer`)

### 16.1. Staged 2-Screen User Journey Architecture
To prevent cognitive overload and maintain strict legal compliance under the Indian IT Act, 2000, `/portal/offer` divides the appointment onboarding flow into two distinct visual screens:
1. **Screen 1 (`#screenOfferReview`) — Appointment Letter Review**:
   - High-fidelity parchment rendering of the full official appointment terms, weekly 10h commitments, sprint deliverables, and ₹5,000 milestone stipend provisions.
   - **Delicate & Transparent Watermark**: Faint amber styling (`background: rgba(254, 243, 199, 0.10)`, `border: 2.5px dashed rgba(217, 119, 6, 0.22)`, `color: rgba(180, 83, 9, 0.20)`, zero `backdrop-filter` blur) ensures 100% legibility of all terms underneath while retaining the unverified preview watermark stamp.
   - **Review Completion Bar**: Pinned at the bottom of the letter with a prominent CTA button: `Accept & Sign Offer Letter →` (`#btnAcceptAndSignBottom`), which smoothly transitions candidate to Screen 2.
2. **Screen 2 (`#screenActionSteps`) — Digital Execution & Seat Confirmation**:
   - **Top Navigation Bar**: Provides instant `← Review Appointment Letter` back button and candidate reference chips (`REF: {{ offer.offer_letter_id }}`, `Track: {{ offer.domain }}`).
   - **Step 2 (Digital Acceptance)**:
     * Unsigned: Renders `STEP 2: REVIEW & DIGITAL ACCEPTANCE` with Full Legal Name input, statutory agreement checkbox, and `Sign & Accept Appointment Agreement` button.
     * Signed: Renders `STEP 2 COMPLETED: AGREEMENT EXECUTED` green banner with verified signature name, execution timestamp, and `Legally Accepted` badge.
   - **Step 3 (Cohort Seat Confirmation)**:
     * **Compact QR Code**: Scaled down to a sleek **115px × 115px** with `Download QR` button and Merchant VPA (`Q652429146@ybl`) with 1-click `Copy UPI ID`.
     * **Vibrant Brand 1-Tap UPI Launchers**: High-contrast, non-blending buttons with distinct brand styling:
       - **GPay**: Pure White (`#ffffff`), border `2px solid #4285F4`, Google blue icon (`#4285F4`).
       - **PhonePe**: Vibrant Royal Purple (`#5f259f`), border `2px solid #c084fc`, white text (`#ffffff`).
       - **Paytm**: Electric Paytm Sky Blue (`#00baf2`), border `2px solid #ffffff`, deep navy text (`#002970`), high-contrast against dark card background.
       - **Any UPI**: Radiant Amber/Gold gradient (`linear-gradient(135deg, #f59e0b 0%, #d97706 100%)`), border `2px solid #fde68a`, dark text (`#0b1120`).
     * **UTR Submission & Reconciliation Card**: 12-digit numeric validation (`\d{12}`), admissions ledger submission, and under-review state with 1-tap WhatsApp expedite button.
3. **Screen 3 / Reconciled State (`is_deposit_verified: True`)**:
   - Stepper displays all 3 steps completed.
   - Preview watermark is eliminated; candidate legal cursive signature and cryptographic QR seal are embedded.
   - Official signed PDF download button (`#btnPrintOfferTop`, `#btnPrintOfferDossier`) is unlocked, directing to `/portal/offer/print`.

### 16.2. Smart Screen Routing & Stepper Navigation
- **Initial Landing Logic**:
  * `is_signed: False` &rarr; Lands on Screen 1 (Review) with transparent watermark.
  * `is_signed: True`, `is_deposit_verified: False` &rarr; Lands directly on Screen 2 (Action Steps: Step 2 Executed + Step 3 Payment) to minimize friction.
  * `is_deposit_verified: True` &rarr; Lands on Screen 1 (Verified Document with Download PDF unlocked).
- **Interactive Stepper Switcher**:
  Clicking Step 1 on `#stepperStep1` toggles to Screen 1. Clicking Step 2 (`#stepperStep2`) or Step 3 (`#stepperStep3`) toggles to Screen 2.

### 16.3. Strict Nonce CSP Event Binding & Zero-Inline-Handler Enforcement
- **CSP Nonce Requirement**: Under `Content-Security-Policy: script-src 'self' 'nonce-{nonce}'`, modern browsers drop all inline `onclick="..."` and pseudo-URLs (`href="javascript:void(0)"`).
- **Semantic Button Architecture**: All action controls use `<button type="button">` instead of anchors with void hrefs.
- **Zero Inline Event Handlers**: Exactly 0 inline `onclick` attributes remain across the template.
- **Programmatic Event Registrations**: All listeners are registered inside `DOMContentLoaded` within `<script nonce="{{ csp_nonce() }}">`:
  * `#btnReviewSignTop`: switches to Screen 2 (`showScreen('screenActionSteps')`).
  * `#btnConfirmSeatTop`: switches to Screen 2 (`showScreen('screenActionSteps')`).
  * `#btnAcceptAndSignBottom`: switches to Screen 2 (`showScreen('screenActionSteps')`).
  * `#btnBackToReview`: switches back to Screen 1 (`showScreen('screenOfferReview')`).
  * `#stepperStep1`: switches to Screen 1.
  * `#stepperStep2` & `#stepperStep3`: switches to Screen 2.
  * `#copyVpaBtn`: 1-click clipboard copy (`copyUpiVpa('Q652429146@ybl')`) with visual checkmark and toast notification.
  * `#btnPrintOfferTop` & `#btnPrintOfferDossier`: opens `/portal/offer/print` in new tab.
- **Academic Profile Route Forwarding (Option B)**:
  Route `/profile` dynamically redirects via HTTP 302 to `/portal?tab=editprofile`, ensuring candidates who click profile links seamlessly access academic background completion without broken or disconnected pages.

---

## 17. Cohort Engineering Leaderboard Architecture & Weightage Governance (`/leaderboard`)

### 17.1. Route & Component Architecture
- **Route**: `https://lms.dbert.in/leaderboard` (Managed by Flask route handler `_tutor_leaderboard()` in `apps/portal/app.py`).
- **Template**: `apps/portal/templates/leaderboard.html`.
- **UI Structure**:
  * Top Header with Trophy icon and cohort description.
  * Personal Standing Card (`.standing-card`) with rank, points, sprint hours, bounty count, and cert count.
  * Domain Filter Pills (`.domain-tabs-wrapper`) across canonical domains.
  * Top 3 Podium Cards (`.podium-card.rank-1`, `.rank-2`, `.rank-3`) with gold, silver, bronze medal styling.
  * Top 50 Standings Table (`.table-card` and `.lb-table`) with rank, avatar, name, domain tag, hours, bounties, lessons, concepts, and total score.
  * Multidimensional Scoring Methodology Card (`.rubric-card`) with color-coded rubric badges.

### 17.2. 8-Week Cohort Tenure Window Protocol
1. **Tenure Duration**: All DBERT internship cohorts operate on a strict **8-Week (56 calendar days)** cohort tenure.
2. **Start Date Resolution**:
   - Primary: Candidate's recorded `enrollments.joining_date`.
   - Secondary: Candidate's offer letter `intern_offer_letters.batch_start_date`.
   - Fallback: Earliest recorded attendance record `MIN(attendance.week_start)` for the candidate.
3. **Window Boundary**:
   $$\text{tenure\_window} = [\text{start\_date}, \text{start\_date} + 56\text{ days}]$$
4. **Attendance Exclusion**: Any attendance record whose `week_start` falls outside this 56-day window is strictly excluded from ranking calculations.

### 17.3. 80-Hour Attendance Points Cap
- Standard engagement across the 8-week cohort is **10 hours/week**, totaling an expected **80.0 hours**.
- **Display vs Calculation**:
  - The leaderboard table displays the candidate's actual logged hours within their tenure window (e.g., `104.0 hrs`).
  - For total point calculation, attendance hours are capped at 80.0 hours:
    $$\text{points}_{\text{attendance}} = \min(\text{tenure\_hours}, 80.0) \times 5.0\text{ pts}$$
    (Maximum possible contribution from attendance is **400.0 pts**).

### 17.4. Multidimensional Competency Scoring Weightage (7 Core Metrics)
The total score for each candidate is calculated using the updated weightage formula:
$$\text{Score} = 100 \times \text{certs} + 50 \times \text{tasks} + 25 \times \text{lessons} + 5 \times \min(\text{tenure\_hours}, 80.0) + 100 \times \text{articles} + 5 \times \text{quizzes} + 5 \times \text{concepts}$$

| Metric | Point Weightage | Verification & Source Criteria | Rubric Badge |
|---|:---:|---|---|
| **Verified Certification** | **+100 pts** | Completed credential in `intern_certificates` where `tier != 'provisional'` | `.badge-gold` |
| **Approved Bounty Task** | **+50 pts** | Staff-approved task submission in `task_submissions` (`status = 'approved'`) | `.badge-green` |
| **Completed Sprint Lesson** | **+25 pts** | Course lesson marked complete in `user_progress` | `.badge-cyan` |
| **Platform Sprint Attendance** | **+5 pts/hr** | Logged sprint attendance within 8-week tenure window (capped at max 80.0 hrs) | `.badge-indigo` |
| **Published Engineering Article**| **+100 pts** | Peer-reviewed and published technical article (`approved_articles`) | `.badge-blue` |
| **100% Score on Daily Quiz** | **+5 pts** | Quiz attempt scored at 100% in `quiz_attempts` | `.badge-purple` |
| **Mastered Technical Concept** | **+5 pts** | Concept marked mastered in `concept_mastery` | `.badge-rose` |

### 17.5. Spacing & Typography Hardening
- **Container Padding**: Increased `.leaderboard-container` padding to `2rem 2rem 4rem` (desktop) and `4.5rem 1.25rem 4rem` (mobile).
- **Card Header Component**: Replaced inline styles with `.table-card-header` class with `padding: 1.5rem 2rem;` (desktop) and `padding: 1.25rem 1.25rem;` (mobile).
- **Anti-Clipping Design**: Table heading `"Leaderboard Standings (Top 50)"` and candidate count `"Showing 50 ranked candidates in All"` have ample margin and flex spacing, preventing any glyph clipping of leading characters ("L" and "S") against the card border or sidebar.

---

## 18. Staged Offer Review, Signature-First Gating & Luxury Dark Seat Confirmation (`/portal/offer`)

### 18.1. Screen Segregation & Strict Gating Architecture
- **Screen 1 (`#screenOfferReview`)**: Official Appointment Letter reading view with legal terms, responsibilities, stipends, and dual navigation CTAs.
- **Screen 2 (`#screenActionSteps`)**:
  - **For Unsigned Candidates (`is_signed == False`)**:
    * Jinja strictly compiles ONLY `#offerSignCard` (Step 2: Review & Digital Acceptance).
    * `#signedBanner` ("STEP 2 COMPLETED: AGREEMENT EXECUTED / Signed by None on None") and `#postSignPaymentSection` ("STEP 3: COHORT SEAT CONFIRMATION") are physically omitted from HTML compilation via a strict `{% if is_signed %}` server gate.
    * Zero possibility of leaking empty signature names or rendering Step 3 before digital agreement execution.
  - **For Executed Candidates (`is_signed == True`)**:
    * Jinja strictly compiles `#signedBanner` (displaying actual signature name and execution timestamp recorded under Indian IT Act, 2000) and `#postSignPaymentSection` (Step 3: Cohort Seat Confirmation).
    * `#offerSignCard` is physically omitted from HTML compilation.
- **Digital Execution Transition Protocol**:
  * When candidate signs, AJAX POST to `/portal/offer/sign` commits signature to database and returns `{ status: "success" }`.
  * JavaScript displays toast: `"Appointment Agreement Digitally Signed! Loading Cohort Seat Confirmation..."` and triggers `window.location.reload()`.
  * Upon reload, `is_signed` evaluates `True`, automatically revealing Screen 2 with the Executed Banner and Step 3 Payment/UTR.

### 18.2. Step 3 UI/UX Design System Parity (`/enroll/1999` Standard)
- **Left Card (Scan & Pay ₹499 + Mobile 1-Tap Fast Pay)**:
  * Container: `background: #0B0F17; border: 1px solid #2A364B; border-radius: 12px; padding: 22px;`.
  * White QR Box: `130px × 130px` high-contrast wrapper (`background: #FFFFFF; padding: 12px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.6)`).
  * High-Res Download Button: `background: transparent; color: #E2B96F; border: 1px solid rgba(226, 185, 111, 0.4)`.
  * Merchant VPA Pill: `background: #141A23; border: 1px solid #1E2633; color: #F0F4F8;` monospace with copy button (`color: #38BDF8; font-weight: 700`).
  * 1-Tap Mobile UPI Intent Launchers (2x2 Grid):
    - Google Pay: `background: #1A73E8; color: #FFFFFF !important; font-weight: 800;`
    - PhonePe: `background: #5F259F; color: #FFFFFF !important; font-weight: 800;`
    - Paytm: `background: #00BAF2; color: #FFFFFF !important; font-weight: 800;`
    - Any UPI: `background: #10B981; color: #FFFFFF !important; font-weight: 800;`
- **Right Card (12-Digit Bank UTR Entry Form)**:
  * Container: `background: #0B0F17; border: 1px solid #2A364B; border-radius: 12px; padding: 22px;`.
  * Heading: `#F0F4F8`, description `#8A9AB5`.
  * UTR input: `background: #080C14; border: 1.5px solid #2A364B; color: #F0F4F8; font-family: monospace; letter-spacing: 1.5px;`.
  * Submit button: `background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%); color: #0b1120 !important; font-weight: 900;`.
  * Footer note: `border-top: 1px solid #1E2633; color: #8A9AB5; font-size: 12px;`.

---

## 19. Web Push Notification Architecture, Self-Test Endpoint & Telemetry Pipeline (`/account/notifications`)

### 19.1. Architectural Scope & Endpoint Routing
- **Active Endpoints**:
  * `@app.route("/api/push/test", methods=["POST"])` (Primary self-test endpoint)
  * `@app.route("/api/push/broadcast", methods=["POST"])` (Backward-compatible alias for legacy or cached clients)
- **Strict Role & Tenant Gating**:
  * Dispatches exclusively to the authenticated intern (`current_intern()`) or staff (`current_staff()`).
  * Unauthenticated requests are rejected with `401 Unauthorized` (`{"status": "error", "message": "Authentication required."}`).
  * Eliminates mass broadcast vulnerabilities: Student self-test triggers target ONLY the caller's active device(s) (`event_name="self_test"`). Mass cohort broadcasts remain strictly reserved for `/admin/push-broadcast`.
- **CSRF Protection**:
  * Validates session `_csrf` against `X-CSRF-Token` / `X-CSRFToken` request headers.

### 19.2. Cryptographic VAPID Delivery & Zero Silent Fails
- **RFC 8292 NIST P-256 Protocol**:
  * Payload signed by `VapidManager` and encrypted via `pywebpush.webpush()` with client `p256dh` and `auth` credentials.
- **Delivery Telemetry & Last-Pushed Audit**:
  * On delivery (HTTP 201 Created from Google/Chrome FCM or Mozilla autopush):
    - Updates `last_pushed_at = CURRENT_TIMESTAMP` in `dbert_internship.web_push_devices`.
    - Atomically inserts audit record into `dbert_internship.web_push_delivery_logs` with `delivery_status='DELIVERED'`, `status_code=201`.
  * Dual-syncs with in-app notifications inbox in `notifications` table (`sync_inapp=True`).

### 19.3. Frontend UX Hardening (`account_notifications.html`)
- **Button State & Spinner**:
  * `#btnTestPush` disables on click and shows `<i class="fa-solid fa-spinner fa-spin"></i> Sending Alert...` during network roundtrip.
- **Toast & DOM Feedback**:
  * On 200 JSON success: Displays green toast (`✓ Push notification dispatched to your registered device!`) and immediately updates the "Last Pushed" table column from "None" / "Never" to bold green "Just now".
  * On error: Displays red toast with exact error message from server.
- **Fallback Notification**:
  * Uses verified logo asset `/static/img/dbert-logo-192.png`.
  * Handles click event via `onclick = () => window.focus()` to seamlessly bring browser tab to foreground.
- **Nonce CSP Compliance**:
  * Zero inline `onclick` or pseudo-URL handlers. Bound programmatically via `addEventListener`.

---

---

## 20. Admin Enrollment Payment Review Pipeline, Synchronous Lifecycle Orchestration & Robust Action Delegation (`/admin`)

### 20.1. Architectural Scope & Root Cause Remediation
- **Identified Failure Mode**:
  On `https://lms.dbert.in/admin`, clicking **"Accept Payment"** or **"Reject"** in the enrollment review modal (`enrModal`) previously resulted in no action or visual response.
  * *Root Cause 1 (Omitted ID Argument)*: In `apps/portal/templates/admin.html`, table row rendering under the payment proof column called `viewScreenshot` with only 3 arguments `[r.payment_screenshot, r.name, r.utr||'']`, completely omitting `r.id`.
  * *Root Cause 2 (Null State Trap)*: `viewScreenshot` never initialized `_currentEnrId`. In `reviewEnrollment(action)`, `if (!_currentEnrId) return;` silently exited with zero feedback or network activity.
  * *Root Cause 3 (Missing Loading States)*: Modal buttons lacked spinner feedback and disabled attributes during execution, allowing repeated or silent clicks.
  * *Root Cause 4 (Database Sync Deficit)*: `admin_enrollment_review` updated `enrollments` and `applications`, but omitted updating `intern_offer_letters.caution_deposit_status` (`'VERIFIED'` / `'REJECTED'`), `pdf_unlocked`, and `intern_accounts.is_active`.

### 20.2. Frontend UI/UX & Delegated Actions Hardening (`admin.html`)
- **Argument Alignment**:
  * Table row render now passes `r.id` as the primary argument:
    `${actAttr('click', 'viewScreenshot', [r.id, r.payment_screenshot, r.name, r.utr||''])}`
- **Modal State Binding (`viewScreenshot` & `openEnrModal`)**:
  * `function viewScreenshot(id, filename, name, utr)` immediately binds `_currentEnrId = id;`, resets `enrNote`, displays the full-size receipt or 12-digit UPI voucher, and enriches candidate details from `PG['enr'].all` cache.
  * `openEnrModal(id)` leverages local cache first before fallback network fetching, displaying candidate domain, email, batch, joining date, and payment status.
- **Interactive Feedback & Loading Spinners**:
  * Modal buttons assigned IDs `id="btnEnrAccept"` and `id="btnEnrReject"`.
  * During API requests, buttons are disabled and render animated spinners:
    - Accept: `<i class="fas fa-spinner fa-spin"></i> Accepting...`
    - Reject: `<i class="fas fa-spinner fa-spin"></i> Rejecting...`
  * Buttons restore original state and text inside a `finally` block.
- **CSRF & Toast Feedback**:
  * `apiFetch` automatically detects and attaches `X-CSRF-Token` from `<meta name="csrf-token">`.
  * Displays user-facing toast alerts (`showToast('Enrollment accepted successfully.', 'green')` or error toast).

### 20.3. Backend Multi-Table Lifecycle Synchronization (`app.py`)
- **Endpoints**:
  * `POST /admin/enrollment/review` (Single enrollment decision)
  * `POST /admin/enrollment/bulk-review` (Bulk enrollment decisions)
- **State Transition Matrix on Accept (`action == 'accept'`)**:
  1. `enrollments`: Updates `payment_status = 'Accepted'`, `admin_note = note`, `updated_at = now`.
  2. `applications`: Updates `status = 'Accepted'`, `updated_at = now` (matching `email` and `domain`).
  3. `intern_offer_letters`: Updates `caution_deposit_status = 'VERIFIED'`, `pdf_unlocked = 1`, `updated_at = now` (unlocks official appointment letter).
  4. `intern_accounts`: Updates `is_active = 1`, `updated_at = now` (activates LMS workstation).
  5. `handle_enrollment_accepted(conn, eid)`: Mints ambassador referral code, auto-enrolls intern into domain curricula, and calculates referral commissions.
- **State Transition Matrix on Reject (`action == 'reject'`)**:
  1. `enrollments`: Updates `payment_status = 'Rejected'`, `admin_note = note`, `updated_at = now`.
  2. `applications`: Reverts `status = 'Enrollment Pending'` (or `STATUS_PAID_ENROLLED` for paid programs).
  3. `intern_offer_letters`: Updates `caution_deposit_status = 'REJECTED'`, `updated_at = now`.

### 20.4. Dual-Engine Notification Pipeline with Safe Isolation
- **Resilient Delivery**:
  * Notification triggers are wrapped in dedicated `try...except` blocks, ensuring external SMTP latency or push gateway errors never fail the admin transaction or return HTTP 500.
- **Acceptance Dispatch**:
  * Google Workspace SMTP: Sends official enrollment acceptance dossier email (`send_enrollment_acceptance_dossier_email(ed)`).
  * Real-Time VAPID Web Push: Dispatches `🎉 Enrollment Confirmed & Seat Unlocked!` notification to candidate's registered devices with deep-link to `https://lms.dbert.in/portal/offer`.
- **Rejection Dispatch**:
  * Google Workspace SMTP: Sends status update email with admin note explaining re-submission instructions.
  * Real-Time VAPID Web Push: Dispatches `⚠️ Caution Deposit Needs Resubmission` notification with admin note.

### 20.5. Automated Test Suite & Production Verification
- **Automated Test Suite**:
  * `apps/portal/tests/test_admin_enrollment_review_flow.py` (6 comprehensive test cases):
    1. `test_unauthorized_review_returns_401`
    2. `test_invalid_payload_returns_400`
    3. `test_review_accept_synchronizes_all_tables`
    4. `test_review_reject_synchronizes_all_tables`
    5. `test_bulk_review_accept`
    6. `test_admin_html_markup_compliance`
- **Verification Environment**:
  * 100% test pass on local SQLite and live EC2 PostgreSQL production environment.






