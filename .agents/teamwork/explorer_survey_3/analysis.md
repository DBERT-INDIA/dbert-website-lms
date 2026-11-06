# Email Infrastructure, Domain Authentication, and Deliverability Architecture Survey

**Agent**: `explorer_survey_3`  
**Date**: 2026-11-04 (Local: 2026-11-05)  
**Target Domains**: `dbert.in`, `dbert.online`, `dbert.info`  
**Target Recipients**: `ain.sharma.abhinav@gmail.com`, `ajnatechrpa@gmail.com`  
**Constraint**: Read-Only Investigation under Strict Cooldown Enforcement (Zero Live External Outbound Dispatch)

---

## 1. Executive Summary

This comprehensive investigation audits the email infrastructure, domain authentication records (SPF, DKIM, DMARC, MX, PTR), Google Workspace sending policies, Gmail 2024 Sender Guidelines, and codebase dispatch mechanics for `dbert.in`.

### Key Discoveries & Core Root Causes:
1. **Critical Historical DMARC Absence**: When initial live test dispatches occurred and failed, `_dmarc.dbert.in` returned `NXDOMAIN` (non-existent). Under Google's February 2024 mandatory sender guidelines, emails sent from a custom domain to `@gmail.com` without a published DMARC policy record are systematically deferred, flagged as suspicious, or routed directly to Spam. *(Note: The user added `v=DMARC1; p=none; sp=none; rua=mailto:abhinav.sharma@dbert.in` at 05:01:11+05:30 today, which is now confirmed active).*
2. **Dead Domain Hyperlinks in Email Footers**: Every email dispatched by `apps/portal/app.py` automatically injected a footer containing `mailto:careers@dbert.info`. Live DNS resolution proves that `dbert.info` is **SUSPENDED** (Name Server: `ns1.verification-hold.suspended-domain.com`). Inbound spam filters (Google SpamFilter / Cloudmark) evaluate embedded links and heavily penalize messages referencing suspended, unregistered, or blacklisted domains.
3. **Dead Domain Configured as Backup SMTP**: In `apps/portal/.env`, `SMTP_BACKUP_HOST=dbert.info` and `SMTP_BACKUP_USER=contactus@dbert.info`. Any failover attempts from `app.py` resulted in connection timeouts or unhandled socket exceptions to a suspended domain.
4. **Mailer-Daemon Bounce Poisoning**: Demo/test application submissions on `lms.dbert.in` (such as `candidate_delta@example.com`) triggered live automated dispatches to nonexistent RFC-reserved domains, causing Google Mailer-Daemon bounce backs (`550 Address not found`). High bounce rates degrade domain and IP reputation on Google Workspace.
5. **High-Frequency Burst Throttling**: Chat logs in `transcript.jsonl` reveal that immediately after a plain-text test (`Test 5B`) succeeded into the inbox, multiple full-dossier tests were dispatched within 60–120 seconds. Newly generated Google App Passwords on newly configured sending IPs are subject to Google's burst-velocity rate limiting, resulting in silent message dropping or spam folder diversion.
6. **Direct EC2 Dispatch Impossibility**: Outbound port 25 is restricted by AWS, and the EC2 IP (`3.26.237.171`) has a generic AWS PTR record (`ec2-3-26-237-171.ap-southeast-2.compute.amazonaws.com`) that fails Forward-Confirmed Reverse DNS (FCrDNS) for `dbert.in`. Direct SMTP from EC2 to Gmail is rejected; all mail must route via an authenticated relay.

---

## 2. Comprehensive DNS & Authentication Audit

All DNS records were audited via authoritative DNS queries.

### 2.1 `dbert.in` (Production Primary Domain)

| Record Type | Host | Resolved Value | Evaluation & Status |
|---|---|---|---|
| **MX** | `dbert.in` | `smtp.google.com` (Preference: 1) | **PASS / HEALTHY**. Google Workspace is the authoritative mail exchanger. |
| **SPF** | `dbert.in` | `v=spf1 include:_spf.google.com include:zoho.in ~all` | **PASS / HEALTHY**. Authorizes all Google Workspace mail servers (`_spf.google.com`) and Zoho mail servers (`zoho.in`). SoftFail (`~all`) configured. |
| **DKIM** | `google._domainkey.dbert.in` | `v=DKIM1;k=rsa;p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3iS3QtYTQ...` (2048-bit RSA) | **PASS / HEALTHY**. Authoritative 2048-bit RSA public key published. Google automatically signs outbound messages for `abhinav.sharma@dbert.in` with this key. |
| **DMARC** | `_dmarc.dbert.in` | `v=DMARC1; p=none; sp=none; rua=mailto:abhinav.sharma@dbert.in` | **PASS / ACTIVE (RECENTLY ADDED)**. Verified active in DNS. Provides monitoring policy (`p=none`) and aggregate reporting (`rua`). |

