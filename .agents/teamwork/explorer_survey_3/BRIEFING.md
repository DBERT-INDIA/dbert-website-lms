# BRIEFING — 2026-11-04T23:36:00Z

## Mission
Investigate email infrastructure, domain authentication (SPF, DKIM, DMARC, MX, PTR), Google Workspace SMTP policies, Gmail 2024 Bulk Sender rules, port and TLS protocols, and multi-provider fallback architectures for reliable inbox delivery to ain.sharma.abhinav@gmail.com and ajnatechrpa@gmail.com.

## 🔒 My Identity
- Archetype: explorer
- Roles: [explorer, synthesis]
- Working directory: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_survey_3
- Original parent: 1954b148-861e-46e3-9273-69539bb3dcb5
- Milestone: email-survey-deliverability-architecture

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- COOLDOWN ENFORCEMENT: UNDER NO CIRCUMSTANCES SEND LIVE EMAILS OR CONNECT TO EXTERNAL SMTP/API SERVERS. ALL TESTS MUST BE DRY-RUN/MOCK/OFFLINE.

## Current Parent
- Conversation ID: 1954b148-861e-46e3-9273-69539bb3dcb5
- Updated: 2026-11-04T23:34:23Z

## Investigation State
- **Explored paths**:
  - Authoritative DNS queries: MX, SPF, DKIM, DMARC for `dbert.in`, `dbert.online`, `dbert.info`.
  - Reverse DNS (PTR) and port 25 constraints for AWS EC2 `3.26.237.171`.
  - Codebase: `apps/portal/.env`, `apps/portal/app.py` (lines 300–350, 3900–4120, 18090–18125).
  - Domain services: `services/notification_service.py`, `services/notifications/dispatch.py`, `services/outbox_service.py`.
  - Test suites and scripts: `scripts/test_isolation_matrix.py`, `scripts/test_link_formats.py`, `scripts/verify_delivery_dual_test.py`.
  - Execution logs: `transcript.jsonl` (lines 2400–6789) diagnosing exact user interaction and delivery timeline.
- **Key findings**:
  1. DMARC was non-existent (NXDOMAIN) during initial testing, causing Gmail inbound filter rejection/spam. DMARC has now been published and verified live (`v=DMARC1; p=none; sp=none; rua=mailto:abhinav.sharma@dbert.in`).
  2. `dbert.info` and `dbert.online` are suspended domains (`ns1.verification-hold.suspended-domain.com`). Embedding `mailto:careers@dbert.info` in email footers (`app.py:3953, 3962`) severely penalized message reputation.
  3. `SMTP_BACKUP_HOST=dbert.info` in `.env` causes unhandled connection failures upon fallback.
  4. Test 5B (domain path `dbert.in/verify/...` without `https://`) succeeded into the inbox, but subsequent rapid-fire bursts within 60–120s triggered Google's burst-velocity rate limiter.
  5. Bounces from demo applications (`candidate_delta@example.com`) caused Google mailer-daemon bounce notices; `DUMMY_EMAIL_DOMAINS` guard deployed to prevent future bounces.
  6. Direct sending from EC2 IP is impossible due to generic AWS PTR, lack of SPF inclusion, and AWS port 25 block; authenticated relay via Google Workspace or HTTPS API is mandatory.
- **Unexplored areas**: None. Full evidence chain complete across DNS, SMTP, headers, and code paths.

## Key Decisions Made
- Confirmed full tri-factor authentication: SPF (`_spf.google.com`), DKIM (`google._domainkey.dbert.in`), and DMARC (`_dmarc.dbert.in`).
- Formulated architectural blueprint for multi-provider fallback engine (Primary: Google Workspace SMTP with pacing; Secondary: Transactional HTTPS API; Tertiary: Transactional Outbox).
- Documented clean MIME and header synthesis specifications conforming to SCOPE.md interface contract.

## Artifact Index
- DISPATCH.md — Task instructions and dispatch log
- BRIEFING.md — Persistent situational awareness
- progress.md — Liveness heartbeat and milestone tracker
- analysis.md — Comprehensive findings and architecture recommendations
- handoff.md — 5-component completion handoff report
