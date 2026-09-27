# Email Path Migration Report

**Date:** 2026-09-26  
**Project:** DBERT LMS  
**Target:** Complete Email Path Migration to DBERT Mailer

---

## 1. Migration Overview

- **Default Transport:** DBERT Mailer API (`https://mailer.aivaratech.online/send`).
- **Portal Core `_send()` Handler:** Updated in `apps/portal/app.py` to route all non-SES transactional emails directly to `_cpanel_api_send()`.
- **Direct Local SMTP Egress:** Removed from core portal dispatch logic. Direct `smtplib` usage is strictly scoped to `apps/portal/dbert-mailer/` microservice.

---

## 2. Unit & Integration Verification

- **Test Suite (`tests/test_email_path_migration.py`):** Verified that `send_email_async()` dispatches through `_cpanel_api_send()` when `EMAIL_PROVIDER` is un-set or set to default.
- **Pass Status:** `1 passed in 0.14s`.
