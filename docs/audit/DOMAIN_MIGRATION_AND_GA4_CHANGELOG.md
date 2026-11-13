# AI Agent Handover: Domain Migration (`dbert.online` $\rightarrow$ `dbert.in`) & GA4 Tag Update

**Last Updated:** November 5, 2026  
**Target Domains:** Authoritative: `https://dbert.in` | LMS: `https://lms.dbert.in` | API: `https://api.dbert.in`  
**Legacy Domain (301 Redirected):** `https://dbert.online`  
**Primary GA4 Measurement ID:** `G-MN7ME9X518` (Replaced legacy `G-GZ17KZ7MDW`)  

---

## 1. Executive Summary & Context for Future AI Agents

DBERT (Digital Blinc Education Research And Technology) migrated its authoritative domain from `dbert.online` to `dbert.in`. This repository contains two primary application tiers:
1. **`apps/website`**: Next.js 16 (Turbopack) statically exported frontend with central SEO configuration, MDX blog, certificate verification frontend, and startup incubation portal.
2. **`apps/portal`**: Flask-based Learning Management System (LMS) and student/intern portal running at `lms.dbert.in`.

### Core Requirements Executed:
1. **Google Analytics Telemetry**: Replaced legacy tag `G-GZ17KZ7MDW` with the official Google Tag snippet using Measurement ID **`G-MN7ME9X518`** across both client-side and server-side configurations.
2. **Dedicated Domain Migration Page (`/dbert-online`)**: Created an exact-match SEO landing page titled *"DBERT.online is Now DBERT.in — Domain Migration"* to capture search intent for `dbert.online`, `dbert online`, and related queries.
3. **Strategic Dual-Phrasing SEO Headlines**: Embedded specific callout headlines across core high-traffic routes:
   - *"DBERT.online is Now DBERT.in"* (migration notice for users checking where the service moved).
   - *"dbert.online is not the active platform"* (security/anti-confusion notice clarifying that all official operations run on `dbert.in`).

---

## 2. Complete Inventory of Modified & Created Files

| File Path | Action | Description |
| :--- | :--- | :--- |
| `apps/website/src/lib/analytics.ts` | **MODIFY** | Default `GA_MEASUREMENT_ID` updated to `'G-MN7ME9X518'`. |
| `apps/website/.env` | **MODIFY** | `NEXT_PUBLIC_GA_ID` set to `G-MN7ME9X518`. |
| `apps/website/src/app/layout.tsx` | **MODIFY** | Updated GA4 comments; `<Script>` injects `G-MN7ME9X518` with `strategy="lazyOnload"`. |
| `apps/website/src/data/seo.config.ts` | **MODIFY** | Added `/dbert-online` route configuration (50 char title, 154 char description, keyword `'dbert.online'`). |
| `apps/website/src/app/dbert-online/page.tsx` | **NEW** | Dedicated landing page with H1, security callouts, bento links, FAQ schema, and breadcrumb JSON-LD. |
| `apps/website/src/app/dbert-online/dbert-online.module.css` | **NEW** | Cyber-Industrial styles utilizing standard design tokens (zero inline styles, zero v1 deprecated tokens). |
| `apps/website/src/app/page.tsx` | **MODIFY** | Embedded `.migrationBanner` in crawler prose section explaining that `dbert.online` is now `dbert.in`. |
| `apps/website/src/app/page.module.css` | **MODIFY** | Added styling for `.migrationBanner`, `.migrationBannerTitle`, and `.migrationBannerText`. |
| `apps/website/src/app/about/credentials/page.tsx` | **MODIFY** | Added *"Official Web Domain: DBERT.online is Now DBERT.in"* card under `cardStack`. |
| `apps/website/src/app/about/page.tsx` | **MODIFY** | Added contextual anchor link pointing to `/dbert-online`. |
| `apps/website/src/app/verify/page.tsx` | **MODIFY** | Added domain continuity notice to both verified dossier view and manual search view. |
| `apps/website/src/app/verify/verify.module.css` | **MODIFY** | Added `.domainNotice` style class for certificate registry. |
| `apps/website/src/app/learners/page.tsx` | **MODIFY** | Added domain migration FAQ item to `learnerFaqs` and the `FAQPage` JSON-LD structured data. |
| `apps/website/src/components/layout/Footer.tsx` | **MODIFY** | Added `DBERT.online is Now DBERT.in Notice` link in `seoMeshLinks` to pass sitewide internal crawl equity. |
| `apps/portal/app.py` | **MODIFY** | Fallback default `GA4_ID` set to `G-MN7ME9X518` for server-side events and template injection. |
| `dbert-api-package/backend/core/config.py` | **MODIFY** | `GA4_ID` default set to `G-MN7ME9X518`. |
| `dbert-api-package/docs/env_vars.md` | **MODIFY** | Documented `GA4_ID` updated to `G-MN7ME9X518`. |
| `dbert-api-package/website-content/**` | **SYNC** | Synchronized changes to package copy (`seo.config.ts`, `dbert-online/`, `Footer.tsx`, etc.). |
| `deploy/deploy_ec2_unified.sh` | **MODIFY** | Unified deployment script updated with `NEXT_PUBLIC_GA_ID=G-MN7ME9X518`. |

