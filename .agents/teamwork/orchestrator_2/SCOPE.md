# Scope: DBERT Domain Remediation, UI/UX Modal Conversion, Artifact & Production Deployment

## Architecture
- `apps/website`: Next.js marketing website (runs on port 3001 or static export).
- `apps/portal`: Flask / Gunicorn LMS application (runs on port 5001).
- `dbert-api-package`: API package and website content.
- `deploy/`: EC2 deployment scripts, systemd service definitions, Nginx configs.
- Production host: AWS EC2 `ubuntu@3.26.237.171` (ap-southeast-2) with SSH key `C:\Users\user\.ssh\dbert-production-server.pem`.
- Live services & endpoints: `dbert.in` (:3001), `lms.dbert.in` (:5001), `api.dbert.in` (:8000), PostgreSQL 16 `dbert_lms`.

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|:---:|
| 1 | R1: Legacy Domain Remediation | Audit and replace all references to `dbert.online` and `internship.dbert.online` across all files with `dbert.in` and `lms.dbert.in` | M1, M2 | ORIGINAL_REQUEST §R1 | **VERIFIED** |
| 2 | R2: Password Reset Modal Conversion | Convert inline password reset form on LMS page into popup modal; identify and convert any similar inline elements | M1, M2 | ORIGINAL_REQUEST §R2 | **VERIFIED** |
| 3 | R3: Visual and UI/UX Audit & Fixes | Fix layout issues, stacked elements, broken styling, and interaction flaws in `apps/website` and `apps/portal` | M1, M2 | ORIGINAL_REQUEST §R3 | **VERIFIED** |
| 4 | Automated Tests & Local Verification | Run automated test suites, verify local builds and clean startup | M3, M6 | ORIGINAL_REQUEST §Acceptance Criteria | **REMEDIATING** (app.py:9615 NameError regression & running all 28 test suites) |
| 5 | R4: Audit & Fix Artifact | Author comprehensive documentation of all identified issues, modified files, and applied resolutions | M4, M7 | ORIGINAL_REQUEST §R4 | **NEEDS_UPDATE** |
| 6 | R5: Production Deployment & Live Verification | Deploy fixes to EC2 `ubuntu@3.26.237.171`, restart systemd services, test live endpoints | M5, M8 | ORIGINAL_REQUEST §R5 | **NEEDS_REDEPLOY** |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|:---:|
| M1 | Survey & Technical Investigation | 3 parallel Explorers mapped legacy domain occurrences, modal conversion targets, and visual UI/UX bugs | none | **DONE** |
| M2 | Remediation Implementation | Workers applied code, template, CSS, and database sanitization fixes | M1 | **DONE** |
| M3 | Verification & Review | 2 Reviewers and 2 Challengers verified tests, builds, domain clean state, modal and UX behavior | M2 | **DONE** |
| M4 | Forensic Audit & Artifact Generation | Forensic Auditor verified integrity and compiled master AUDIT_AND_FIX_REPORT.md artifact | M3 | **DONE** |
| M5 | Production EC2 Deployment | Deploying verified codebase to EC2, restarting systemd, verifying live endpoints | M4 | **DONE** |
| M6 | Victory Audit Remediation Investigation | Explorer investigating full test suite failure & app.py:9615 NameError regression | M5 | **IN_PROGRESS** |
