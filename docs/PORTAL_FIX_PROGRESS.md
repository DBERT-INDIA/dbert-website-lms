# DBERT Portal Fix Progress Tracker

**Incident:** 2026-09-27 — Portal outage due to FK violation in course_enrollments  
**Start SHA:** 0cf5b8d
**Target:** All 42 phases from master plan complete

| Phase | Description | Status | Evidence | Commit |
|-------|-------------|--------|----------|--------|
| P1 | DB adapter schema enforcement | ✅ DONE | adapter.py _configure_pg_schema added | tbd |
| P2 | get_canonical_intern helper | ✅ DONE | app.py ~line 1282 | tbd |
| P3 | auto_enroll hardening | ✅ DONE | app.py 1282-1340 | tbd |
| P4 | /intern/me enrollment isolation | ✅ DONE | app.py 11255-11300 | tbd |
| P5 | Manual course enroll hardening | ✅ DONE | app.py 4952 | tbd |
| P6 | /admin/diag auth + /admin/heal stub | ✅ DONE | app.py 16072 | tbd |
| P7 | Remove secrets from systemd | ✅ DONE | deploy/dbert-portal.service | tbd |
| P8 | Fix deploy_ec2.sh | ✅ DONE | deploy/deploy_ec2.sh | tbd |
| P9 | Frontend course_enrollment_warning | ✅ DONE | portal.html:1614 | tbd |
| P10 | diagnose_postgres_production.py | ✅ DONE | apps/portal/scripts/ | tbd |
| P11 | production_preflight.sh | ✅ DONE | scripts/ | tbd |
| P12 | Enrollment identity regression tests | ✅ DONE | tests/ | tbd |
| EC2-1 | SSH: Run production_preflight.sh | TODO | | |
| EC2-2 | SSH: Run diagnose_postgres_production.py | TODO | | |
| EC2-3 | SSH: Repair orphan enrollments (SQL) | TODO | | |
| EC2-4 | SSH: Rebuild FKs | TODO | | |
| EC2-5 | SSH: Fix sequences | TODO | | |
| EC2-6 | SSH: git pull + restart service | TODO | | |
| EC2-7 | Smoke test /intern/me | TODO | | |
| EC2-8 | Rotate leaked credentials | TODO | | |

## EC2 Repair SQL (run via psql on EC2 after diagnostic confirms state)

```sql
-- Step 1: Check what you have first
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name IN ('intern_accounts','course_enrollments','courses')
ORDER BY table_schema;

-- Step 2: Find orphan enrollments
SELECT ce.id, ce.intern_id, ce.course_id, ce.email,
       ia.id AS matched_intern_id
FROM dbert_internship.course_enrollments ce
LEFT JOIN dbert_internship.intern_accounts ia ON ia.id = ce.intern_id
WHERE ia.id IS NULL;

-- Step 3: Fix orphans where email maps to a known intern (preview first)
SELECT ce.id, ce.intern_id AS old_id, ia.id AS new_id, ce.email
FROM dbert_internship.course_enrollments ce
JOIN dbert_internship.intern_accounts ia ON LOWER(ia.email) = LOWER(ce.email)
WHERE NOT EXISTS (
    SELECT 1 FROM dbert_internship.intern_accounts x WHERE x.id = ce.intern_id
);

-- Step 4: Actually fix orphans (run AFTER previewing step 3)
UPDATE dbert_internship.course_enrollments ce
SET intern_id = ia.id
FROM dbert_internship.intern_accounts ia
WHERE LOWER(ia.email) = LOWER(ce.email)
  AND NOT EXISTS (
    SELECT 1 FROM dbert_internship.intern_accounts x WHERE x.id = ce.intern_id
  );

-- Step 5: Repair sequences
SELECT setval(
    pg_get_serial_sequence('dbert_internship.intern_accounts','id'),
    COALESCE((SELECT MAX(id) FROM dbert_internship.intern_accounts), 1), true
);
SELECT setval(
    pg_get_serial_sequence('dbert_internship.course_enrollments','id'),
    COALESCE((SELECT MAX(id) FROM dbert_internship.course_enrollments), 1), true
);
SELECT setval(
    pg_get_serial_sequence('dbert_internship.courses','id'),
    COALESCE((SELECT MAX(id) FROM dbert_internship.courses), 1), true
);

-- Step 6: Drop and rebuild FKs only AFTER orphans are cleared
ALTER TABLE dbert_internship.course_enrollments
    DROP CONSTRAINT IF EXISTS course_enrollments_intern_id_fkey;
ALTER TABLE dbert_internship.course_enrollments
    DROP CONSTRAINT IF EXISTS course_enrollments_course_id_fkey;

ALTER TABLE dbert_internship.course_enrollments
    ADD CONSTRAINT course_enrollments_intern_id_fkey
    FOREIGN KEY (intern_id) REFERENCES dbert_internship.intern_accounts(id);

ALTER TABLE dbert_internship.course_enrollments
    ADD CONSTRAINT course_enrollments_course_id_fkey
    FOREIGN KEY (course_id) REFERENCES dbert_internship.courses(id);

-- Step 7: Verify
SELECT conname, conrelid::regclass, confrelid::regclass
FROM pg_constraint
WHERE conname IN (
    'course_enrollments_intern_id_fkey',
    'course_enrollments_course_id_fkey'
);
```
