# Dispatch for Explorer R4: EC2 Deployment Configuration Audit

Objective: Audit deploy/ directory for Nginx unified config, systemd service files, deploy_ec2_unified.sh hardcoded password, production_preflight.sh variable expansion bug, and port safety.
Working Directory: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r4
Original Request: c:\Users\user\Desktop\dbert-website-lms\ORIGINAL_REQUEST.md
Report Destination: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r4\handoff.md

## 2026-10-25T22:49:16Z
sender=3a4d7ac2-699c-47ca-9101-c0e51547ba94 priority=MESSAGE_PRIORITY_HIGH
content=You are explorer_r4 (Role: Deployment Configuration Auditor).
Your working directory is: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r4
The project workspace root is: c:\Users\user\Desktop\dbert-website-lms
You MUST read: c:\Users\user\Desktop\dbert-website-lms\ORIGINAL_REQUEST.md

Your task is requirement R4 from ORIGINAL_REQUEST.md:
Audit `deploy/` directory:
1. Nginx unified config (dbert-unified-nginx.conf): All server_name, SSL cert paths, upstream proxy_pass URLs correct for dbert.in. Confirm intentional redirect blocks for dbert.online -> dbert.in and internship.dbert.online -> lms.dbert.in are syntactically correct.
2. Systemd service files: Check WorkingDirectory, ExecStart, User/Group — no old domain references, paths match expected EC2 layout (/var/www/dbert-website-lms/).
3. Deploy script (deploy_ec2_unified.sh): Verify committed DB password DBERT_SECURE_PASSWORD_123 (blocker) and document the exact fix. Check certbot command covers dbert.in, www.dbert.in, and lms.dbert.in in SAN.
4. production_preflight.sh variable expansion bug: Find all occurrences where the script uses single-quoted strings like '${REQUIRE_POSTGRES:-}' inside a check function — single quotes prevent shell expansion, so every check always sees the literal string '${REQUIRE_POSTGRES:-}' and silently passes. Enumerate all occurrences with line numbers and document the fix (use double quotes).
5. Port safety: Next.js :3001 and Gunicorn :5001 — confirm no conflicts with system services.

Requirements for output:
For EVERY finding, cite the exact relative file path and line number, classification (Blocker/Warning/Info), explanation, and recommended fix.
Write your complete, self-contained report to:
c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r4\handoff.md
Update c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r4\progress.md as you work.
When done, notify orchestrator via send_message with a brief summary and path to your handoff.md.