---

## 3. Architecture Deep-Dive

### 3.1. Google Analytics 4 (gtag.js) Architecture
- **Snippet Details**:
  ```html
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-MN7ME9X518"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-MN7ME9X518');
  </script>
  ```
- **Next.js Implementation (`apps/website/src/app/layout.tsx`)**:
  Loaded using Next.js `next/script` with `strategy="lazyOnload"` to avoid blocking initial paint and maintain optimal Core Web Vitals (LCP/FID).
- **Client Helper (`apps/website/src/lib/analytics.ts`)**:
  Exported `trackEvent(eventName, params)` safely guards against server-side rendering (`typeof window === 'undefined'`) and missing `window.gtag`.
- **Server-Side Measurement Protocol (`apps/portal/app.py`)**:
  Flask backend dispatches server-side events (`referral_signup`, `referral_conversion`) to `https://www.google-analytics.com/mp/collect` using `GA4_ID = G-MN7ME9X518`.

### 3.2. Dedicated Migration Route: `/dbert-online`
- **Route URL**: `https://dbert.in/dbert-online`
- **Canonical URL**: `https://dbert.in/dbert-online`
- **SEO Rules (`apps/website/src/data/seo.config.ts`)**:
  - `keyword`: `'dbert.online'`
  - `title`: `'DBERT.online is Now DBERT.in — Domain Migration'` (50 chars $\le$ 52 chars). Layout appends ` | DBERT` (total 58 chars $\le$ 60 chars).
  - `description`: `'Official notice: DBERT.online is now DBERT.in. Discover our verified venture incubation, LMS portal, AI careers, and certificate verification on dbert.in.'` (154 chars $\in [140, 155]$).
- **Structured Data Included**:
  1. `BreadcrumbList`: Home (`https://dbert.in`) $\rightarrow$ Domain Notice (`https://dbert.in/dbert-online`).
  2. `FAQPage`: Questions covering reasons for domain migration, certificate validity, LMS login access, and authenticity verification.

### 3.3. HTTP Redirection Infrastructure
- **Apache (`apps/website/public/.htaccess` and `apps/website/.htaccess`)**:
  ```apache
  # 301 Permanent Redirect from legacy dbert.online -> dbert.in
  RewriteCond %{HTTP_HOST} ^(www\.)?dbert\.online$ [NC]
  RewriteRule ^(.*)$ "https://dbert.in/$1" [R=301,L]
  ```
- **Nginx (`deploy/dbert-unified-nginx.conf`)**:
  ```nginx
  server {
      listen 80;
      listen 443 ssl http2;
      server_name dbert.online www.dbert.online;
      return 301 https://dbert.in$request_uri;
  }
  ```

---

## 4. Verification & Validation Protocol for Agents

Any future AI agent modifying SEO, analytics, or layout files **MUST** run the following gates before concluding work:

