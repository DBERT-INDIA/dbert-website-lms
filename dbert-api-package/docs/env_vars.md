# DBERT Environment Variables Reference
> Complete audit of all environment variables across `app.py`, `services/`, and `routes/`.

| Variable Name | Default Value in Code | Required in Production | Description |
|---|---|---|---|
| `ACCESS_TTL` | `3600` | NO | Environment configuration parameter |
| `ADMIN_KEY` | `dbert_admin_2026` | NO | Environment configuration parameter |
| `ADMIN_PASSWORD` | `dbert_admin_2026` | YES | Environment configuration parameter |
| `ADMIN_USERNAME` | `dbert_admin` | NO | Environment configuration parameter |
| `ADSENSE_PUB_ID` | `pub-1320532532258767` | NO | Environment configuration parameter |
| `AMBASSADOR_ENABLED` | `0` | NO | Environment configuration parameter |
| `AWS_SES_REGION` | `os.environ.get("AWS_REGION", "us-east-1` | NO | Environment configuration parameter |
| `COOKIE_SECURE` | `1" if is_prod else "0` | NO | Environment configuration parameter |
| `CPANEL_EMAIL_API_KEY` | `` | NO | Environment configuration parameter |
| `CPANEL_EMAIL_API_URL` | `https://mailer.aivaratech.online/send` | NO | Environment configuration parameter |
| `CRON_SECRET` | `` | NO | Environment configuration parameter |
| `CSP_ALLOW_INLINE` | `0` | NO | Environment configuration parameter |
| `CSP_ENFORCE` | `1` | NO | Environment configuration parameter |
| `DATABASE_URL` | `None` | YES | Environment configuration parameter |
| `DB_FILE` | `` | NO | Environment configuration parameter |
| `DISABLE_RATE_LIMIT` | `None` | NO | Environment configuration parameter |
| `EMAILS_ENABLED` | `true` | NO | Environment configuration parameter |
| `EMAIL_PROVIDER` | `smtp` | NO | Environment configuration parameter |
| `ENROLLMENT_DEADLINE` | `2026-12-31` | NO | Environment configuration parameter |
| `FERNET_KEY` | `` | YES | Environment configuration parameter |
| `FLASK_DEBUG` | `false` | NO | Environment configuration parameter |
| `FLASK_ENV` | `None` | NO | Environment configuration parameter |
| `FLASK_SECRET_KEY` | `` | YES | Environment configuration parameter |
| `FORCE_RECONCILE` | `None` | NO | Environment configuration parameter |
| `FROM_EMAIL` | `contactus@dbert.online` | NO | Environment configuration parameter |
| `FROM_NAME` | `DBERT Support` | NO | Environment configuration parameter |
| `GA4_API_SECRET` | `` | NO | Environment configuration parameter |
| `GA4_ID` | `G-GZ17KZ7MDW` | NO | Environment configuration parameter |
| `GEMINI_API_KEY` | `` | NO | Environment configuration parameter |
| `GEMINI_API_KEYS` | `` | NO | Environment configuration parameter |
| `GEMINI_MODEL` | `gemini-3.1-flash-lite` | NO | Environment configuration parameter |
| `GEMINI_TIMEOUT` | `8` | NO | Environment configuration parameter |
| `GEMINI_TOTAL_BUDGET` | `30` | NO | Environment configuration parameter |
| `GITHUB_TIMEOUT` | `6` | NO | Environment configuration parameter |
| `GITHUB_TOKEN` | `` | NO | Environment configuration parameter |
| `GOOGLE_INDEXING_SA_JSON` | `` | NO | Environment configuration parameter |
| `GUIDED_LEARNING_V2` | `` | NO | Environment configuration parameter |
| `INDEXNOW_KEY` | `` | NO | Environment configuration parameter |
| `INTERVIEW_COOLING_HOURS` | `24` | NO | Environment configuration parameter |
| `INTERVIEW_ENABLED` | `true` | NO | Environment configuration parameter |
| `INTERVIEW_MAX_ATTEMPTS` | `2` | NO | Environment configuration parameter |
| `INTERVIEW_NUM_QUESTIONS` | `4` | NO | Environment configuration parameter |
| `LOGO_URL` | `` | NO | Environment configuration parameter |
| `MASTERCLASS_DISCORD_URL` | `https://discord.gg/dbert` | NO | Environment configuration parameter |
| `MASTERCLASS_WHATSAPP_URL` | `https://chat.whatsapp.com/invite/DBERTDataAnalystMasterclass` | NO | Environment configuration parameter |
| `MAX_APPLICATIONS_PER_PERSON` | `3` | NO | Environment configuration parameter |
| `OG_IMAGE_URL` | `` | NO | Environment configuration parameter |
| `ONESIGNAL_APP_ID` | `1b181bc1-46b8-4359-ac7a-e87ecab91be4` | NO | Environment configuration parameter |
| `ONESIGNAL_REST_API_KEY` | `` | NO | Environment configuration parameter |
| `PAID_PROGRAM_AMOUNT` | `1599` | NO | Environment configuration parameter |
| `POSTGRES_SCHEMA` | `dbert_internship` | NO | Environment configuration parameter |
| `RAZORPAY_ENABLED` | `1` | NO | Environment configuration parameter |
| `RAZORPAY_KEY_ID` | `` | NO | Environment configuration parameter |
| `RAZORPAY_KEY_SECRET` | `` | NO | Environment configuration parameter |
| `RAZORPAY_WEBHOOK_SECRET` | `` | NO | Environment configuration parameter |
| `RECAPTCHA_SECRET_KEY` | `` | NO | Environment configuration parameter |
| `REFRESH_TTL` | `str(60 * 24 * 3600` | NO | Environment configuration parameter |
| `REQUIRE_POSTGRES` | `false` | NO | Environment configuration parameter |
| `SESSION_DAYS` | `30` | NO | Environment configuration parameter |
| `SITE_ORIGIN` | `https://internship.dbert.online` | NO | Environment configuration parameter |
| `SMTP_BACKUP_HOST` | `dbert.info` | NO | Environment configuration parameter |
| `SMTP_BACKUP_PASS` | `` | NO | Environment configuration parameter |
| `SMTP_BACKUP_PORT` | `465` | NO | Environment configuration parameter |
| `SMTP_BACKUP_USER` | `contactus@dbert.info` | NO | Environment configuration parameter |
| `SMTP_HOST` | `dbert.online` | NO | Environment configuration parameter |
| `SMTP_PASS` | `` | NO | Environment configuration parameter |
| `SMTP_PORT` | `465` | NO | Environment configuration parameter |
| `SMTP_USER` | `contactus@dbert.online` | NO | Environment configuration parameter |
| `TESTING` | `None` | NO | Environment configuration parameter |
| `TURNSTILE_ENABLED` | `false` | NO | Environment configuration parameter |
| `TURNSTILE_SECRET` | `` | NO | Environment configuration parameter |
| `TURNSTILE_SITEKEY` | `` | NO | Environment configuration parameter |
| `UPI_AMOUNT` | `499` | NO | Environment configuration parameter |
| `UPI_ID` | `Q681021429@ybl` | NO | Environment configuration parameter |
| `UPLOAD_FOLDER` | `uploads` | NO | Environment configuration parameter |