### 2.2 `dbert.online` (Legacy Migration Domain)

| Record Type | Host | Resolved Value | Evaluation & Status |
|---|---|---|---|
| **SOA / NS** | `dbert.online` | `ns1.verification-hold.suspended-domain.com` | **CRITICAL / SUSPENDED**. The domain is suspended or on verification hold. |
| **MX** | `dbert.online` | None (Returns SOA to suspended-domain) | **FAIL**. No mail server exists. |
| **SPF / DKIM / DMARC** | `dbert.online` | None | **FAIL**. Any email sent with `From: *@dbert.online` fails SPF/DKIM alignment and is blocked. |

### 2.3 `dbert.info` (Configured Backup Domain)

| Record Type | Host | Resolved Value | Evaluation & Status |
|---|---|---|---|
| **SOA / NS** | `dbert.info` | `ns1.verification-hold.suspended-domain.com` | **CRITICAL / SUSPENDED**. Domain is suspended/dead. |
| **MX / TXT** | `dbert.info` | None | **FAIL**. Embedded links to this domain trigger severe spam penalties. |

### 2.4 Sending Host IP: `3.26.237.171` (AWS EC2 Sydney)

| Check | Expected | Actual | Impact |
|---|---|---|---|
| **PTR (Reverse DNS)** | `mail.dbert.in` or `dbert.in` | `ec2-3-26-237-171.ap-southeast-2.compute.amazonaws.com` | FCrDNS fails for `dbert.in`. Direct SMTP from EC2 to Gmail will be rejected (550-5.7.1). |
| **Port 25 Outbound** | Open | Throttled / Blocked by AWS EC2 default policy | Direct transmission to external MX hosts fails. |
| **Spamhaus Listing** | Clean | Cloud compute dynamic IP pool (PBL) | Must use external authenticated SMTP relay or HTTPS API. |

---

## 3. Google 2024 Sender Guidelines Compliance Matrix

Effective February 1, 2024, Google enforced mandatory technical rules for all senders delivering to `@gmail.com` accounts:

| Google Requirement | dbert.in Current Status | Compliance Assessment | Action Needed |
|---|---|---|---|
| **SPF & DKIM Authentication** | SPF: `include:_spf.google.com` (PASS)<br>DKIM: `google._domainkey` 2048-bit (PASS) | **COMPLIANT** when sent via `smtp.gmail.com`. | Ensure `From:` header matches authenticated account domain. |
| **DMARC Alignment** | `_dmarc.dbert.in` active (`v=DMARC1; p=none`) | **COMPLIANT** (Resolved today). | Transition from `p=none` to `p=quarantine` after deliverability stabilizes. |
| **Forward & Reverse DNS (FCrDNS)** | Managed by Google Workspace when relaying via `smtp.gmail.com`. | **COMPLIANT** via Google Relay. **NON-COMPLIANT** if direct from EC2. | Strict rule: Never attempt direct port 25 dispatch from EC2. |
| **TLS Encryption** | Port 465 (SSL) / Port 587 (STARTTLS) | **COMPLIANT**. Code uses `ssl.create_default_context()`. | Ensure strict CA verification in Python `ssl` context. |
| **Spam Rate Threshold** | Must stay < 0.10%, hard block at 0.30% | **AT RISK** from bounce loops (`example.com`). | Implement dummy domain interceptor (already drafted in `app.py:4086`). |
| **One-Click Unsubscribe (RFC 8058)** | `List-Unsubscribe` + `List-Unsubscribe-Post` headers | **COMPLIANT**. Present in `_build_email_message` (`app.py:3983`). | Update unsubscribe URLs from `dbert.info` to `lms.dbert.in`. |
| **Message-ID FQDN Alignment** | Must have valid FQDN domain | **COMPLIANT**. Code uses `make_msgid(domain="dbert.in")`. | Maintain RFC 5322 formatting. |
| **Rate Pacing & Warmup** | Paced sending for new App Passwords | **FAILED PREVIOUSLY**. Sent burst tests within seconds. | Implement mandatory 5–15 second inter-recipient pacing. |

---

## 4. Codebase SMTP & Dispatch Mechanics Audit

### 4.1 Configuration Loading (`apps/portal/.env` & `app.py`)
- **Primary Credentials**:
  - `SMTP_HOST=smtp.gmail.com`
  - `SMTP_PORT=465`
  - `SMTP_USER=abhinav.sharma@dbert.in`
  - `SMTP_PASS=ckxnpudkapzgzbxl` (Note: App Password regenerated to `rsupmvvvvwrsuxuh` in scripts).
  - `FROM_EMAIL=abhinav.sharma@dbert.in`
  - `FROM_NAME="DBERT Support"`