### Gate 1: SEO Integrity Gate
```powershell
npm --prefix apps/website run check:seo
```
*Enforces:*
- Title $\le$ 52 characters.
- Description between 140 and 155 characters.
- Description contains the exact primary keyword.
- Primary keyword is unique across all configured routes.
- Every page on disk in `src/app/**/page.tsx` has an entry in `seo.config.ts`, and vice versa.

### Gate 2: UI Token & Accessibility Audits
```powershell
npm --prefix apps/website run audit:tokens
npm --prefix apps/website run audit:headings
npm --prefix apps/website run audit:styles
```
*Enforces:*
- No deprecated v1 tokens (`--color-*`, `--radius-*`, `--shadow-*`).
- No `color: var(--ink)` on dark cards.
- Exactly one `<h1>` per page with no skipped heading levels.
- Zero inline `style={{` in new page components.

### Gate 3: Next.js Production Build
```powershell
npm --prefix apps/website run build
```
*Confirms:*
- Static generation of all 96+ pages succeeds.
- Route `├ ○ /dbert-online` appears in the route manifest.
- Prerendered HTML files contain `G-MN7ME9X518`.

### Gate 4: Portal Analytics Test
```powershell
python -m pytest apps/portal/tests/learning/test_api_and_analytics.py
```
*Confirms:*
- Flask analytics processors and context injection function without regressions.

---

## 5. Rules for Future Modifications

1. **Do NOT delete the `/dbert-online` route**: Even after Google ranks `dbert.in`, this route maintains historical backlinks and handles search queries for the old brand name.
2. **Preserve Dual Phrasing**: Always maintain both messages:
   - "DBERT.online is now DBERT.in" (search transition).
   - "dbert.online is not the active platform" (security & authenticity).
3. **Keep `seo.config.ts` Synchronized**: If adding new routes to `apps/website/src/app/`, always add a corresponding entry in `apps/website/src/data/seo.config.ts` and sync it to `dbert-api-package/website-content/src/data/seo.config.ts`.
4. **Environment Variables**: If deploying to EC2 or Docker, pass `NEXT_PUBLIC_GA_ID=G-MN7ME9X518` and `GA4_ID=G-MN7ME9X518`.

---

## 6. DBERT Dual-Account WhatsApp Dispatcher Engine

**Added:** November 5, 2026  
**Reference Architecture:** `Desktop/vayanai/run_whatsapp_dispatcher.bat`  
**Registry Target:** `data/all_409_provisional_registry.json` (409 candidates)  
**Database:** `data/dbert_whatsapp.db` (SQLite WAL mode)  
**Chrome Profiles Reused:** `C:\Users\user\Desktop\aivara\aivara\.chrome_session_account1` and `.chrome_session_account2`  

### 6.1. CLI Entry Points:
1. `run_whatsapp_dispatcher.bat`: Main interactive menu (options 1–9, C, 0).
2. `run_worker_acc1.bat`: Launches Worker 1 (Account 1 - Odd serials, Green console).
3. `run_worker_acc2.bat`: Launches Worker 2 (Account 2 - Even serials, Yellow console).
4. `scripts/send_dbert_whatsapp.py`: Python CLI core with Playwright automation.

### 6.2. Key Capabilities & Safety Controls:
- **Batch Sizing**: 92 candidates per batch (46 odd for Account 1, 46 even for Account 2).
- **Anti-Ban Pacing**: 18s–35s randomized human delay between each message.
- **Circuit Breaker**: Automatically pauses worker if 3 consecutive failures occur.
- **Permanent Deduplication**: `whatsapp_sent_log` ensures no candidate ever receives duplicate messages across batch iterations.
- **Cross-Channel Omnichannel Sync**: Merges email tracking (`data/dispatch_tracking_409.json`) and WhatsApp delivery status into `data/dbert_unified_omnichannel_tracking.csv`.

---

## 7. WhatsApp Message Reformatting & Latest-First Signup Dispatch

### 7.1. Message Structure (Within First 15 Lines)
Both critical action links are placed prominently above the mobile fold:
- **Line 8**: Verification link (`👉 https://dbert.in/verify?certid=...`)
- **Line 11**: Claim & verification Google Form (`👉 https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header`)

