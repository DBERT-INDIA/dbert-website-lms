# DISPATCH for explorer_survey_3

## Task
Email Infrastructure, Domain Authentication (SPF, DKIM, DMARC), and Deliverability Architecture Analysis.

## Scope & Objective
1. Inspect DNS records and domain authentication configuration in the repository, docs, scripts, and environment files for `dbert.in` and `dbert.online`.
2. Analyze SPF records (`v=spf1 ...`), DKIM records/selectors, DMARC policy (`v=DMARC1 ...`), MX records, and reverse DNS (PTR).
3. Analyze Google's sender requirements (especially 2024 Gmail Bulk/General Sender Guidelines for delivery to `@gmail.com` accounts: mandatory SPF, DKIM, DMARC, valid forward/reverse DNS, TLS requirement, spam threshold < 0.3%).
4. Investigate the current SMTP sender configuration: from address, envelope sender (Return-Path), SMTP host (`smtp.gmail.com` vs custom relay vs EC2 direct SMTP), port (465 SSL vs 587 STARTTLS vs 25), authentication mechanism (Google App Passwords vs OAuth2 vs SMTP relay).
5. Identify why emails sent from this domain or host fail Gmail's spam filters or get blocked at the gateway.
6. Evaluate architectural solutions for 100% reliable inbox delivery:
   - Optimized Google Workspace SMTP relay / App Password configuration
   - Multi-provider fallback (e.g. SMTP + transactional API like Resend, SendGrid, Amazon SES, Brevo)
   - Proper header synthesis (Message-ID with proper FQDN domain, Date, Mime-Version, auto-unsubscribe, etc.)
   - Dry-run / mock capabilities for zero-risk testing.

## STRICT CONSTRAINT: COOLDOWN ENFORCEMENT
DO NOT send any live emails or execute any script that connects to external SMTP/API servers. This is a read-only investigation.

## Inputs
- `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\ORIGINAL_REQUEST.md`
- Repository DNS notes, deployment scripts, `.env` files, Nginx/domain configs.

## Output Requirements
- Write your comprehensive findings in `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_survey_3\analysis.md`
- Write your structured completion handoff in `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_survey_3\handoff.md`
- When complete, notify the orchestrator with send_message.

## 2026-11-04T23:24:50Z
[Message from 1954b148-861e-46e3-9273-69539bb3dcb5]
You are explorer_survey_3, an exploration subagent.
Your working directory is: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_survey_3
Read your task instructions at: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_survey_3\DISPATCH.md
Read the original request at: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\ORIGINAL_REQUEST.md

CRITICAL CONSTRAINT: COOLDOWN ENFORCEMENT - UNDER NO CIRCUMSTANCES SEND LIVE EMAILS OR CONNECT TO EXTERNAL SMTP/API SERVERS. THIS IS A READ-ONLY INVESTIGATION.

Investigate domain authentication (SPF, DKIM, DMARC, MX, PTR), Google Workspace SMTP policies, Gmail 2024 Bulk Sender rules, port and TLS protocols, and multi-provider fallback architectures.
Write your analysis to c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_survey_3\analysis.md
Write your completion handoff to c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_survey_3\handoff.md
When finished, send a message to the orchestrator (conversation ID: 1954b148-861e-46e3-9273-69539bb3dcb5).

## 2026-11-04T23:34:23Z
[Message from 1954b148-861e-46e3-9273-69539bb3dcb5]
**Context**: Infrastructure and DNS Update from Parent
**Content**: 
1. DMARC TXT record has been published and verified live on global DNS:
   - Host: _dmarc.dbert.in
   - Content: "v=DMARC1; p=none; sp=none; rua=mailto:abhinav.sharma@dbert.in"
2. dbert.in now has full tri-factor authentication: SPF (include:_spf.google.com), DKIM (google._domainkey.dbert.in), and DMARC.
3. Production hard bounce prevention guard (DUMMY_EMAIL_DOMAINS) is deployed and active on EC2 production (apps/portal/app.py line 4067).
**Action**: Please factor this into your analysis and report.