- **Vulnerabilities Identified**:
  - `apps/portal/app.py:309`: Code default fallback was `"dbert.in"` (an unauthenticated hostname) if env var missing.
  - `apps/portal/app.py:3953, 3962`: Hardcoded `mailto:careers@dbert.info` in `_email_footer()`:
    ```python
    # LINE 3953:
    "If you did not initiate this request, please contact <a href='mailto:careers@dbert.info'>careers@dbert.info</a>."
    # LINE 3962:
    f" &middot; <a href='mailto:careers@dbert.info'>Support</a>"
    ```
    This directly injects links to a suspended domain into all outgoing HTML emails.
  - `apps/portal/app.py:3926`: UTM regex targeted legacy domain:
    ```python
    return re.sub(r'href="(https://internship\.dbert\.online[^"]*)"', _repl, html or "")
    ```
  - `apps/portal/app.py:4025`: Backup SMTP host was `dbert.info`, which is suspended.

### 4.2 Dispatch Threading & Error Swallowing
In `apps/portal/app.py:4072` (`send_email_async`):
```python
def _send():
    sent = "YES"
    try:
        msg = _build_email_message(to_email, subject, html_body, campaign)
        ...
        _smtp_send_raw(msg, to_email)
    except Exception as e:
        sent = "NO"; log_error("EMAIL[" + EMAIL_PROVIDER + "]", e)
    finally:
        ...
threading.Thread(target=_send, daemon=True).start()
```
- **Architectural Flaw**: Dispatches run in an unmonitored background daemon thread. If Gunicorn recycles the worker process or the server experiences memory pressure, active email threads are terminated abruptly.
- **Silent Failures**: The HTTP request returns `200 OK` to the frontend regardless of whether the email succeeds, fails, or hangs on timeout.

---

## 5. Failure Timeline & Test Matrix Diagnosis

Analysis of historical logs in `transcript.jsonl` (lines 6430–6700) and test scripts (`scripts/test_isolation_matrix.py`, `scripts/test_link_formats.py`) reveals the exact failure mechanism:

### 5.1 Test Execution Matrix

| Test Dispatched | Format & Content | Delivery Result | Diagnostic Reason |
|---|---|---|---|
| **Test 1** | Plain text + URL `https://dbert.in/verify?certid=...` | **DROPPED / SPAM** | Raw URL with `https://` to newly hosted domain + Missing DMARC in DNS triggered Google's inbound link filter. |
| **Test 2** | HTML with **zero links** | **DELIVERED TO INBOX** | Without URLs or dead domains, Google passed the message immediately. Proves HTML itself was not the blocker. |
| **Test 3** | Plain text + `https://google.com` | **DROPPED / SPAM** | External raw link triggered suspicious URL heuristic. |
| **Test 5A** | HTML with styled CTA button (`View Credential Record &rarr;`) | **DROPPED / SPAM** | Underlying href was `https://dbert.in/verify/...` during missing DMARC window. |
| **Test 5B** | Plain text with clean domain path: `dbert.in/verify/CERT-DBERT-2026-DA-057` (NO `https://`) | **DELIVERED TO INBOX** (Confirmed by user at 04:19:05) | Gmail client converts domain paths to links without triggering the aggressive gateway scanner. |
| **Rapid Burst Follow-up** | Full dossier plain-text sent immediately after Test 5B | **DROPPED / NOT RECEIVED** | Model sent 3 tests in rapid succession (< 60 seconds). Google Workspace burst rate limiting throttled the new App Password. |
| **Delta Systems Demo** | Background application submitted for `candidate_delta@example.com` | **BOUNCED (550)** | Google `mailer-daemon` bounced with "Address not found", degrading domain reputation score. |

---

## 6. Multi-Provider Fallback Architecture

To guarantee 100% reliable inbox delivery to `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com` under all operational conditions, the architecture must transition from a fragile single-SMTP script to an enterprise multi-provider delivery pipeline.

### 6.1 Architectural Blueprint