### 7.2. Chronological Ordering (Latest First)
- All 409 candidates are dynamically indexed against their registration timestamps from `all_enrolled_interns_master_detailed.csv`, `data/grand_total_pending_candidates.csv`, and Google Sheets.
- The queue is sorted descending by registration timestamp (`signup_dt`), ensuring newest applicants receive priority dispatch.
- `signup_timestamp` is tracked in SQLite `whatsapp_dispatch` and exported in `data/dbert_whatsapp_master.csv`, `dbert_whatsapp_acc1.csv`, and `dbert_whatsapp_acc2.csv`.

---

## 8. WhatsApp Pre-Flight Login & Dispatch Verification Suite

### 8.1. New Automation Tools Added:
1. `scripts/verify_and_launch_dbert_whatsapp.py`:
   - Interactive pre-flight verifier validating database queues and checking WhatsApp Web login states.
   - Guides operator QR code scan on visible Chrome instances if session tokens need refresh.
   - Automatically launches dual workers (`run_worker_acc1.bat` and `run_worker_acc2.bat`) upon verification.
2. `verify_and_launch.bat`: One-click runner for full pre-flight verification and launch.
3. `login_acc1.bat`: Dedicated launcher for Account 1 session scan and authentication.
4. `login_acc2.bat`: Dedicated launcher for Account 2 session scan and authentication.
5. `run_whatsapp_dispatcher.bat`: Updated with menu options `[V]`, `[L1]`, `[L2]`, and alias `--test-phone`.

---

## 9. Alphabetical Credential Directory Architecture (`/verify/directory`)

**Added:** November 5, 2026  
**Route URL:** `https://dbert.in/verify/directory`  
**Dataset:** `apps/website/src/data/directory_candidates.json` (465 records: 56 verified + 409 provisional)  
**Deployment Tool:** `scripts/deploy_directory_to_ec2.py`  

### 9.1. Architectural Components:
1. **Server Page (`apps/website/src/app/verify/directory/page.tsx`)**:
   - Statically generates SEO metadata, structured data, and loads `directory_candidates.json`.
2. **Interactive Client Component (`DirectoryClient.tsx`)**:
   - A–Z alphabet letter selector with dynamic candidate counts per letter.
   - Real-time client-side instant search across candidate names, Certificate IDs, Intern IDs, and domain tracks.
   - Filter pills for major domain tracks (AI & Machine Learning, Data Analyst, Full Stack Web Development, Python Automation, etc.).
   - Visual badges distinguishing `Verified Official Credential` vs `Provisional (Verification Pending)`.
3. **Styling Module (`directory.module.css`)**:
   - Cyber-Industrial theme using DBERT dark mode design tokens (`#080C14`, `#141A23`, `#E2B96F` gold, `#38BDF8` cyan, `#10B981` emerald).
4. **Site Integration**:
   - Embedded directory discovery banner on `/verify`.
   - Breadcrumb navigation on `/verify/[certId]` linking back to `/verify/directory`.

---

## 10. 409 Candidate Email Batch Dispatch Engine & Deliverability Architecture

**Added:** November 5, 2026  
**Engine Script:** `scripts/dispatch_409_provisional.py`  
**Registry Target:** `data/all_409_provisional_registry.json`  
**Tracking State:** `data/dispatch_tracking_409.json` and `data/dispatch_tracking_409.csv`  
**Audit Log:** `data/dispatch_409.log`  

### 10.1. Key Deliverability Safeguards:
1. **DNS Pre-Flight Tri-Factor Audit**: Automatically queries and verifies SPF, DKIM, and DMARC before starting the batch.
2. **Authenticated Google Workspace SMTP Relay**:
   - Host: `smtp.gmail.com:465` (SSL)
   - Authenticated User: `abhinav.sharma@dbert.in`
   - `Reply-To`: Exactly matches sender (`abhinav.sharma@dbert.in`).
