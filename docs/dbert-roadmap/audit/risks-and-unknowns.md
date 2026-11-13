# DBERT Operational Risks & Technical Unknowns
**Audit As-of Date:** 9 November 2026  
**Auditor:** Antigravity AI Engine  

---

## 1. Identified Technical & Operational Risks

### 1.1. Google Workspace SMTP Daily Sending Limits
- **Risk:** Google Workspace imposes a strict 24-hour rolling sending limit (~500 emails/day per user account `abhinav.sharma@dbert.in`). High-volume batch dispatches can hit `550 5.4.5 Daily user sending limit exceeded`.
- **Mitigation:** Built-in circuit breakers in `dispatch_409_provisional.py` and `dispatch_9_verified_certificates.py` exit with status code 55 without dropping state. The automated watchdog daemon `quota_watchdog_and_dispatcher.py` probes quota every 5 minutes and resumes immediately upon quota replenishment.

### 1.2. Candidate Privacy & Consent Governance
- **Risk:** Public exposure of candidate personal details (phone numbers, private email addresses, UPI accounts, raw academic grades) creates regulatory and privacy exposure.
- **Mitigation:** Strict Privacy-by-Default architecture:
  - Phone numbers and UPI IDs are Fernet-encrypted in PostgreSQL.
  - The public Pre-Vetted Engineers Directory displays candidate names, domains, tech stacks, and evaluation rubrics, omitting all personal contact info.
  - Verification is strictly exact-ID based.

### 1.3. Next.js Standalone Build Symlink Desynchronization
- **Risk:** Running `npm run build` in Next.js Turbopack generates a fresh `.next/standalone` folder which initially lacks symlinks to the production `data/` directory, causing API lookup failures if not handled.
- **Mitigation:** Production deployment script `scripts/deploy_directory_to_ec2.py` and `scripts/deploy_enrollment_1999_to_ec2.py` automatically copy `public/` assets and re-link `/var/www/dbert-website-lms/data` to `.next/standalone/data` immediately after every build before restarting `dbert-website.service`.

### 1.4. External Job Lead Freshness & False Taxonomy
- **Risk:** Scraped job leads can go stale or misclassify non-technical roles (e.g. sales, administrative) under AI/engineering categories.
- **Mitigation:** Automated domain normalization pipelines with 30-day expiration windows and clear source transparency tags (`DIRECT`, `PARTNER`, `SOURCED_LEAD`).