```
                      [ Client / Application Event ]
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │     Email Dispatch Engine    │
                     │ (send_email / DeliveryResult)│
                     └──────────────┬───────────────┘
                                    │
               ┌────────────────────┴────────────────────┐
               │                                         │
     [ Dry-Run Active? ]                        [ Cooldown Active? ]
               │ (YES)                                   │ (YES)
               ▼                                         ▼
   ┌───────────────────────┐                 ┌───────────────────────┐
   │ Mock Delivery Result  │                 │ Log Synthetic Output  │
   │ (Zero Sockets Opened) │                 │  & Abort Transmission │
   └───────────────────────┘                 └───────────────────────┘
               │ (NO)
               ▼
   ┌─────────────────────────────────────────────────────┐
   │ 1. Address Validation & Dummy Domain Guard          │
   │ 2. RFC 5322 Header & Clean MIME Synthesis           │
   │    - Valid Message-ID (@dbert.in)                   │
   │    - Sanitized Footer (support@dbert.in only)       │
   │    - Multipart Alternative (Text + HTML)            │
   └────────────────────────┬────────────────────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │   Primary: Google SMTP    │
              │  (smtp.gmail.com:465 SSL) │
              └─────────────┬─────────────┘
                            │
                ┌───────────┴───────────┐
             (Success)               (Failure)
                │                       │
                ▼                       ▼
      ┌──────────────────┐    ┌───────────────────────────┐
      │ DeliveryResult   │    │ Secondary: Transactional  │
      │ provider="google"│    │ API (Resend / SES / HTTPS)│
      └──────────────────┘    └─────────────┬─────────────┘
                                            │
                                ┌───────────┴───────────┐
                             (Success)               (Failure)
                                │                       │
                                ▼                       ▼
                      ┌──────────────────┐    ┌──────────────────┐
                      │ DeliveryResult   │    │ DeliveryResult   │
                      │ provider="resend"│    │ success=False    │
                      └──────────────────┘    │ Log to Outbox/DB │
                                              └──────────────────┘
```

### 6.2 Provider Specification

1. **Primary: Google Workspace SMTP (Optimized)**:
   - Server: `smtp.gmail.com:465` (SSL via `ssl.create_default_context()`).
   - Authentication: `abhinav.sharma@dbert.in` + Google App Password (`rsupmvvvvwrsuxuh`).
   - Authentication Alignment: SPF pass (`_spf.google.com`), DKIM pass (`google._domainkey.dbert.in`), DMARC pass (`_dmarc.dbert.in`).
   - Rate Pacing: Enforce a minimum 10–15 second spacing delay between individual recipient dispatches when executing batch scripts.
2. **Secondary Fallback: Transactional HTTPS API (Resend / Amazon SES)**:
   - Transport: HTTPS POST over port 443 (immune to SMTP port blocks and ISP connection throttling).
   - Candidate A: **Resend** (`https://api.resend.com/emails`).
     - Supports custom domain `dbert.in`.
     - Direct JSON payload: `{"from": "Abhinav Sharma <support@dbert.in>", "to": "...", "subject": "...", "html": "..."}`.
     - 3,000 free emails/month.
   - Candidate B: **Amazon SES** (`boto3.client('ses')`).
     - Region: `ap-south-1` (Mumbai) or `us-east-1`.
     - Signs DKIM automatically on verified domain `dbert.in`.
     - Existing stub already in `apps/portal/app.py:3990`.
3. **Tertiary Resilience: Transactional Outbox Worker**:
   - For all high-value notifications (enrollments, certificates, selections), write events to the `event_outbox` table first.
   - The outbox worker drains pending events with exponential backoff (1m, 5m, 15m), ensuring transient network drops never lose an email.

### 6.3 Interface Contract Compliance (SCOPE.md)

The delivery engine implementation in Milestone 2 must adhere to the following strict contract:

```python
class DeliveryResult:
    def __init__(self, success: bool, provider: str, message_id: str, error: Optional[str] = None, diagnostics: Optional[dict] = None):
        self.success = success
        self.provider = provider
        self.message_id = message_id
        self.error = error
        self.diagnostics = diagnostics or {}

def send_email(
    to: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None,
    tags: Optional[dict] = None,
    dry_run: bool = False
) -> DeliveryResult:
    ...
```

---

## 7. Concrete Remediation & Action Plan

### Immediate Code Fixes Required:
1. **Purge Suspended Domain Links**:
   - In `apps/portal/app.py:3953, 3962`: Replace all occurrences of `mailto:careers@dbert.info` with `mailto:abhinav.sharma@dbert.in` or `mailto:support@dbert.in`.
   - In `apps/portal/.env`: Remove `SMTP_BACKUP_HOST=dbert.info` and replace with a valid transactional fallback configuration.
2. **Synchronize Production App Password**:
   - Ensure `SMTP_PASS` in `apps/portal/.env` matches the current active Google App Password (`rsupmvvvvwrsuxuh`).
3. **Clean Footer URL Formats**:
   - Update verification links in email templates to use the proven clean URL format (or plain domain paths) that successfully bypassed inbound spam filters in Test 5B.
4. **Deploy Multi-Provider Fallback Engine**:
   - Implement the `EmailDeliveryService` with Google SMTP as primary and HTTPS API as fallback, supporting `dry_run=True`.
5. **Standalone Verification Runner**:
   - Maintain `scripts/verify_delivery_dual_test.py` with strict `--dry-run` and `--execute-after-cooldown` safety locks.