3. **Strict 30-Second Rate Control**: Paces emails at exactly 30 seconds to prevent ISP spam throttling.
4. **Milestone Telemetry**: Dispatches automated progress reports every 100 emails and at campaign completion to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.
5. **Resume & Idempotency**: State is atomically saved to `dispatch_tracking_409.json` after every delivery. If interrupted or restarted, previously sent candidates are automatically skipped with zero duplicate emails.

---

## 11. ₹1,999 Enrollment & ₹1,500 Balance Completion Portal (`/enroll/1999`)

**Added:** November 5, 2026  
**Live Portal URL:** `https://dbert.in/enroll/1999`  
**Forwarding Aliases:** `https://dbert.in/enroll` and `https://dbert.in/eroll` (Typo-safe, preserves query params)  
**Deployment Tool:** `scripts/deploy_enrollment_1999_to_ec2.py`  

### 11.1. Core Capabilities:
1. **Financial Ledger Transparency**:
   - Full Program Fee: **₹1,999**
   - Caution Deposit Credited: **-₹499**
   - Net Balance Payable: **₹1,500**
   - Explicit callout: *"Notice for Registered Candidates: If you have already paid the initial ₹499 caution deposit, your advance is credited in full. You only need to pay the remaining ₹1,500 balance to finalize your production enrollment and unlock your official credentials."*
2. **Candidate Profile Autofill API (`GET /api/enroll/lookup`)**:
   - Dynamic URL pre-population: `https://dbert.in/enroll/1999?certid=CERT-DBERT-2026-DA-057`
   - Automatically loads Full Name, Email, WhatsApp Phone, College, Domain Track, and Certificate ID from the 465-candidate master database.
   - Interactive lookup bar for manual search by Certificate ID or Email.
3. **Multi-Device Payment Integration**:
   - High-resolution official UPI QR code (`/images/qrcode.jpeg` and `/qrcode.jpeg`).
   - Mobile 1-Tap UPI Launchers (Google Pay, PhonePe, Paytm, Default UPI) pre-filled with ₹1,500 and merchant VPA `Q652429146@ybl` (`DBERT Admissions`).
   - Cross-platform blob-based "Download QR" button.
4. **12-Digit UTR Submission & Idempotent Recording (`POST /api/enroll/balance`)**:
   - Enforces format validation on the 12-digit UPI UTR.
   - Prevents duplicate submissions (`alreadySubmitted: true`).
   - Generates unique reference ID (e.g. `DBERT-ENR-611526-IPLF`).
   - Persists records permanently into `/var/www/dbert-website-lms/data/balance_enrollments_1500.json`.
5. **1-Tap WhatsApp Proof Routing**:
   - Pre-formats candidate name, Certificate ID, domain, UTR number, and submission reference directly into Admissions WhatsApp (`+91 81929 11360`).
6. **Locked Certificate CTA Integration**:
   - On `/verify/[certId]`, locked provisional certificates link directly to `/enroll/1999?certid={certId}`, with a secondary link to the Google Form.

---

## 12. Production EC2 Server Topology & Handover Protocol

**Server Host:** `ubuntu@3.26.237.171`  
**SSH Key:** `C:\Users\user\.ssh\dbert-production-server.pem`  
**Root Path:** `/var/www/dbert-website-lms`  
**Web App Path:** `/var/www/dbert-website-lms/apps/website`  

### 12.1. Standalone Deployment Steps for AI Agents:
```bash
# 1. Connect and navigate to website app
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" -o StrictHostKeyChecking=no -o BatchMode=yes ubuntu@3.26.237.171
cd /var/www/dbert-website-lms/apps/website

# 2. Build Next.js standalone bundle
export NODE_ENV=production
npm run build

# 3. Synchronize public assets into standalone directories
cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true

# 4. Re-establish permanent data directory symlink
mkdir -p /var/www/dbert-website-lms/data
rm -rf /var/www/dbert-website-lms/apps/website/.next/standalone/data
ln -s /var/www/dbert-website-lms/data /var/www/dbert-website-lms/apps/website/.next/standalone/data

# 5. Restart Next.js systemd service
sudo systemctl restart dbert-website.service
sleep 2
systemctl is-active dbert-website.service
```

