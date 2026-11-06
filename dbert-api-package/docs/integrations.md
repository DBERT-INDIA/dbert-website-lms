# DBERT Third-Party Integrations Architectural Blueprint

This document details all third-party and external service integrations ported into the FastAPI backend.

---

## 1. Razorpay Payment Gateway

### 1.1 Key Components
- **Client**: `backend/services/razorpay_client.py` using `httpx.AsyncClient`.
- **Order Creation**: `/api/v1/payments/razorpay/create-order`
  - Takes `amount` (in paise, integer), `currency` ("INR"), and receipt identifier.
  - Calls `POST https://api.razorpay.com/v1/orders` with HTTP Basic Auth (`RAZORPAY_KEY_ID:RAZORPAY_KEY_SECRET`).
- **Payment Verification**: `/api/v1/payments/razorpay/verify-payment`
  - Validates `razorpay_order_id`, `razorpay_payment_id`, and `razorpay_signature`.
  - Signature computed using HMAC-SHA256: `hmac.new(secret, f"{order_id}|{payment_id}", hashlib.sha256).hexdigest()`.
- **Webhook Processing**: `/api/v1/payments/razorpay/webhook`
  - Verifies `X-Razorpay-Signature` against the raw request body.
  - Handles `payment.captured`, `order.paid`, and `refund.processed`.
- **Deposit / Product Amounts**:
  - `UPI_AMOUNT`: ₹499 (internship security deposit, refundable).
  - `PAID_PROGRAM_AMOUNT`: ₹1,599 (direct paid track).
  - Track 3: ₹1,999 (advanced program).

---

## 2. Google Gemini Generative AI

### 2.1 Interview Engine
- **Client**: `backend/services/interview_service.py` using `httpx.AsyncClient`.
- **Key Rotation**: Supports comma-separated `GEMINI_API_KEYS` + `GEMINI_API_KEY_1..20`.
- **Model**: Default `gemini-2.0-flash-lite` (or configurable via `GEMINI_MODEL`).
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
- **Timeout Budget**: Per-call `GEMINI_TIMEOUT` (8s), overall budget `GEMINI_TOTAL_BUDGET` (30s).
- **Fallback**: If all Gemini keys fail or budget is exceeded, falls back smoothly to the curated domain question bank (`INTERVIEW_BLUEPRINT`). The applicant is never blocked.
- **GitHub Enrichment**: If applicant provides a GitHub username, fetches public repos using `GITHUB_TOKEN` to generate personalized technical questions.

### 2.2 Guided Learning (GL) AI Tutor
- Multi-turn socratic dialog tutor per course subtopic (`/api/v1/courses/{id}/subtopic/{subtopic_id}/chat`).
- Tracks student misconceptions (`gl_misconception_catalog`) and concept mastery (`gl_student_mastery`).

---

## 3. Email Delivery Engine

### 3.1 Dual-Failover Architecture
- **Primary Host**: `SMTP_HOST` (`dbert.in`), port 465 (SSL).
- **Secondary Host**: `SMTP_BACKUP_HOST` (`dbert.info`), port 465 (SSL).
- **Relay Microservice**: `CPANEL_EMAIL_API_URL` (`https://mailer.aivaratech.online/send`).
- **AWS SES Fallback**: If `EMAIL_PROVIDER=ses`, dispatches using Amazon SES API.
- **Outbox Queue**: All non-critical transactional emails queued in `event_outbox` table and processed asynchronously by the background runner / cron endpoint.

---

## 4. Push Notifications & In-House Push Engine

### 4.1 OneSignal Integration
- REST API endpoint: `https://api.onesignal.com/notifications`
- Headers: `Authorization: Basic {ONESIGNAL_REST_API_KEY}`
- Targets users by external user ID (`intern_id` / email).

### 4.2 In-House Push & Bot Protection (Replacing Cloudflare Turnstile)
- Cloudflare Turnstile has been excluded per project requirements.
- **Bot Defense**: Signed cryptographic timing tokens + sliding-window rate limiting on sensitive submission endpoints.
- **In-House Notifications**: PostgreSQL-backed notification inbox (`notifications` table) with real-time polling or WebSocket stream for frontend subscribers.

---

## 5. Security & Encryption

### 5.1 Financial PII Encryption (Fernet)
- Ambassador UPI identifiers and payout details are encrypted at rest using AES-128-CBC + HMAC-SHA256 via `cryptography.fernet.Fernet` (`FERNET_KEY`).

### 5.2 Passwords
- All user passwords stored as salted bcrypt hashes.
- Legacy 64-character SHA-256 digests migrated to bcrypt lazily upon next successful login.
