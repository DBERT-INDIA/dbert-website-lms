# Scope: Email Deliverability Analysis & Permanent Fix

## Architecture
- Email Service Subsystem in `apps/portal/` (Flask backend)
- SMTP & Provider Integrations (Google Workspace / SMTP / Fallback providers)
- DNS & Deliverability Authentication (SPF, DKIM, DMARC, MX, Reverse DNS/PTR considerations)
- Delivery Monitoring & Verification Runner (Standalone post-cooldown tool with dry-run/mock testing)

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Deliverability Analysis & Root Cause Diagnosis | Full investigation of codebase, logs, chat, DNS (SPF/DKIM/DMARC), Google Workspace SMTP, and Gmail reception rules | M1 | survey |
| 2 | Permanent Robust Delivery Fix | Architectural redesign of email sending service with multi-provider/fallback, proper headers, error logging, retry, and deliverability best practices | M2 | requirements |
| 3 | Live Email Sending Safeguards (Cooldown) | Complete freeze on live email dispatch during development; dry-run/mock enforcement | M2 | requirements |
| 4 | Post-Cooldown Verification Runner & Docs | Automated standalone script to test live delivery to both recipients after cooldown + complete guide | M3 | requirements |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Survey & Root Cause Diagnosis | Code analysis, transmission logs, chat history, DNS/auth investigation | none | DONE |
| M2 | Permanent Delivery Solution Implementation | Refactored email dispatch engine, provider configuration, delivery headers, fallback, dry-run safety | M1 | DONE |
| M3 | Verification Runner & Documentation | Standalone post-cooldown script for live validation + instructions | M2 | DONE |

## Interface Contracts
### Email Delivery Engine
- `send_email(to, subject, html_content, text_content=None, tags=None, dry_run=False) -> DeliveryResult`
- `DeliveryResult`: `success: bool`, `provider: str`, `message_id: str`, `error: Optional[str]`, `diagnostics: dict`
