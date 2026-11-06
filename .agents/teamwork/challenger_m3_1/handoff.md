# Milestone 3 Empirical Challenge Report: Domain Migration & Database Integrity

**Agent**: `challenger_m3_1` (Critic & Empirical Challenger)  
**Parent Orchestrator Conversation ID**: `d66c654e-a32e-4bd2-a554-e6ecbf8cc20c`  
**Timestamp**: 2026-11-04T08:55:00Z  
**Verdict**: **PASS / PRODUCTION-READY** (with 2 minor informational observations on gitignored local test artifacts)

---

## 1. Observation

### 1.1 Domain Reference Sweep across 3,609 Files
An exhaustive multi-pattern regex and binary sweep across all 3,609 files in the repository (excluding `.git/`, `.next/`, `node_modules/`, `__pycache__/`) scanned for:
- Plain case-insensitive `dbert.online`
- URL-encoded strings `%64%62%65%72%74%2[eE]%6[fF]%6[eE]%6[cC]%69%6[eE]` and `dbert%2eonline`
- Hex-encoded byte patterns `64626572742e6f6e6c696e65`
- Base64 variations (`ZGJlcnQub25saW5l`, `ZGJlcnQub25saW5`, `GJlcnQub25saW5l`)
- Subdomains (`[a-zA-Z0-9_-]{1,40}\.dbert\.online`)

**Results**:
- URL-encoded / Hex / Base64: **0** occurrences across all production source files, databases, templates, and configurations.
- Plain `dbert.online` / subdomains: All occurrences fall strictly into one of four well-defined buckets:
  1. **Intentional 301 Permanent Redirects**:
     - `deploy/dbert-unified-nginx.conf:31,45,61,73`
     - `apps/website/.htaccess:13-14`
     - `apps/website/public/.htaccess:13-14`
     - `cpanel_public_html/.htaccess:13-14`
     - `dbert-api-package/website-content/public/.htaccess:12-14`
  2. **Certbot SAN Deployment Configuration**:
     - `deploy/deploy_ec2_unified.sh:229`: Instruction argument `sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in -d api.dbert.in -d dbert.online -d www.dbert.online -d internship.dbert.online` necessary to obtain certificates so that legacy HTTPS traffic can be received and 301-redirected.
  3. **Historical Planning / Analysis Markdown**:
     - Pre-existing planning docs (`DBERT_LMS_MASTER_DEVELOPMENT_HARDENING_PLAN.md`, `DBERT_WEBSITE_UIUX_REDESIGN_PHASE_PLAN.md`, `ORIGINAL_REQUEST.md`, `QA_REPORT.md`, `WEBSITE_ROUTE_INVENTORY.md`, `WEBSITE_UIUX_PHASE_PLAN.md`, `WEBSITE_UIUX_PRODUCTION_PREFLIGHT.md`, `WEBSITE_UIUX_PROGRESS.md`, `.agent/FINAL_RELEASE_GATE_REPORT.md`, `deploy/FILEZILLA_DEPLOYMENT_GUIDE.md`, `deploy/FIRST_TIME_EC2_DEPLOYMENT.md`), `.agents/teamwork/` metadata logs, and the sanitizer script `scripts/sanitize_sqlite_domains.py`.
  4. **Gitignored Test Artifacts**:
     - `apps/portal/cgi-bin/internship.db`: Ignored by `.gitignore:12` (`apps/portal/cgi-bin/*.db*`). Contains 1 record in `staff_accounts.email`: `dbert_superadmin@dbert.online`.
     - `test_portal.db`: Ignored by `.gitignore:3` (`*.db*`). Contains 2 records in `application_status_history.changed_by`: `staff@dbert.online`, `admin@dbert.online`.

### 1.2 Syntax and Logic Verification of 301 Redirect Blocks
1. **Nginx Configuration (`deploy/dbert-unified-nginx.conf`)**:
   - Port 80 (HTTP) Block 1 (lines 28–40):
     ```nginx
     server {
         listen 80;
         listen [::]:80;
         server_name dbert.online www.dbert.online;
         location /.well-known/acme-challenge/ { root /var/www/certbot; }
         location / { return 301 https://dbert.in$request_uri; }
     }
     ```
   - Port 80 (HTTP) Block 2 (lines 42–54):
     ```nginx
     server {
         listen 80;
         listen [::]:80;
         server_name internship.dbert.online;
         location /.well-known/acme-challenge/ { root /var/www/certbot; }
         location / { return 301 https://lms.dbert.in$request_uri; }
     }
     ```
   - Port 443 (HTTPS) Block 1 (lines 58–67):
     ```nginx
     server {
         listen 443 ssl http2;
         listen [::]:443 ssl http2;
         server_name dbert.online www.dbert.online;
         ssl_certificate /etc/letsencrypt/live/dbert.in/fullchain.pem;
         ssl_certificate_key /etc/letsencrypt/live/dbert.in/privkey.pem;
         return 301 https://dbert.in$request_uri;
     }
     ```
   - Port 443 (HTTPS) Block 2 (lines 70–79):
     ```nginx
     server {
         listen 443 ssl http2;
         listen [::]:443 ssl http2;
         server_name internship.dbert.online;
         ssl_certificate /etc/letsencrypt/live/dbert.in/fullchain.pem;
         ssl_certificate_key /etc/letsencrypt/live/dbert.in/privkey.pem;
         return 301 https://lms.dbert.in$request_uri;
     }
     ```
   - **Assessment**: Syntactically valid. Includes ACME challenge paths for non-disruptive SSL renewal. Accurately preserves query string and URI via `$request_uri`.

