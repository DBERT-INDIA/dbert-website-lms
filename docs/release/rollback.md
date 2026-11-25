# DBERT Fellowship Remediation — Rollback Plan

- **Baseline Commit SHA:** `4bfa105a84ae468c1afbf7e72cf0f32f0208fcd1` (on `main`)
- **Feature Branch:** `fix/fellowship-landing-pages`
- **Backend / Database Changes:** None. Zero migrations, zero API contract changes.
- **Deployment Status:** Not deployed to EC2.

## How to Rollback
1. **Local Git Rollback:**
   ```bash
   git checkout main
   ```
   Or if merged and needing revert:
   ```bash
   git revert --no-commit <merge-commit-sha>
   ```
2. **Production EC2 Rollback (if ever deployed):**
   - Checkout `4bfa105a84ae468c1afbf7e72cf0f32f0208fcd1` in `/var/www/dbert-website-lms`.
   - Rebuild Next.js standalone (`npm run build`), sync `public/` and `data/` symlink, and run `sudo systemctl restart dbert-website.service`.
   - Verify `https://dbert.in/learners/courses` and `https://dbert.in/learners/fellowship` return HTTP 200.
