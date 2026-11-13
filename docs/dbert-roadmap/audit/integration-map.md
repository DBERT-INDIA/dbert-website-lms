# DBERT Third-Party Integrations & External Services Map
**Audit As-of Date:** 9 November 2026  
**Auditor:** Antigravity AI Engine  

---

## 1. External Services Directory

| Integration | Protocol / Tech | Configuration & Credentials | Purpose / Operational Boundary | Rate Limits & Failure Handling |
|---|---|---|---|---|
| **Google Workspace SMTP** | SMTPS (Port 465) SSL | `smtp.gmail.com:465`<br>Sender: `abhinav.sharma@dbert.in` | Official authenticated transactional email delivery for certificates, acceptance letters, and telemetry notifications. | Google Workspace rolling daily limit (~500/day). Circuit breaker exits with code 55 upon 550 quota error; resumes automatically via watchdog. |
| **Google Analytics 4 (GA4)** | Google Tag (gtag.js) | Measurement ID: `G-MN7ME9X518` | Unified client and server telemetric tracking across `dbert.in` and `lms.dbert.in`. | Client-side async execution; non-blocking to user experience. |
| **WhatsApp Dual-Account Automation** | Playwright Chromium Headless | Dual profiles:<br>`data/.chrome_session_account1`<br>`data/.chrome_session_account2` | High-engagement direct admissions communication and verification notifications. | Strictly throttled with 18s–35s randomized human delays between messages. Anti-ban circuit breaker pauses after 3 errors. |
| **Google Gemini 2.5 AI Pre-Screening** | REST HTTPS via `google-generativeai` | In-portal `GEMINI_API_KEY` | Evaluates submitted technical sprint deliverables, GitHub PRs, and reports against domain-specific rubrics. | Admin pre-flight health check halts execution if API key is unconfigured to prevent silent failures. |
| **Razorpay / UPI Payment Gateway** | Webhook & Merchant VPA | Merchant VPA: `Q652429146@ybl`<br>(`DBERT Admissions`) | Program fee balance payments (₹1,500 net), automated QR rendering, and manual 12-digit UTR reconciliation. | UTRs validated via idempotent regex; duplicate UTR submissions rejected atomically. |
| **AWS EC2 Production Host** | SSH / Systemd / Nginx | Host: `ubuntu@3.26.237.171`<br>Base: `/var/www/dbert-website-lms` | Production deployment host managing reverse proxies, standalone Next.js server, Flask LMS, and FastAPI. | Managed via Systemd with automatic restart on process failure. |

---

## 2. DNS & Security Compliance

- **Domain:** `https://dbert.in`
- **SPF Record:** `v=spf1 include:_spf.google.com ~all`
- **DKIM Selector:** `google._domainkey.dbert.in`
- **DMARC Policy:** `v=DMARC1; p=none; sp=none; rua=mailto:abhinav.sharma@dbert.in`
- **SSL / TLS:** Let's Encrypt automated certificate renewal via Certbot on Nginx.