2. **Apache `.htaccess` Rewrite Rules**:
   - Lines 12–14:
     ```apache
     # 1. 301 Permanent Redirect from legacy dbert.online -> dbert.in
     RewriteCond %{HTTP_HOST} ^(www\.)?dbert\.online$ [NC]
     RewriteRule ^(.*)$ "https://dbert.in/$1" [R=301,L]
     ```
   - **Assessment**: Correct regex capture, case-insensitive host matching, standard 301 permanent redirect flag `[R=301,L]`.

### 1.3 Database Integrity Probe
Direct Python SQLite probing (`integrity_check`, `foreign_key_check`, `freelist_count`, and deep text column iteration) was executed across the three primary databases:
1. `internship.db` (root, 856,064 bytes, 68 tables):
   - `PRAGMA integrity_check`: `[('ok',)]`
   - `PRAGMA foreign_key_check`: **0 violations**
   - `PRAGMA freelist_count`: **0 free pages** (100% vacuumed)
   - Table/Column SQL matches for `dbert.online`: **0**
   - Raw binary bytes matching `b"dbert.online"`: **0**
2. `apps/portal/internship.db` (37,740,544 bytes, 77 tables):
   - `PRAGMA integrity_check`: `[('ok',)]`
   - `PRAGMA foreign_key_check`: **0 violations**
   - `PRAGMA freelist_count`: **0 free pages** (100% vacuumed)
   - Table/Column SQL matches for `dbert.online`: **0**
   - Raw binary bytes matching `b"dbert.online"`: **0**
3. `dbert-api-package/databases/internship.db` (32,784,384 bytes, 75 tables):
   - `PRAGMA integrity_check`: `[('ok',)]`
   - `PRAGMA foreign_key_check`: **0 violations**
   - `PRAGMA freelist_count`: **0 free pages** (100% vacuumed)
   - Table/Column SQL matches for `dbert.online`: **0**
   - Raw binary bytes matching `b"dbert.online"`: **0**

### 1.4 Distribution Package Archive Probe (`dbert-api-package-v1.zip`)
Direct programmatic inspection of `dbert-api-package-v1.zip` (8,858,794 bytes):
- Total archived entries: **342** files.
- Files matching `dbert.online`: **1 file** (`dbert-api-package/website-content/public/.htaccess`).
- Inspection of matching line: Line 12 `# 1. 301 Permanent Redirect from legacy dbert.online -> dbert.in` (an intentional comment explaining the redirect rule).
- Embedded SQLite database `dbert-api-package/databases/internship.db` inside archive:
  - Raw binary count of `b"dbert.online"`: **0**
  - `PRAGMA integrity_check`: `[('ok',)]`
  - `PRAGMA foreign_key_check`: **0 violations**
  - `PRAGMA freelist_count`: **0 free pages**
  - SQL table/column matches: **0**

### 1.5 Automated Test Suite Execution
- `apps/portal/tests/test_mobile_accessibility.py`: **18 passed** in 0.68s.
- `apps/portal/tests/test_ux_dead_ends.py`: **13 passed** in 3.42s.
- `apps/portal/tests/test_auth.py`: **4 passed** in 1.15s.
- `apps/portal/tests/test_application_state_machine.py`: **7 passed** in 2.34s.
- Total portal tests: **42 passed, 0 failed**.
- `npm --prefix apps/website run audit:headings`: **71 pages audited; 0 heading violations**.

---

## 2. Logic Chain

1. **R1 Domain Eradication**:
   - Observation 1.1 demonstrates that zero active runtime files, templates, scripts, or assets contain `dbert.online` or its subdomains.
   - Observation 1.1 demonstrates that no obfuscated or URL-encoded variations (`%64%62%65%72%74%2E%6F%6E%6C%69%6E%65`, hex, base64) exist in code.
   - Therefore, the codebase is free of functional legacy domain links.
