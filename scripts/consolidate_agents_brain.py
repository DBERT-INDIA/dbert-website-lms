import re

def main():
    with open('AGENTS.md', 'r', encoding='utf-8') as f:
        text = f.read()

    parts = re.split(r'\n(?=## \d+\. )', text)
    print(f'Total original parts: {len(parts)}')

    # Part 0 is file header
    part0 = parts[0]

    # Add pointer to ARCHITECTURE_ROADMAP.md right below the header
    header_addon = """
> [!IMPORTANT]
> **DBERT MASTER ARCHITECTURE & USER JOURNEY ROADMAP**:
> For the comprehensive system topology, end-to-end user state machines, 5 Mermaid sequence/state diagrams, complete dead-end & silent-fail audits, stage-by-stage feature entitlement matrix, and 4-phase strategic engineering roadmap, refer to **[`ARCHITECTURE_ROADMAP.md`](file:///c:/Users/user/Desktop/dbert-website-lms/ARCHITECTURE_ROADMAP.md)**.
"""
    if '# DBERT Engineering & Agent Brain (AGENTS.md)' in part0:
        part0 = part0.replace('================================================================================\n\n', '================================================================================\n' + header_addon + '\n')

    def renumber_section(part_text, old_num, new_num, new_title=None):
        lines = part_text.split('\n')
        m = re.match(r'^##\s+\d+\.\s+(.*)', lines[0])
        if not m:
            return part_text
        title = new_title if new_title else m.group(1).strip()
        lines[0] = f'## {new_num}. {title}'
        
        # Renumber ### <old_num>.<sub_num>.
        for i in range(1, len(lines)):
            sub_m = re.match(r'^(###\s+)\d+\.(\d+)(\.\s+.*)', lines[i])
            if sub_m:
                lines[i] = f'{sub_m.group(1)}{new_num}.{sub_m.group(2)}{sub_m.group(3)}'
        return '\n'.join(lines)

    # Define Section 8: Historical Batch Ingestion & Dispatch Campaign Registry
    sec8_historical_registry = """## 8. Historical Batch Ingestion & Dispatch Campaign Registry

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
"""

    # Update Part 9 (Persistent Documentation Directory) to include ARCHITECTURE_ROADMAP.md and renumber to Section 9
    part9_text = parts[9]
    part9_text = renumber_section(part9_text, 9, 9)
    if 'ARCHITECTURE_ROADMAP.md' not in part9_text:
        part9_text = part9_text.replace('- Comprehensive architectural records and changelogs:\n', '- Comprehensive architectural records and changelogs:\n  - [`ARCHITECTURE_ROADMAP.md`](file:///c:/Users/user/Desktop/dbert-website-lms/ARCHITECTURE_ROADMAP.md)\n')

    # Merged Offer Letter Section (Section 42)
    sec42_offer_letter = """## 42. Official Internship Offer Letter, Preview Gating & Digitally Signed PDF Engine (`/portal/offer`)

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
"""

    new_sections = [
        (1, renumber_section(parts[1], 1, 1)),
        (2, renumber_section(parts[2], 2, 2)),
        (3, renumber_section(parts[3], 3, 3)),
        (4, renumber_section(parts[5], 5, 4)),
        (5, renumber_section(parts[6], 6, 5)),
        (6, renumber_section(parts[7], 7, 6)),
        (7, renumber_section(parts[8], 8, 7)),
        (8, sec8_historical_registry),
        (9, part9_text),
        (10, renumber_section(parts[13], 13, 10)),
        (11, renumber_section(parts[14], 14, 11)),
        (12, renumber_section(parts[15], 15, 12)),
        (13, renumber_section(parts[16], 16, 13)),
        (14, renumber_section(parts[17], 17, 14)),
        (15, renumber_section(parts[18], 18, 15)),
        (16, renumber_section(parts[19], 19, 16)),
        (17, renumber_section(parts[20], 18, 17)),
        (18, renumber_section(parts[21], 19, 18)),
        (19, renumber_section(parts[22], 20, 19)),
        (20, renumber_section(parts[23], 21, 20)),
        (21, renumber_section(parts[24], 22, 21)),
        (22, renumber_section(parts[26], 24, 22)),
        (23, renumber_section(parts[27], 25, 23)),
        (24, renumber_section(parts[28], 26, 24)),
        (25, renumber_section(parts[29], 27, 25)),
        (26, renumber_section(parts[31], 29, 26)),
        (27, renumber_section(parts[32], 30, 27)),
        (28, renumber_section(parts[33], 31, 28)),
        (29, renumber_section(parts[34], 32, 29)),
        (30, renumber_section(parts[35], 33, 30)),
        (31, renumber_section(parts[36], 34, 31)),
        (32, renumber_section(parts[37], 35, 32)),
        (33, renumber_section(parts[38], 36, 33)),
        (34, renumber_section(parts[39], 37, 34)),
        (35, renumber_section(parts[40], 38, 35)),
        (36, renumber_section(parts[42], 40, 36)),
        (37, renumber_section(parts[43], 41, 37)),
        (38, renumber_section(parts[44], 42, 38)),
        (39, renumber_section(parts[45], 43, 39)),
        (40, renumber_section(parts[46], 44, 40)),
        (41, renumber_section(parts[47], 45, 41)),
        (42, sec42_offer_letter),
        (43, renumber_section(parts[49], 47, 43)),
        (44, renumber_section(parts[50], 48, 44)),
    ]

    print(f'Total new sections: {len(new_sections)}')

    full_output = part0.strip() + '\n\n---\n\n'
    for idx, (num, content) in enumerate(new_sections):
        full_output += content.strip() + '\n\n---\n\n'

    # Remove trailing separator
    full_output = full_output.rstrip('-\n ') + '\n'

    # Write to AGENTS.md and GEMINI.md
    with open('AGENTS.md', 'w', encoding='utf-8') as f:
        f.write(full_output)
    with open('GEMINI.md', 'w', encoding='utf-8') as f:
        f.write(full_output)

    print('Successfully consolidated and wrote AGENTS.md and GEMINI.md')
    print(f'Total length of consolidated brain: {len(full_output)} bytes ({len(full_output.splitlines())} lines)')

if __name__ == '__main__':
    main()
