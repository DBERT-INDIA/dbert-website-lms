# TEST RESULTS

## Baseline Run (2026-09-25)
- **Total Tests:** 347
- **Passed:** 344
- **Failed:** 3
- **Duration:** 148.94s

### Baseline Failures Noted
1. `tests/e2e/test_phase10_workflows.py::test_intern_auth_workflow[chromium]`
   - SMTP sender authentication error logged (`530 5.7.0 Authentication Required`) via direct SMTP attempt.
2. `tests/learning/test_characterization.py::TestGuidedLearningCharacterization::test_chat_without_csrf_returns_403`
   - Expected 403 status code for unauthenticated chat, received 401 UNAUTHORIZED.
3. `tests/security/test_security_regression.py::TestCSRFDefenseEnforcement::test_cron_endpoint_with_valid_secret_is_csrf_exempt`
   - Cron endpoint `/cron/clean-tokens` failed CSRF exempt check with HTTP 403.