2. **Redirect Correctness**:
   - Observation 1.2 demonstrates that both HTTP (port 80) and HTTPS (port 443) redirect blocks exist in `dbert-unified-nginx.conf` and Apache `.htaccess`.
   - The targets explicitly map:
     - `dbert.online` and `www.dbert.online` $\rightarrow$ `https://dbert.in$request_uri`
     - `internship.dbert.online` $\rightarrow$ `https://lms.dbert.in$request_uri`
   - Therefore, incoming traffic on legacy domains will preserve URI paths and arrive at official production endpoints with a 301 permanent redirect.
3. **Database Consistency & Compaction**:
   - Observation 1.3 shows that across all 3 primary SQLite databases (`internship.db`, `apps/portal/internship.db`, `dbert-api-package/databases/internship.db`), foreign keys report 0 violations, schemas pass `integrity_check`, and `freelist_count` is 0.
   - Furthermore, raw byte scans return 0 hits for `b"dbert.online"`, proving that vacuuming removed all residual strings from deleted/overwritten B-tree cells.
   - Therefore, database integrity is fully verified.
4. **Distribution Package Purity**:
   - Observation 1.4 confirms that `dbert-api-package-v1.zip` contains 342 sanitized files with zero unmigrated code references, and its embedded database is identically clean.
   - Therefore, the distribution package is safe for release.

---

## 3. Caveats

1. **Gitignored Local Database Artifacts**:
   - `apps/portal/cgi-bin/internship.db` (gitignored legacy CGI artifact) has 1 obsolete row (`dbert_superadmin@dbert.online`). It is ignored by git and not referenced by the Gunicorn app (`apps/portal/app.py` references `apps/portal/internship.db`).
   - `test_portal.db` (gitignored test fixture) has 2 historical rows (`staff@dbert.online`, `admin@dbert.online`).
   - These do not affect production deployments.
2. **Live EC2 Deployment**:
   - This audit verified static code, configurations, SQLite databases, and package archives locally. Live DNS resolution, live ACME cert issuance, and live HTTP response verification on the production host `3.26.237.171` must be completed during the deployment phase.

---

## 4. Conclusion

The domain migration and database remediation performed by Worker M2 is **EMPIRICALLY VERIFIED AND APPROVED**.
- **Domain Eradication**: Complete. All surviving references are intentional 301 redirects, Certbot SAN instructions, or historical markdown docs.
- **301 Redirects**: Verified syntactically correct and pointing to `https://dbert.in$request_uri` and `https://lms.dbert.in$request_uri`.
- **Database Integrity**: Passed all checks (`integrity_check: ok`, `foreign_key_check: 0`, `freelist_count: 0`, 0 legacy domain traces).
- **Package Archive**: `dbert-api-package-v1.zip` verified clean (342 files, 0 unintended domain references, vacuumed DB).
- **Portal Tests**: All 42 tests passed with 0 failures.

---

## 5. Verification Method

To independently reproduce the empirical findings in this report:

1. **Verify Database Integrity and Zero Legacy Domain Strings**:
   ```powershell
   python -c "
   import sqlite3, os
   for path in ['internship.db', 'apps/portal/internship.db', 'dbert-api-package/databases/internship.db']:
       conn = sqlite3.connect(path)
       cur = conn.cursor()
       cur.execute('PRAGMA integrity_check;')
       assert cur.fetchall() == [('ok',)], f'Integrity fail on {path}'
       cur.execute('PRAGMA foreign_key_check;')
       assert cur.fetchall() == [], f'FK fail on {path}'
       cur.execute('PRAGMA freelist_count;')
       assert cur.fetchone()[0] == 0, f'Freelist fail on {path}'
       with open(path, 'rb') as f:
           assert b'dbert.online' not in f.read().lower(), f'String leak in {path}'
       conn.close()
   print('All 3 databases verified 100% clean, valid, and vacuumed.')
   "
   ```

2. **Verify Distribution Package Archive**:
   ```powershell
   python -c "
   import zipfile
   with zipfile.ZipFile('dbert-api-package-v1.zip') as z:
       files = [f for f in z.namelist() if not f.endswith('/')]
       assert len(files) == 342, f'Expected 342 files, got {len(files)}'
       leaks = [f for f in files if b'dbert.online' in z.read(f).lower() and not f.endswith('.htaccess')]
       assert len(leaks) == 0, f'Leaks in zip: {leaks}'
   print('Package zip verified: 342 files, 0 unintended domain references.')
   "
   ```

3. **Verify Portal Test Suite**:
   ```powershell
   cd apps/portal
   python -m pytest tests/test_mobile_accessibility.py tests/test_ux_dead_ends.py tests/test_auth.py tests/test_application_state_machine.py -v
   cd ../..
   ```
   *Expected*: All 42 tests pass with exit code 0.

4. **Verify Nginx Redirect Syntax**:
   Inspect lines 28–79 in `deploy/dbert-unified-nginx.conf` and confirm `return 301 https://dbert.in$request_uri;` and `return 301 https://lms.dbert.in$request_uri;`.
