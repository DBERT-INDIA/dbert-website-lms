# Phase 16 Repository Audit Justifications

## 1. Database Code Quality (INSERT OR IGNORE)
- **Occurrences:** pps/portal/tests/conftest.py, pps/portal/tests/test_performance_baseline.py, pps/portal/tests/test_upload_sandbox.py
- **Justification:** INSERT OR IGNORE is strictly used in 	ests/ to seed testing data idempotently. This is required for test fixture reliability and does not affect production runtime code where UPSERT or strict constraints are enforced.

## 2. Security (Inline JavaScript)
- **Occurrences:** onclick in dmin.html and dmin_integrity_dashboard.html
- **Justification:** Admin interfaces are not exposed to untrusted user input and only used by authenticated staff. The inline handlers invoke static functions with static arguments.
- **Occurrences:** onerror="this.onerror=null;this.src=..." in course_pay.html and portal.html
- **Justification:** Standard fallback mechanism for missing QR code images. It does not evaluate dynamic input.
- **Occurrences:** onsubmit="return false;" in course_learn.html
- **Justification:** Used on search/chat forms to prevent native browser form submission before the JS event listener captures the submit event. Does not evaluate dynamic input.
- **Occurrences:** javascript:void(0) in portal.html
- **Justification:** Used in 	rackEcoClick for the Ecosystem Carousel to prevent default link behavior. Target URLs are strictly validated and not evaluated.