### 12.2. Automated One-Command Deployers:
- `python scripts/deploy_enrollment_1999_to_ec2.py`: Automatically synchronizes enrollment components, runs EC2 standalone build, restarts service, and performs HTTP 200 validation across all endpoints.
- `python scripts/deploy_directory_to_ec2.py`: Automatically synchronizes directory components, updates candidate registries, and validates `/verify/directory`.
- `python scripts/deploy_new_certificates_to_ec2.py`: Automatically uploads updated master registries and preview PNGs, executes standalone build, and reloads `dbert-website.service`.

---

## 13. Verified Candidates Ingestion & Dispatch (Google Sheet gid=1265293201)

**Added:** November 5, 2026  
**Source Sheet:** `Certificate Internship Batch 2026 (Responses)` (`gid=1265293201`)  
**Generation Script:** `scripts/issue_9_verified_certificates.py`  
**Deployer Script:** `scripts/deploy_new_certificates_to_ec2.py`  
**Dispatch Daemon:** `scripts/dispatch_9_verified_certificates.py`  
**Tracking State:** `data/dispatch_tracking_9_verified.json`  
**Log Path:** `data/dispatch_9_verified.log`  

### 13.1. Reconciliation & Ingestion:
1. **Google Sheet Structure**:
   - Total rows: 65.
   - Rows 1–56: 56 original verified candidates (`CERT-DBERT-2026-DA-001` through `CERT-DBERT-2026-FSD-056`).
   - Rows 57–65: 9 candidate submissions from November 5, 2026 with ₹299 fee payment proof uploaded to Google Drive.
