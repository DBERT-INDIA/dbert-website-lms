# DBERT website and learning portal

DBERT supports course learning, mentorship, credential verification, and internship hiring. This implementation connects course cohorts to a source-grounded study classroom, mentor follow-ups, and credentials tied to learner progress.

## What you can do

| Role | Workflow |
| --- | --- |
| Learner | Join a course cohort or its waitlist. Ask questions about the course, open citations at the relevant lesson section, keep private notes, and add questions to the dashboard review queue. Track milestones and claim a credential once the requirements are met. |
| Mentor | View assigned cohort rosters and progress. Use aggregate lesson activity to identify topics for follow-up. Assign a follow-up to the cohort or leave a private check-in for a learner. |
| Admin | Create course cohorts with dates, capacity, and assigned mentors. Manage registration and waitlists, configure milestones, issue eligible cohort credentials, and inspect staff activity and platform health. |
| Visitor or employer | Discover courses and opportunities, check a résumé against a target role, verify public credentials, and use the employer workflow to track applicants. |

The study classroom has Study Trail, Tutor Chat, and Lecture panels on desktop and tabs on mobile. It uses course excerpts by default. A configured portal can enable optional Gemini responses with `STUDY_CLASSROOM_USE_GEMINI=true` and a learner-supplied key.

Cohort milestones can use passed quizzes, approved capstones, distinct lessons discussed, and course completion. Completion requires an approved capstone for courses that require one. Cohort credentials appear in the existing wallet alongside ordinary course certificates.

## Repository layout

| Path | Contents |
| --- | --- |
| [apps/portal](apps/portal) | Flask learning portal, staff and mentor tools, Jinja templates, and portal tests |
| [apps/website](apps/website) | Next.js public website, course discovery, résumé checker, and certificate verification |
| [scripts/verify_offline.py](scripts/verify_offline.py) | Offline checks for the portal and website |

## Run locally

### Learning portal

Use Python 3.10 or later. From the repository root in PowerShell, create a virtual environment and install the portal dependencies.

```powershell
python -m venv ../dbert-venv
$dbertPython = (Resolve-Path ..\dbert-venv\Scripts\python.exe).Path
& $dbertPython -m pip install -r apps/portal/requirements-dev.txt
Set-Location apps/portal
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

For a local SQLite instance, set `FLASK_DEBUG=true` and `DB_FILE=internship.db` in the portal's `.env` and leave `DATABASE_URL` unset. Set your own development values for `FLASK_SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `ADMIN_KEY`. Set `EMAILS_ENABLED=false` for the local demo.

```powershell
& $dbertPython -m flask --app app run --host 127.0.0.1 --port 5000
```

Open `http://127.0.0.1:5000`. The cohort demo uses a local admin account, an assigned mentor account, and two synthetic learners already enrolled in the course.

### Public website

Use Node.js 22.12 or later in the 22.x line, or Node.js 24 LTS. In a second terminal, run these commands from the repository root.

```powershell
Set-Location apps/website
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
npm ci
npm run dev -- --hostname 127.0.0.1
```

Open `http://127.0.0.1:3000`. Public pages can build without a database. For features that store form submissions or manage records, configure `DATABASE_URL` for a disposable PostgreSQL database and initialize its schema with `npx prisma db push` from `apps/website`. Set `LMS_INTERNAL_URL=http://127.0.0.1:5000` to use the local portal for résumé scans.

### Enrollment payment claims

The website sends payment claims for the deposit and legacy balance flows to the Flask portal. Set the same randomly generated, server-only `INTERNAL_SYNC_SECRET` in both services. Set `INTERNAL_LMS_SYNC_URL` on the website to the portal's full `/api/internal/enrollment-sync` endpoint. The website's example points to the local portal on port 5000. For Vercel, use the HTTPS endpoint of the portal assigned to that deployment and set the secret in the same Vercel environment.

Roll out the portal endpoint and configure both services before switching the website payment forms. The website acknowledges submissions after the portal returns a saved claim receipt.

On EC2, set the shared secret in the website and portal `.env` files used by the systemd services.

## Production architecture

Nginx routes `dbert.in` to the standalone Next.js website and `lms.dbert.in` to the Gunicorn-hosted Flask portal. Production uses PostgreSQL. The [deployment directory](deploy) contains Nginx and systemd configuration. See the [engineering playbook](AGENTS.md) for the application lifecycle and production workflows.

## Demo walkthrough

1. Open `/admin/program-cohorts` as an admin. Create a cohort with one seat, assign a mentor, and define a milestone.
2. From `/program-cohorts`, join as the first learner and waitlist the second. Raise the capacity to two to show promotion.
3. In the course's **Study classroom**, ask about a lesson, open a citation, save a note, and flag a question for review. Reload to show the saved work.
4. Open `/mentor/program-cohorts` as the assigned mentor. Review cohort progress and assign a lesson follow-up.
5. Meet the required milestones, claim the cohort credential, and open it from `/account/credentials`.

See the [cohort and classroom report](COHORT_CLASSROOM_IMPLEMENTATION.md) for the full video walkthrough.

## Verification

From the repository root, run the following with the development environment's Python interpreter and Node.js on your path. Install Playwright's Chromium with `python -m playwright install chromium` if you plan to run the browser checks.

```powershell
python -B scripts/verify_offline.py
python -B scripts/verify_offline.py --browser
```

The portal checks use synthetic data and SQLite, with a simulated PostgreSQL connection for startup checks. Verify live PostgreSQL, payment, and Gemini integrations in a configured staging environment.

## Implementation reports

- [Platform improvements](IMPLEMENTATION_REPORT.md) covers the earlier changes to enrollment, payments, navigation, assessments, capstones, mentoring, support, hiring, and credentials.
- [Cohorts, study classroom, and verification](COHORT_CLASSROOM_IMPLEMENTATION.md) explains the original gaps, how the current workflows operate, and the bugs fixed during verification.