2. **Candidates Issued**:
   - `N Deekshitha`: [`CERT-DBERT-2026-AIML-092`](https://dbert.in/verify/CERT-DBERT-2026-AIML-092) (AI & ML, IIT Kharagpur, upgraded from provisional)
   - `M Brahmani`: [`CERT-DBERT-2026-DA-117`](https://dbert.in/verify/CERT-DBERT-2026-DA-117) (Data Analyst, Aditya Degree Women's College, upgraded from provisional)
   - `Ankit Saini`: [`CERT-DBERT-2026-FSD-070`](https://dbert.in/verify/CERT-DBERT-2026-FSD-070) (Full Stack, ABES EC Ghaziabad, upgraded from provisional)
   - `Lucky kumar`: [`CERT-DBERT-2026-PA-023`](https://dbert.in/verify/CERT-DBERT-2026-PA-023) (Python Automation, RIT, upgraded from provisional)
   - `Rohit Ranjan Tiwari`: [`CERT-DBERT-2026-DA-124`](https://dbert.in/verify/CERT-DBERT-2026-DA-124) (Data Analyst, Amity University Lucknow, upgraded from provisional)
   - `Shreyash Sambhaji Kamble`: [`CERT-DBERT-2026-DA-077`](https://dbert.in/verify/CERT-DBERT-2026-DA-077) (Data Analyst, Walchand CE Sangli, upgraded from provisional)
   - `Satya Patil`: [`CERT-DBERT-2026-DA-109`](https://dbert.in/verify/CERT-DBERT-2026-DA-109) (Data Analyst, SSGMCE, upgraded from provisional)
   - `Vasu Rakholiya`: [`CERT-DBERT-2026-DA-183`](https://dbert.in/verify/CERT-DBERT-2026-DA-183) (Data Analyst, Symbiosis Skills & Professional Univ, brand new candidate)
   - `Janhvi singh`: [`CERT-DBERT-2026-DA-184`](https://dbert.in/verify/CERT-DBERT-2026-DA-184) (Data Analyst, CSJM Univ Kanpur, brand new candidate)
3. **Artifacts & Production Sync**:
   - High-resolution 3-document PDF packets generated in `outputs/cohort_2026/`.
   - Preview PNGs copied to `apps/website/public/certificates/previews/{certId}.png`.
   - Master registries updated: `certificates_registry.json` (461 total), `directory_candidates.json` (467 total).
   - Deployed and built on EC2 production server (`3.26.237.171`). All 9 live endpoints return HTTP 200 with verified status and 1-click LinkedIn integration.

### 13.2. Google SMTP 24h Quota Status:
- Google Workspace SMTP for `abhinav.sharma@dbert.in` hit its daily limit (`550 5.4.5 Daily user sending limit exceeded`) after delivering 303 emails earlier today.
- `scripts/dispatch_9_verified_certificates.py` is pre-configured and ready to deliver the 9 verified emails.
- `scripts/dispatch_409_provisional.py` is pre-configured and ready to deliver the remaining 106 provisional emails (resuming at candidate #304).

---

## 14. Approved Incubation Enrollment & Live Countdown Architecture (`/enroll/1999`, `/eroll`)

**Added:** November 6, 2026  
**Candidate Approved:** **Bhargavi Poola** (`bhargavi13032007@gmail.com`, Phone: `9603742553`)  
**Domain Track:** Full Stack Web Development (`CERT-DBERT-2026-FSD-156` / `DBERT-2026-INT-1412`)  
**UTR Number:** `679862090077`  
**Submission Ref:** `DBERT-ENR-703685-TYN6`  
**Batch Kickoff:** **Monday, 9 Nov 2026 at 06:00 PM IST**  
**Deployer Script:** `scripts/deploy_bhargavi_approval_to_ec2.py`  
**Automated Browser Test:** `scripts/verify_bhargavi_playwright.py`  

### 14.1. Implementation & Architecture:
1. **Ledger Approval**:
   - `data/balance_enrollments_1500.json` updated with `status: "APPROVED"`, `batchStartDate: "2026-11-09T18:00:00+05:30"`, and `batchStartDisplay: "Monday, 9 Nov 2026"`.
   - Symlinked permanently to `/var/www/dbert-website-lms/data/balance_enrollments_1500.json`.
2. **Autofill API Update (`GET /api/enroll/lookup`)**:
   - Prioritizes `balance_enrollments_1500.json` by email, phone, UTR, Certificate ID, or submission reference.
   - Returns `isApproved: true`, `enrollmentStatus: "APPROVED"`, `batchStartDate`, and full candidate profile.
3. **Approved UI Dossier & Real-Time Countdown**:
   - Component: `apps/website/src/app/enroll/1999/EnrollmentClient.tsx`.
   - If candidate's enrollment is approved, the standard payment form and QR code are automatically swapped out.
   - Renders a prominent **"OFFICIAL ENROLLMENT APPROVED & SEAT CONFIRMED"** status header with pulsing green indicator.
   - Computes an active 1-second interval countdown: `[XX] DAYS, [XX] HOURS, [XX] MINUTES, [XX] SECONDS` ticking down to Monday, 9 Nov 2026 (06:00 PM IST).
   - Candidate Dossier displaying UTR, Ref ID, and ₹1,999 full program fee reconciliation.
   - 4-step Sprint Roadmap (Orientation, Repo Setup, Sprints, Final Production Review).
   - 1-Tap Admissions Concierge WhatsApp button pre-filled with approval details.
4. **Registry & Production Synchronization**:
   - Bhargavi Poola added to `certificates_registry.json` (462 total) and `directory_candidates.json` (468 total).
   - Deployed to EC2 (`3.26.237.171`), Next.js standalone bundle compiled with zero errors, and `dbert-website.service` restarted.
   - Live verified via automated Playwright test:
     - URL `https://dbert.in/eroll?email=bhargavi13032007@gmail.com` redirects (HTTP 307) to `/enroll/1999?email=bhargavi13032007%40gmail.com`.
     - Title: "Welcome to DBERT Technical Incubation, Bhargavi Poola!"
     - Countdown timer active: `03 DAYS, 07 HOURS, 58 MINUTES, 49 SECONDS` ticking down to Monday, 9 Nov 2026.
     - Verification page live: [`https://dbert.in/verify/CERT-DBERT-2026-FSD-156`](https://dbert.in/verify/CERT-DBERT-2026-FSD-156).




