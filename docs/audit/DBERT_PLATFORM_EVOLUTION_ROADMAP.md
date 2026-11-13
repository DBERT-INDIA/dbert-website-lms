# DBERT Platform Evolution Roadmap

**Purpose:** An implementation brief and phased goal for a local coding agent working on `dbert.in` and `lms.dbert.in`.

**Audit snapshot:** 9 November 2026  
**Primary objective:** Make DBERT a highly trusted, engineering-first AI venture studio, fellowship operator, verified talent network, and internship marketplace.  
**Primary constraint:** Improve the existing system without breaking existing routes, user accounts, application records, credentials, payments, integrations, or production workflows.

> **Execution rule:** This document is a target-state plan, not permission to rewrite the codebase. The agent must inspect the existing repository and runtime first, preserve existing behaviour, implement in small reversible increments, and stop at every human-approval gate described below.

---

## 0. Executive direction

DBERT should not try to become a generic job board, a generic EdTech catalogue, or a clone of a large recruitment company. Its strongest possible position is:

> **A proof-first AI engineering venture studio where learning, real project delivery, mentor review, technical credentials, and hiring evidence are connected end to end.**

The differentiator should be a verifiable **Proof-of-Work Graph**:

`person → application → screening → cohort → mentor → project → issue/task → branch/commit/PR → review → accepted release → competency evidence → credential → talent profile → interview/placement outcome`

Every important claim on the public website should be supported by a real record or link in this graph. Marketing should be the presentation layer of verified operational data, not a manually maintained source of truth.

### 0.1 Outcomes DBERT should aim to lead on

1. **Authentic technical experience:** fellows make attributable, reviewed contributions to real software, not just complete tutorials or copy sample projects.
2. **Mentorship quality:** every active fellow has an identified, available mentor with an explicit review cadence and measurable service level.
3. **Hiring confidence:** employers can inspect relevant, consented evidence of a candidate's skills instead of relying only on CV keywords and certificates.
4. **Trust and transparency:** fees, deposits, stipend rules, employer identity, internship duration, work expectations, and outcomes are unambiguous.
5. **Marketplace quality:** direct employer roles, DBERT project roles, partner roles, and third-party sourced leads are visibly different and correctly categorised.
6. **Research credibility:** DBERT Labs publishes reproducible code, model cards, data/methodology notes, benchmarks, limitations, and valid publication identifiers.
7. **Learner protection:** data is private by default; productive work, IP, attribution, stipends, and partner sharing are governed by written terms.
8. **Operational reliability:** the existing platform remains stable as new features are introduced.

Do not claim that DBERT is “better than every company” as a marketing assertion. Build measurable advantages and let users and employers reach that conclusion from evidence.

---

## 1. Public-site audit: what exists now

This is a public-web review, not a source-code review or a privileged database audit. The agent must verify every item against the local repository and authorised runtime data before changing it.

### 1.1 Domain and product map

| Surface | Current public purpose | Intended responsibility |
|---|---|---|
| `https://dbert.in/` | Corporate identity, venture studio, enterprise AI products, learner pathways, Labs, engineering team, credentials, hiring | Canonical public/marketing/portfolio/trust surface |
| `https://lms.dbert.in/` | LMS, accounts, applications, courses, internship/job listings, student portal, sprint and mentorship navigation | Operational learner and marketplace application |
| `dbert.online` | Public migration notice says this is the deprecated/legacy domain | Do not build new features here; retain/verify redirects only if infrastructure still owns it |

The current migration notice says `dbert.in` is the authoritative website and directs LMS activity to `lms.dbert.in`. Do not casually consolidate the two apps, change DNS, replace hosts, or remove legacy redirects as part of this roadmap.

### 1.2 DBERT business/product domains visible on `dbert.in`

**Venture studio / startup services**
- Hire pre-vetted AI and software engineers.
- Technical assistance and hiring assistance.
- Legal/compliance assistance, AI/ML infrastructure setup, seed funding, equity model, investor network and startup registration/portfolio.
- Startup portfolio includes at least an Alkame case-study page and references to Gayatri AI and Aivara-related work.

**Enterprise and internal products linked from the main navigation**
- DBERT Chat / private LLM.
- Document AI / ingest and OCR.
- Certificate verification API.
- Hiring automation suite.
- Intern management system.
- AI consultant interface, AI readiness assessment, fine-tuning pipeline, DBERT_AI architecture and private model hosting.

**DBERT Labs**
- Multi-agent orchestration.
- Local LLM / edge quantisation.
- RAG evaluation.
- Quantitative/financial ML research.
- Open-source repositories, model weights and technical reports.

**Learner pathway**
- Launchpad (foundation / beginner).
- Accelerate (intermediate / applied AI systems).
- Fellowship (experience / project work).
- AI job/referral pathway.
- Public course pages for AI Agent Development, Generative AI, Machine Learning, Python Automation, Full Stack, Data Analytics and interview preparation.

### 1.3 Current internship and learning domains

Do not collapse all of these into one ambiguous category. The public site currently exposes multiple taxonomies.

| Source | Publicly described tracks/domains |
|---|---|
| `dbert.in` learner menu | AI Agent Development, Generative AI, Machine Learning, Python Automation, Full Stack Development, Data Analytics, Interview Preparation |
| `lms.dbert.in` homepage | AI Agent Development, Data Analyst, Full Stack Development, Python Automation |
| LMS broader listing filters | AI Agent Development, Data Analyst, Full Stack Development, Python Automation, UI/UX Design, DevOps & Cloud, Mobile App Development, Cybersecurity, Digital Marketing |
| Aivara hiring cohort page | AI Agent Development, Full Stack, Python Automation, Data Analytics, Data Engineering/ML |
| Research/product work | RAG, LLM agents, local inference, document AI, ML/quantitative systems, data pipelines, backend APIs, cloud/deployment |

**Recommended canonical engineering taxonomy**

1. `ai-ml`
   - `generative-ai-llm-applications`
   - `rag-search-retrieval`
   - `agentic-systems-tool-use`
   - `llm-evaluation-guardrails`
   - `fine-tuning-model-adaptation`
   - `inference-serving-quantization`
   - `applied-machine-learning`
   - `computer-vision`
   - `nlp-speech`
   - `mlops-llmops`
   - `ai-data-dataset-engineering`
   - `ai-research`
2. `software-engineering`
   - `backend-api`
   - `full-stack`
   - `frontend`
   - `mobile`
   - `qa-test-automation`
3. `data`
   - `data-analytics-bi`
   - `data-engineering-etl`
   - `database-engineering`
4. `platform-infrastructure`
   - `devops-cloud`
   - `sre-platform`
   - `cybersecurity`
5. `automation`
   - `python-automation`
   - `workflow-automation`
6. `design`
   - `ui-ux-product-design`
7. `business-nontechnical`
   - `sales-business-development`
   - `marketing-content`
   - `hr-operations`
   - `campus-ambassador`
   - `program-management`

Keep existing IDs/slugs as compatibility aliases. The canonical taxonomy is an internal normalisation layer first; do not break existing query parameters, saved filters, SEO URLs, category IDs, or application references.

### 1.4 Public internship-marketplace observations

At the audit snapshot, the LMS listing page displayed approximately 6,684 internships. The AI Agent Development page showed 540 listings in one public view. Other cached/public listing views can show different counts as data refreshes. Treat these as dynamic listing counts, **not** counts of DBERT employees, interns, vetted engineers, or verified employers.

The marketplace visibly distinguishes at least:
- `Direct Company Posting`.
- `Curated Sourced Lead`.

Examples shown in the AI Agent Development listing included DBERT/Gayatri AI direct postings such as an AI Coding Assistant Intern and AI Workflow Automation Intern, a DBERT Enterprise AI Agent Integration role, and externally sourced opportunities. The same broad AI category also displayed roles such as campus ambassador, HR, content/marketing, and general business development. This indicates that category tagging and source quality need auditing.

Some role-detail URLs returned an HTTP 500 to the public crawler during this audit. That does not conclusively prove a user-facing production defect, but it creates a concrete test requirement: the local agent must run real browser/API smoke tests against listing detail pages, including unauthenticated and authenticated flows.

The public filter UI showed global city/market values (for example London, Berlin, Paris, Munich and Zürich) as well as India/Remote. Make the geography model explicit: country eligibility, work location, remote eligibility, employer market and displayed location must not be conflated.

### 1.5 Current cohort/programme claims requiring one source of truth

Public pages currently describe several distinct programme offers. Preserve the distinction between a free application-based track, a paid training-plus-placement product, and a partner/company-specific hiring cohort.

| Programme surface | Public description observed | Required action |
|---|---|---|
| LMS homepage / Free Internship Track | 2 months, remote, minimum 10 hours/week; selected candidates pay a ₹499 refundable security deposit; displayed stipend range ₹5,000–₹18,000/month based on performance milestones | Clarify eligibility, refund deadline/conditions, and that stipend is conditional unless an individual offer says otherwise |
| LMS paid programme | ₹1,999 one-time, 2 months, non-refundable; training, production work, mentor sessions and internship placement after successful completion | State the exact employer, role, work period, assessment, deliverables, and meaning of “guaranteed placement” before payment |
| LMS Terms | Free track is not an employment offer, stipend promise or placement guarantee unless explicitly stated; paid programme placement is conditional; stipend listings are potential ranges and require paid-project allocation and completion of milestones | Terms must be consistent with each exact product and with offer letters |
| Aivara 2026 cohort page | 3-month cohort; 10–15 hours/week stated in one place and minimum 10 hours elsewhere; up to ₹22,000 performance-linked stipend; five engineering tracks | Treat as a distinct cohort contract and verify employer/legal counterparty, start/end dates, stipend formula and capacity |
| `dbert.in/learners` pathway | Launchpad, Accelerate and Fellowship prices/durations described separately | Ensure pricing and fellowship pages use the same programme registry |

Specific inconsistencies that must be resolved by a human product/legal owner:
- Main LMS: 2 months versus Aivara's 3 months.
- Main LMS: ₹499 refundable deposit versus a ₹1,999 non-refundable paid programme.
- Learner pathway: paid Launchpad/Accelerate/Fellowship products alongside an application-based internship track.
- LMS homepage says an offer letter is issued after enrolment, while Terms describe documents as conditional on satisfactory programme completion and use “where applicable” for offer letters.
- Stipend banners can look like guaranteed earnings, while Terms make stipend contingent on a revenue-generating project and required milestones.
- The credentials page says no application/registration/screening/interview fee; the LMS says a refundable post-selection deposit exists. Explain “no application fee” separately from any seat deposit, or remove the deposit if that is the intended policy.
- Main LMS homepage says “10K+ Students”; credential pages describe 1,500+ evaluated learners, 465+ certified fellows and 120+ venture fellows; the directory currently displays 468 records. These may be different populations, but each metric needs a clear definition, date and source.

**Do not let the coding agent decide fee policy, stipend guarantees, employment classification, IP assignment, refunds or legal meaning.** It must expose the conflict, propose copy/configuration, and wait for an authorised human decision before publishing changes.

### 1.6 Public people, mentor and candidate inventory

#### Staff / leadership

- `dbert.in/about/team` publicly names Abhinav Sharma as Founder, CTO and Principal AI Architect.
- The page describes domain practice leads for AI Systems / Agent Architecture & RAG, Full Stack / Modern Web & Distributed Systems, and Data & Quant / Data Pipelines & Conformal ML.
- The practice-lead functions are described, but the individual names, public technical profiles, availability, mentoring capacity and backup coverage are not adequately visible.
- `dbert.in/about/careers` advertises an Aivara Technologies 2026 hiring cohort and a general talent network for AI practitioners, researchers and technical mentors.

#### Mentors

The team page claims an active practitioner network, weekly live PR reviews, system-design mock sessions and latency audits. The public information is not enough to confirm the actual number of active mentors, their identities, current employment/contractor relationship, available hours, fellow-to-mentor ratio or recent review activity.

#### Pre-vetted engineers

The public hire page claims:
- “top 1% cohort fellows” in the headline, while the detailed criteria refer to a “top 3%” screen.
- Live PR, architecture, security, async collaboration and AI/LLM evaluations.
- Technologies including Next.js, FastAPI, PostgreSQL, LangChain, PyTorch and Docker.
- A 14-day risk-free trial.
- Candidate matching/onboarding in 48–72 hours, with candidate profiles promised within 24 hours in another section.

These are DBERT-authored claims. The page does not publicly expose a consented, availability-aware candidate roster with profile evidence, assessment date, role level, project contributions, verification status or current capacity. Do not treat the credential directory as the pre-vetted engineer roster.

#### Interns / fellows / alumni

- The public credential directory currently shows 468 records: 66 marked Verified and 402 marked Provisional.
- Directory entries expose names, credential IDs, programme/domain, tenure and evaluation grades. Individual credential pages may expose further information such as institution, academic score, a plagiarism index, permanent intern ID and signatory.
- A person can have multiple programme/credential entries; records must be linked carefully without assuming that repeated names are duplicates.
- The public directory is a credential registry, not a live “currently active interns” list. Past cohorts and completed tenures appear in it.
- An Alkame portfolio section titled “Interns Currently Working on Alkame” displayed “Loading contributors…” during the audit rather than a usable contributor list.

**Privacy warning:** Public search by candidate name and public display of academic/evaluation details is more disclosure than a simple credential verification task requires. Move to privacy-by-default and explicit opt-in before building richer public profiles. Do not scrape/export the full directory into a new page, public JSON endpoint, AI prompt, logs or repository fixtures.

#### Current advertised internship/cohort activity

- Aivara Technologies cohort page: remote, asynchronous, minimum 10 hours/week (10–15 hours/week also appears), performance-linked stipend advertised up to ₹22,000, and tracks across AI agents, full stack, Python automation, analytics and data engineering/ML.
- AI Agent listing page includes DBERT/Gayatri AI direct postings and third-party curated leads.
- General LMS board displays thousands of listings, but the number is not an active-student count.

The public site does not provide enough evidence to produce a reliable list of every currently active staff member, active mentor, active intern or available pre-vetted engineer. The agent may inspect authorised internal records locally if its environment is explicitly provisioned, but must return only aggregates or consented public profiles and must not expose private personal data.

---

## 2. Product strategy and target-state experience

### 2.1 The DBERT flywheel

1. Startups and internal product teams submit scoped engineering problems.
2. DBERT validates the problem, ownership, security classification, budget and delivery capacity.
3. A senior engineer breaks work into production-grade issues and acceptance criteria.
4. Vetted fellows are assigned based on skills, readiness, availability and mentor capacity.
5. Fellows work in protected branches and PRs; mentors review and approve.
6. Accepted changes are tested, released and attributed.
7. The platform records competencies and verified work evidence.
8. Graduates may opt into the hiring roster.
9. Employers inspect evidence, interview candidates and give outcome feedback.
10. Hiring outcomes, employer feedback and mentor assessments improve the next cohort.

### 2.2 Core user journeys

**Learner / intern**
- Discover a precise programme or actual vacancy.
- Understand whether it is training, a fellowship, an employment internship, or a sourced third-party lead.
- See fees, stipend formula, weekly hours, duration, legal employer and IP rules before applying.
- Apply with consent and minimum necessary personal information.
- Complete screening and receive a reasoned decision.
- Receive a named mentor, signed offer/engagement details, project and onboarding checklist.
- Work through issues and PRs with review feedback.
- Track hours, milestones, stipend approval/payment and progress.
- Receive an accurate certificate/LOR/experience letter with verified project attribution.
- Choose whether to publish a profile or join the hiring roster.

**Mentor / staff**
- See assigned fellows, project scope, workload and review queue.
- Assign tasks with acceptance criteria.
- Review PRs using a calibrated rubric.
- Record feedback and competency evidence.
- Escalate blockers, workload risks, misconduct, security issues and stipend disputes.
- See workload/capacity without accessing unrelated personal/payment data.

**Startup / employer**
- Verify company and authorised hiring contact.
- Publish a direct role or scoped engineering project.
- Set skills, eligibility, work mode, hours, stipend, duration, mentor, deliverables and application method.
- Review candidate profiles only after permission/consent.
- See evidence relevant to the role, not private academic/payment data.
- Run interview or trial under written conditions.
- Record hire, rejection, trial and retention outcomes.

**Public visitor**
- Understand DBERT's actual legal identity and business model.
- Inspect projects, code, named mentors, transparent programme terms and anonymised cohort outcomes.
- Verify a credential by exact ID without browsing unrelated candidates' personal records.

---

## 3. Phased implementation plan

The phases are intentionally ordered so that trust, data quality and safety are fixed before the platform is marketed more aggressively. A phase is complete only when its acceptance criteria pass in staging and the regression suite is green.

## Phase 0 — Repository discovery, safety baseline and change control

**Priority:** P0 / mandatory before any code changes  
**Risk:** Very high if skipped  
**Mode:** Read-only audit first

### Tasks

1. Inspect repository root, git remotes, current branch, tags, package files, framework/runtime versions, build scripts, test scripts, CI workflows, infrastructure files and deployment configuration.
2. Run `git status --short --branch`. If there are uncommitted changes, do not stash, reset, checkout over them or overwrite them. Record the state and stop for human direction if ownership is unclear.
3. Map all apps/packages and domains. Identify which code serves `dbert.in`, `lms.dbert.in`, APIs, webhooks, payment callbacks, certificate verification and scheduled jobs.
4. Map routes, dynamic routes, redirects, canonical URLs, auth boundaries, public/private pages and any middleware.
5. Map database schema, migrations, ORM, seeds, indexes, triggers, background jobs and data ownership. Do not run destructive scripts.
6. Identify integrations: GitHub, email, UPI/payment verification, analytics, notifications, certificate hashing/verification, AI model APIs, cloud storage and external job sources.
7. Identify actual role/status values in code for candidates, fellows, mentors, employees, employers, jobs, cohorts, credentials and payments. Do not assume names or values from this document match the code.
8. Run existing lint, typecheck, build, unit, integration and E2E tests. Save exact commands and baseline failures. Do not “fix” unrelated failures in this phase.
9. Create a read-only audit report and route/data diagrams. Capture baseline screenshots for core user flows if browser tooling exists.
10. Find secrets and sensitive-data handling only by checking secret references/configuration names. Never print secret values into the report or AI context.

### Deliverables

- `docs/dbert-roadmap/audit/repository-map.md`
- `docs/dbert-roadmap/audit/route-inventory.csv`
- `docs/dbert-roadmap/audit/data-model-map.md`
- `docs/dbert-roadmap/audit/integration-map.md`
- `docs/dbert-roadmap/audit/test-baseline.md`
- `docs/dbert-roadmap/audit/current-public-claims.md`
- `docs/dbert-roadmap/audit/risks-and-unknowns.md`

### Acceptance criteria

- The agent can explain which code and data store serve each public domain.
- Every critical route and integration has an owner/dependency entry.
- Baseline build/test status is known.
- No source files, database records, production settings or deployment configuration have been modified.
- Existing uncommitted human changes are preserved.

### Stop condition

Do not move to implementation if the app architecture, production data ownership, payment flow, authentication boundary or migration process is not understood.

---

## Phase 1 — Programme truth, brand consistency and domain contracts

**Priority:** P0  
**Goal:** Make every price, duration, stipend, certificate and placement claim consistent across the public site and LMS.

### 1.1 Create one programme source of truth

Inspect the existing schema first. Reuse or extend current entities if possible. Do not create a duplicate programme catalogue if one already exists.

A programme configuration should represent at least:

- Stable programme ID and version.
- Public name and track.
- Programme type: `course`, `training`, `free_internship`, `paid_fellowship`, `company_internship`, `job_listing`.
- Legal contracting entity and actual host/employer.
- Duration and exact start/end date rules.
- Hours/week and synchronous/asynchronous expectations.
- Location/work mode and eligibility.
- Fee, taxes, deposit, refund amount, refund deadline and conditions.
- Stipend base, variable component, eligibility formula, cap, payment dates and payer.
- Deliverables, minimum completion criteria and assessment rubric.
- Mentor assignment and review cadence.
- Certificate, LOR, offer/experience letter issuance conditions.
- Placement promise scope and exclusions.
- IP, confidentiality, data and repo access terms.
- Status, cohort version, effective date and archived date.

All public pages and enrolment forms must render from the same approved version. Historical cohorts must retain their original terms; do not silently rewrite a contract that a participant accepted.

### 1.2 Separate the programme types

Make a clear public comparison between:

- Free application-based internship (if retained).
- Paid learning/training programme.
- Paid fellowship/work engagement (if this is a distinct product).
- Direct DBERT internship.
- Incubated venture/company internship.
- Third-party employer internship.

A paid course must not be presented as an employer-paid internship. A sourced vacancy must not be presented as a DBERT internship. A completion certificate must not be described as a degree or UGC/AICTE accreditation.

### 1.3 Required policy decisions (human approval)

The agent must prepare decision documents and wait for an authorised owner to choose:

1. Keep or remove the ₹499 post-selection refundable deposit.
2. Keep or redesign the ₹1,999 paid programme.
3. Decide whether any fellowship is paid work, a training programme, an internship, or a combination with separately documented phases.
4. Decide the exact stipend model and whether a base stipend is guaranteed for each accepted fellow.
5. Decide the exact duration and commitment for each cohort (2 months vs 3 months; 10 vs 10–15 hours/week).
6. Define precisely what “guaranteed internship placement” means and what is not guaranteed.
7. Define when an offer letter, completion certificate, LOR and experience letter are issued.
8. Confirm legal employer/counterparty for DBERT, Aivara, Gayatri AI, Alkame and each partner role.

### 1.4 Website copy consistency

- Replace hard-coded programme facts with source-of-truth data.
- Put a “Last updated” and effective-cohort label on programme terms.
- Put stipend conditions next to every stipend figure, not only in legal terms.
- Show the legal employer and who pays the stipend.
- Show refund conditions before the payment action.
- Add a printable/downloadable programme agreement summary.
- Clarify that MSME registration is not UGC/AICTE academic accreditation.
- Define the difference between evaluated learners, course learners, credential holders, venture fellows, active interns and pre-vetted engineers.
- Use one verified contact email/domain policy. Ensure old `@dbert.info` references, if any remain, are either intentionally supported or updated after email-domain ownership and delivery are tested.

### Acceptance criteria

- Every displayed programme fact matches the approved programme configuration.
- No contradiction exists between homepage, course page, application form, payment screen, offer template and terms for the same cohort.
- Existing enrolled users see the terms version they accepted.
- Historical certificates and verification URLs still work.
- No payment or refund code changes without sandbox and owner approval.

---

## Phase 2 — Internship/job taxonomy, authenticity and listing quality

**Priority:** P0/P1  
**Goal:** Make the marketplace useful and credible rather than large but noisy.

### 2.1 Canonical taxonomy

Implement the taxonomy in §1.3 as a normalised mapping layer. Reuse existing IDs where possible and map legacy labels to canonical categories. Do not delete old categories or alter URLs until redirects and data migrations are tested.

Every listing should support:
- One primary domain.
- Zero or more secondary domains/skills.
- Job function (engineering, design, business, research, operations, etc.).
- Seniority/experience level.
- Required skills versus preferred skills.
- Country eligibility, location and work mode as separate fields.

Add a validation rule: a role whose main duties are marketing, HR, content, campus ambassador, sales or programme management cannot be shown as an AI engineering vacancy merely because the source used a broad AI category. It may have AI tools as a secondary skill, but the primary function must remain truthful.

### 2.2 Posting-source taxonomy

Use explicit source labels and public explanations:

- `DBERT_DIRECT`: DBERT is the employer/contracting entity.
- `VENTURE_DIRECT`: a named DBERT-incubated venture is the employer/contracting entity, confirmed by that venture.
- `PARTNER_DIRECT`: an external employer has authorised the role and DBERT is an approved channel.
- `CURATED_LINK`: DBERT found a public role; application occurs with the original employer.
- `SOURCED_LEAD`: a role lead that has not yet been fully employer-confirmed.
- `CLOSED_ARCHIVE`: no longer accepting applications.

Do not use the word “verified” as a blanket badge for all scraped, curated or sourced listings.

### 2.3 Employer and listing verification

Employer profile fields:
- Legal entity name, public website, official domain and authorised contact.
- Registration data where appropriate and lawfully collected.
- Verification method and reviewer.
- Employer/partner status and agreement expiry.
- Last confirmation date.
- Whether the role is direct, partner or only a public link.

Listing fields:
- Original source URL and capture timestamp.
- Date created, last employer confirmation and expiry date.
- Role title, responsibilities, skills, domain, location, work mode, eligibility, duration and weekly hours.
- Stipend as fixed / range / performance-based / unpaid / not disclosed.
- Payer and payment frequency when known.
- Application method and official contact.
- Number of actual applicants (not page views or impressions).
- Status: draft, awaiting employer verification, verified open, paused, filled, expired, rejected.

### 2.4 Freshness and deduplication

- Detect exact duplicates and near-duplicates using employer, title, location, source URL and content fingerprints.
- Do not merge separate vacancies without review.
- Expire listings automatically after a configurable freshness window unless reconfirmed. Start with a conservative default (e.g. 30 days) and allow owner overrides for long-running official postings.
- Recheck direct/partner postings on a shorter cadence (for example every 7–14 days).
- Show “last confirmed” and “applications close” dates.
- Keep expired records for analytics, but remove them from active search.
- Avoid fake or inflated counts. Derive counts from the exact query/filter currently shown.

### 2.5 Search and filter correctness

- Ensure category totals, location totals, pagination totals and result rows come from the same query snapshot.
- Separate India-only, global, remote-global and remote-India eligibility.
- Do not interpret “Remote” as “eligible from India” without employer confirmation.
- Make filters keyboard-accessible, bookmarkable and stable across pagination.
- Preserve old query parameters and URLs through adapters/redirects.
- Provide a “report inaccurate listing” action.
- Add moderation queue for questionable listings and user reports.

### 2.6 Listing quality score (internal; do not hide weak data behind a score)

Score completeness, freshness, employer verification, role clarity, stipend transparency and source quality. The score should be explainable and should never transform an unverified role into a verified one. Publicly show the verification state and missing facts.

### Acceptance criteria

- All listings have an explicit source class.
- The AI engineering domain has no obvious non-technical-primary-role leakage in the regression sample.
- Counts match visible result sets.
- Expired and duplicate roles do not appear as active.
- A user can identify employer, location/work mode, compensation status, role duties and application path before applying.
- Existing saved applications and listing IDs remain valid.

---

## Phase 3 — Staff, mentors, interns, alumni and pre-vetted talent registry

**Priority:** P1  
**Goal:** Turn vague claims about people into a governed, consent-based and operationally useful talent system.

### 3.1 Model people as separate roles, not one generic “user” label

Inspect existing user schema and roles first. The system may need distinct role memberships for one person, but do not assume a person can only have one role.

Conceptual roles:
- `STAFF`: DBERT employee or authorised internal operator.
- `CONTRACTOR`: external contributor under a written engagement.
- `FOUNDER`: studio/company founder.
- `MENTOR`: assigned technical or career mentor.
- `ADVISOR`: occasional subject-matter, legal or institutional advisor.
- `APPLICANT`: candidate who has applied.
- `FELLOW`: selected into a structured fellowship.
- `INTERN`: currently engaged in a specific internship role/cohort.
- `ALUMNUS`: completed a cohort or engagement.
- `VETTED_ENGINEER`: passed a defined role-specific technical evaluation and consented to hiring consideration.
- `EMPLOYER`: verified company/contact that posts or hires.

A credential holder is not automatically a vetted engineer. A person who completed a training module is not automatically an intern. A provisional credential is not a verified employment record.

### 3.2 Staff and mentor public profiles

Create a public profile only where the person has approved publication. Each profile may show:
- Name and professional title.
- Staff/mentor/advisor relationship, described accurately.
- Technical specialisations and level of responsibility.
- Public LinkedIn/GitHub/portfolio links.
- Relevant work samples/publications.
- Years/period of relevant experience only when substantiated.
- Current mentoring availability and the cohort(s) served.
- Languages/time zone if useful and voluntarily disclosed.

Do not expose personal phone numbers, private email, home address, government IDs, personal account IDs or private employment documents.

Create named public profiles for the AI Systems, Full Stack and Data/Quant leads only after verifying their identities, engagement status, experience and permission. If a lead is confidential or does not wish to be public, show a role-level team description without implying a named employee exists.

### 3.3 Mentor operations and capacity

Each active mentor record should have:
- Verified professional identity and internal approval.
- Domain/skill coverage and level.
- Availability hours per week.
- Active fellow count and capacity ceiling.
- Expected PR review time.
- Session cadence.
- Backup/cover mentor.
- Conflict-of-interest declaration where relevant.
- Recent review evidence and learner feedback.

Recommended pilot service standards (adjust after capacity measurement):
- One scheduled technical check-in per active fellow per week or a clearly stated alternative.
- Initial response to a blocked fellow within two working days.
- PR review within two working days for normal-sized PRs, with an explicit queue/exception when workload is high.
- No mentor should be assigned more active fellows than they can review properly. Begin with a small capacity (for example 4–6 active fellows per mentor for high-touch engineering work) and revise using actual data.
- Escalation path for missed reviews, absence, conflict or poor supervision.

Do not promise weekly 1:1 sessions or code reviews on marketing pages until scheduling, staffing and completion telemetry prove the service can be delivered.

### 3.4 Intern/fellow lifecycle

Use explicit states with audited transitions, adapting existing states where possible:

`draft → applied → screening → interview/challenge → selected → offer_sent → offer_accepted → onboarding → active → paused/at_risk → completed → credential_issued → alumni`

Additional terminal states: `rejected`, `withdrawn`, `terminated`, `declined_offer`.

Every transition should store who changed it, when, reason/category, and relevant policy/offer version. Keep internal notes separate from candidate-visible messages.

### 3.5 Pre-vetted engineer standard

Replace marketing-only “top 1%/top 3%” wording with a published, repeatable rubric. A suggested 100-point rubric is below; calibrate by track and run a pilot before setting cutoffs.

| Dimension | Suggested weight |
|---|---:|
| Role-specific implementation and technical correctness | 25 |
| Code quality, tests, security and maintainability | 20 |
| Architecture and trade-off reasoning | 15 |
| Debugging and problem decomposition | 10 |
| Async communication and documentation | 10 |
| Collaboration, Git discipline and review response | 10 |
| Ownership, reliability and delivery | 10 |
| **Total** | **100** |

Suggested qualification gate:
- Minimum overall score (propose 80/100 for pilot, then calibrate using real hiring outcomes).
- No critical security, integrity or authorship failure.
- At least one reviewed project contribution relevant to the candidate's target role.
- Two reviewers for higher-risk/lead-level classifications.
- A defined re-assessment date (for example 6 months) and expiry if availability/skills are stale.
- A written explanation of what “vetted” means; do not infer guaranteed job performance.

Assessment must be fair and accessible. Provide accommodations where appropriate. Use take-home tasks that are not disguised unpaid production work. If a candidate contributes to a real client deliverable, use a properly documented and compensated arrangement.

### 3.6 Private candidate roster and public talent pages

**Private hiring roster (permissioned):**
- Candidate opts into being discoverable.
- Skills, target roles and proficiency evidence.
- GitHub/PR/project evidence, reviewed and attributable.
- Mentor assessment summary with date and rubric version.
- Availability, preferred engagement and notice period.
- Remote/relocation preference at coarse geographic level.
- Interview status, offer status and consented outcomes.

**Public directory:**
- Default private.
- Candidate explicitly opts in to each public field.
- Exact credential ID verification remains available.
- Do not publish academic scores, plagiarism reports, institution details, internal evaluation notes, permanent internal IDs or private contact data by default.
- Provide profile visibility controls, correction, revocation and takedown workflows.
- Avoid public bulk search of personal profiles unless there is a documented consent and business need.

### 3.7 Candidate record reconciliation

- Reconcile the 468-record directory and any underlying CRM/LMS records using stable internal IDs, not names alone.
- Distinguish provisional, verified, revoked, expired, corrected and duplicate-linked credentials.
- Link multiple credentials to one person only after an authorised identity reconciliation process.
- Never overwrite historical assessment results; add corrected/updated versions with an audit trail.
- Provide a privacy-safe public aggregate dashboard: applications, completions, verified credentials, active fellows and vetted talent are separate numbers.

### Acceptance criteria

- Public team page reflects only people who have approved publication.
- Every active mentor has a defined capacity and an internal assignment record.
- “Pre-vetted” requires a versioned rubric and completed review evidence.
- Public credential verification works by exact ID without unnecessary disclosure of other candidate information.
- No provisional record appears as a verified engineer.
- Current active fellows can be counted internally without exposing their personal data publicly.

---

## Phase 4 — Fellowship design, curriculum and real engineering delivery

**Priority:** P1  
**Goal:** Make the fellowship a high-quality engineering apprenticeship, not a certificate product.

### 4.1 Distinguish teaching, practice and production work

Each cohort should define separate phases:
1. **Foundation:** onboarding, tooling, secure development, domain concepts.
2. **Practice:** sandbox tasks and supervised exercises.
3. **Project delivery:** scoped project tasks on an approved repository.
4. **Release and reflection:** tests, release notes, demo, technical write-up and review.

Do not label a learning-only course as production employment. Do not claim production experience if a fellow only used a tutorial repository.

### 4.2 Track-specific competency maps

**Generative AI / LLM engineering**
- Python engineering, typing, packaging, async APIs.
- LLM APIs and local inference, provider abstraction and cost controls.
- Embeddings, chunking, hybrid retrieval, reranking and citations.
- RAG evaluation, golden datasets, retrieval precision/recall and hallucination tests.
- Agent tool schemas, permissions, state, retries, timeouts and human approvals.
- FastAPI, PostgreSQL/vector storage, caching and background jobs.
- Prompt injection, data exfiltration, secrets handling and guardrails.
- Observability, latency, token cost, tracing and production deployment.

**Applied ML / model engineering**
- Statistics, data leakage prevention and correct train/validation/test splits.
- Baselines, feature engineering, model selection and calibration.
- Reproducible experiments, versioned data/model artifacts.
- Offline/online evaluation, drift detection and monitoring.
- Model serving, APIs, resource constraints and deployment.

**Data engineering / analytics**
- SQL, data modelling, ETL/ELT, validation and lineage.
- Orchestration, retries, observability and data quality.
- Analytics requirements, dashboard design and reproducibility.

**Full stack / backend**
- API contracts, schema migrations, auth/RBAC, test strategy.
- Frontend accessibility, state management and error handling.
- Database design, performance, security and deployment.

**DevOps / security**
- CI/CD, containers, infrastructure as code, logging/metrics.
- Threat modelling, least privilege, dependency scanning and incident response.

### 4.3 Standard project brief

Every project assigned to fellows must have:
- Problem statement and user/customer.
- Internal project owner and mentor.
- Scope, out-of-scope list and success metrics.
- Repo, issue board and environment access.
- Data classification and access restrictions.
- Architecture/context documentation.
- Acceptance criteria and test expectations.
- Timeline, hours/week and stipend/compensation terms.
- IP, confidentiality and attribution terms.
- Definition of Done and release approver.

### 4.4 Sprint workflow

1. Mentor creates or approves a well-scoped issue.
2. Fellow acknowledges acceptance criteria and estimate.
3. Work occurs in a feature branch; no direct main-branch commits.
4. PR template requires problem, solution, tests, screenshots/logs where applicable, risks and rollback.
5. CI runs tests, lint, type checks, security scans and required quality checks.
6. Reviewer leaves line-level feedback.
7. Author addresses feedback; second review for sensitive or high-impact code.
8. Release is approved by project owner, not by the intern alone.
9. Platform records merged PR, release/commit attribution and mentor review.
10. Fellow receives competency feedback tied to evidence.

### 4.5 Fair stipends and payments

Create or adapt a stipend ledger with separate states:
`not_eligible → eligible → milestone_submitted → mentor_approved → finance_approved → payable → paid`

Also support `rejected`, `disputed`, `on_hold` with reasons and audit trail.

- Define base stipend, milestone bonus and maximum separately.
- Give each candidate an individual written stipend schedule.
- Show payment due date and payment status in the learner portal.
- Notify the candidate of rejection/hold reasons and dispute route.
- Never count a conditional maximum as a guaranteed stipend in public totals.
- Keep payment proof and bank/UPI data private and access-controlled.

### 4.6 Fellow protection and IP

Have qualified counsel review employment/contract status, IP ownership, confidentiality, work hours, stipend treatment, safety, grievance and termination terms. The agent may implement approved workflows and document templates but must not invent legal language or assume every fellow can be treated as a volunteer/contractor.

### Acceptance criteria

- Each active fellow is attached to a versioned project brief, named mentor, approved role/contract and measurable deliverables.
- No production task exists without ownership, acceptance criteria and access controls.
- PR and mentor review evidence is captured.
- Stipend eligibility and payments are auditable.
- Certificates and letters are generated only from approved completion records.

---

## Phase 5 — Proof-of-Work Graph and credential verification

**Priority:** P1  
**Goal:** Make DBERT's strongest claims independently inspectable.

### 5.1 Evidence graph

Connect, using stable IDs and explicit permissions:
- Person and consent record.
- Cohort/programme version.
- Role/offer version.
- Project and repository.
- Issue/task.
- Branch/commit/PR.
- Review event and reviewer.
- CI/test result and security scan result.
- Release/version.
- Competency rubric and score/evidence.
- Credential issued/revoked/corrected.
- Placement/interview result, only with appropriate consent.

A GitHub commit alone is not proof of quality. Evidence should include review, tests, acceptance and project context.

### 5.2 GitHub integration

- Use least-privilege GitHub App or OAuth scopes; do not request broad personal token access unless unavoidable.
- Store repository/installation mapping, not secrets in the database.
- Verify webhook signatures and make handlers idempotent.
- Support private repositories without exposing code to public pages.
- Respect client IP, repo visibility and NDA restrictions.
- Attribute only verified contributions; handle squash merges, co-authorship, rebases and bot commits carefully.
- Provide manual evidence import when GitHub integration is unavailable, with reviewer verification.

### 5.3 Credential verification

- Keep stable credential IDs and historic verification URLs.
- Use signed payloads or a well-documented cryptographic verification design; do not claim blockchain/on-chain or tamper-proof guarantees unless the implementation proves them.
- Expose only: credential ID, issuer, credential type, issue date, current status and consented public attributes.
- Provide revocation/correction status and reason category without disclosing private details.
- Explain that verification proves issuance/authenticity, not academic accreditation or guaranteed job competence.
- Make QR codes resolve to canonical HTTPS verification pages.

### 5.4 Outcomes dashboard

Display well-defined, cohort-specific, dated metrics:
- Applicants.
- Eligible applicants.
- Selected fellows.
- Started fellows.
- Completed fellows.
- Verified credentials issued.
- Accepted/merged PRs (with definition).
- Releases/features shipped.
- Fellows eligible for stipend.
- Fellows paid and median actual paid amount.
- Interview referrals, offers and hires, with attribution window and consent.
- Withdrawals and drop-offs.

Show denominators. For example, “8 offers among 24 fellows whose six-month outcome was known” is more honest than “33% placement” without explaining the denominator.

### Acceptance criteria

- An employer can inspect a consented candidate's evidence without gaining access to private repo/code or internal mentor notes.
- A credential can be verified by exact ID and revoked/corrected safely.
- Metrics can be regenerated from underlying records and have a cohort/time definition.
- Public pages do not overclaim “audited”, “on-chain”, “peer-reviewed”, “accredited” or “verified” beyond what the implementation supports.

---

## Phase 6 — Employer portal and high-quality talent marketplace

**Priority:** P2  
**Goal:** Turn the pre-vetted-engineer page from a promise into a usable, ethical hiring product.

### 6.1 Employer onboarding

- Verify company and authorised requester.
- Capture legal entity and official domain.
- Define whether the employer is client, incubated venture, partner or sourced public employer.
- Record agreement, role owner, hiring budget, location eligibility and feedback contact.
- Add anti-scam checks and a complaint route.

### 6.2 Candidate matching

- Match only candidates who opted into discovery.
- Filter by verified skills, project evidence, availability, location/work eligibility and engagement type.
- Present evidence and rubric version, not a mysterious AI score.
- Never use protected/sensitive traits or proxies to rank candidates.
- Do not auto-reject a candidate solely based on model output.
- Require human review and log reasons for shortlist decisions.

### 6.3 Employer-facing candidate profile

Show only consented, relevant information:
- Name or approved display name.
- Role level and primary skills.
- Two or three relevant project examples.
- Reviewed PRs/releases and competency evidence.
- Mentor reference availability.
- Availability and preferred work mode.
- Candidate-approved CV/portfolio links.

Do not show academic score, private notes, payment history, phone/email or raw assessment submissions by default.

### 6.4 Hiring claims and SLAs

The pre-vetted page should not assert “top 1%” or “top 3%”, “48 hours”, “24 hours”, 14-day trial or zero fee unless DBERT has an operational definition and enough historical records to support each claim.

Define and track:
- Time from approved requisition to first qualified shortlist.
- Time to first interview.
- Interview-to-offer rate.
- Offer acceptance rate.
- Trial completion / conversion rate.
- 30/90-day retention where lawful and consented.
- Employer satisfaction and repeat-hire rate.
- Candidate satisfaction and grievance rate.

Publish median and sample size, not only best-case turnaround.

### Acceptance criteria

- Employers cannot see candidate profiles before verification and permission.
- Each “pre-vetted” profile has dated evidence and an explicit skill rubric.
- Availability is current and candidates can pause discovery.
- Employer and candidate outcomes can be audited.

---

## Phase 7 — Research, product and venture portfolio credibility

**Priority:** P2  
**Goal:** Make DBERT Labs and the venture studio visibly real through reproducible artifacts.

### 7.1 Project portfolio template

Every public project page should include:
- Project owner, sponsoring venture and status.
- Problem, intended users and use case.
- Architecture diagram and current stack.
- Live demo or screenshots where safe.
- Public repo or redacted sample where allowed.
- Test/build/release status.
- Operational metrics and measurement method.
- Known limitations and what is not yet built.
- Team/mentor/fellow contribution attribution, with consent.
- Security/privacy note and data source.
- Last updated date.

### 7.2 Research publishing standard

For each report/model:
- Named authors and affiliations with consent.
- Version and date.
- Correct identifier/DOI and a link that resolves.
- Research question and pre-registration when claimed.
- Dataset provenance, license and data access constraints.
- Model/base weights, architecture, hyperparameters and compute environment.
- Baselines and metrics with uncertainty/error bars where relevant.
- Reproduction instructions and code version.
- Limitations, negative results and conflicts of interest.
- License and model-card details.

Use “preprint”, “technical report”, “peer reviewed” and “peer audited” precisely. Do not call a report peer-reviewed unless an external peer-review process occurred and can be described. Verify each DOI/Zenodo/arXiv/GitHub/Ollama link before publishing.

### 7.3 Metric and telemetry authenticity

The public site uses live-console/telemetry-style statements and metrics. Each metric must be one of:
- Live metric from a production system, with a defined source and last-updated time.
- Historical audited metric, with cohort/time period and methodology.
- Illustrative demo data, visibly labelled as demo/simulated.

Never present hard-coded sample telemetry as real-time production activity. Do not invent uptime, deployment, customer counts, school counts, test coverage, team size or revenue metrics.

### Acceptance criteria

- Public case studies are supported by live repos/demos or a clear explanation of confidentiality limits.
- All benchmark and performance claims can be reproduced or have a clearly stated measurement method.
- Demo telemetry is labelled.
- Research links/identifiers resolve and authorship/peer-review language is accurate.

---

## Phase 8 — UX, accessibility, performance, security and operational maturity

**Priority:** P1/P2  
**Goal:** Improve the experience and resilience without replacing the existing stack.

### 8.1 UX and navigation

- Clear paths for Startups, Learners, Employers, Mentors and Research.
- On learner pages, show “Course”, “Internship”, “Fellowship” and “Job” as distinct product labels.
- Make the programme comparison, current cohort status and exact terms easy to find.
- Provide a working mentor/contact path.
- Fix or clarify routes that redirect to the LMS homepage when opened without authentication; if intentionally private, show an explicit sign-in/permission state rather than a confusing silent redirect.
- Make job details usable and test every “View & apply” link.
- Keep navigation labels consistent between `dbert.in` and `lms.dbert.in`.

### 8.2 Accessibility and performance

- Target WCAG 2.2 AA where practical.
- Semantic headings and landmarks, keyboard support, visible focus, labelled inputs, screen-reader status messages and sufficient contrast.
- Responsive layouts and no horizontal overflow on common mobile widths.
- Optimised images, font loading, caching and route-level code splitting according to the existing framework.
- Avoid shipping large chart/animation code to application-critical pages unnecessarily.
- Measure Core Web Vitals and server response timings before/after changes.

### 8.3 Security and privacy

Audit and strengthen:
- RBAC and object-level authorization for every candidate, mentor, employer, payment, project and credential resource.
- IDOR protection: changing an ID in a URL must not expose another person's record.
- Session, CSRF, CORS, CSP, secure cookie and rate-limit settings.
- Password hashing and account recovery.
- File uploads (MIME/type/size validation, malware scanning, private storage, signed downloads, retention).
- Webhook signature verification and idempotency.
- Encryption in transit and at rest for sensitive fields and files.
- Secrets management and rotation.
- Audit logs for sensitive views, profile exports, credential changes, role changes and payment operations.
- Backups, restore tests and incident response.
- Consent, access, correction, erasure, retention and grievance flows consistent with approved policy and applicable law.

Do not send full student databases, resumes, phone numbers, payment proofs, internal review notes or private code to a hosted AI API unless the data flow has been approved, documented and minimised.

### 8.4 Observability

- Structured logs with request IDs; redact PII, tokens, payment data and secrets.
- Error monitoring for front-end and back-end.
- Metrics for application latency, job-search latency, failed role detail loads, webhook failures, email delivery, mentor task queues and credential verification.
- Alerts for rising 5xx, failed payments, missed stipend payouts, queue backlog and certificate failure.
- Status page or incident notice for learner-facing outages.

### Acceptance criteria

- Critical user journeys work on mobile and desktop with keyboard navigation.
- No cross-user data access in authorization tests.
- No secrets or sensitive personal data appear in logs.
- Backups restore successfully in a non-production environment.
- Performance and error budgets are defined from a measured baseline.

---

## Phase 9 — Controlled rollout and continuous improvement

**Priority:** P1  
**Goal:** Release safely and measure real improvement.

### Rollout sequence

1. Local development with anonymised/test data.
2. Unit/integration tests and static checks.
3. Staging deployment with production-like configuration and no real payment movement.
4. Data migration dry run on a snapshot; verify row counts and referential integrity.
5. Internal staff/mentor pilot.
6. Small cohort pilot behind feature flags.
7. Monitor errors, task queues, user feedback and business KPIs.
8. Expand gradually.
9. Keep rollback available until the change is stable.

### Feature flags

Use the project's existing feature-flag mechanism if present. Otherwise add the smallest compatible mechanism. Suggested flags:
- `program_truth_v2`
- `listing_taxonomy_v2`
- `employer_verification_v2`
- `mentor_profiles_v2`
- `candidate_privacy_v2`
- `talent_roster_v2`
- `proof_of_work_v1`
- `stipend_ledger_v1`

Flags must default to the safe/current behaviour until their migration and tests are complete. Do not create a flag that bypasses auth or privacy.

### Rollback

For every phase, document:
- How to disable the feature.
- How to revert application code.
- Whether a database migration is reversible.
- How to restore/repair data.
- How to preserve user submissions made during the pilot.
- Who approves rollback.

Never delete or rewrite historical user, payment, application, assessment or credential records to make a dashboard look clean.

---

## 4. Cross-cutting “do not break existing code” rules

These rules are mandatory for every phase.

### 4.1 Git and change isolation

- Never work directly on the production branch.
- Create a descriptive feature branch only after checking the working tree.
- Never run `git reset --hard`, `git clean -fd`, forced checkout, rebase or history rewrite on a user-owned working tree.
- Do not overwrite, reformat or remove files unrelated to the current task.
- Keep commits small and explain each one.

### 4.2 No blind rewrites

- Do not change framework, router, ORM, CSS system, auth provider, hosting provider, database, payment provider or domain architecture as part of a feature phase unless separately approved.
- Do not replace working components just because another library is fashionable.
- Reuse existing design system, form validation, API client, auth and error handling.
- Preserve all existing route paths and query parameters; use redirects/adapters for new canonical routes.

### 4.3 Database safety

- Inspect actual schema before designing migrations.
- Prefer additive nullable fields, new tables and compatibility views.
- Do not drop/rename columns, rewrite primary keys, change enums destructively or bulk-delete rows in early phases.
- Use expand → backfill → dual-read/write if needed → verify → contract only after a separate approval and rollback plan.
- Back up before migration and prove restoration in staging.
- Use migrations that are idempotent where possible.
- Do not run migrations or seed commands against production from the local agent.

### 4.4 API and integration compatibility

- Keep old response fields while adding new optional fields.
- Version public API changes where existing clients may depend on a schema.
- Do not change GitHub webhook, UPI/payment reconciliation, email templates, credential hashes or certificate IDs without regression tests.
- Make webhook handlers idempotent.
- Keep old certificate verification URLs operational.
- Do not change mail sender domains before SPF/DKIM/DMARC and inbox delivery have been tested.

### 4.5 Security and privacy

- Enforce server-side authorization; front-end hiding is not security.
- Minimise access to student/staff data.
- Use anonymised fixtures in tests.
- Do not put real resumes, phones, emails, payment screenshots, passwords, credentials or private keys in commits, logs, prompts or public test data.
- Use explicit consent for public profiles and third-party sharing.
- Never auto-publish candidate or mentor profiles.

### 4.6 AI agent boundaries

The local agent may inspect the code and authorised local test data. It must not:
- Invent staff, mentor, employer or alumni identities.
- Infer “active” status from a historic credential.
- Infer a pre-vetted status from course completion or a certificate.
- Send candidate PII to external model APIs without approved safeguards.
- Publish a claim, price, contract, stipend promise or legal policy without a human-approved source.
- Run destructive DB commands, production deployments or real UPI/payment transactions.
- Make a candidate selection/rejection purely through an opaque model score.

---

## 5. Required testing matrix

The agent must adapt this matrix to the real framework and add tests alongside every changed feature.

| Area | Minimum tests |
|---|---|
| Public routing | `dbert.in` pages, LMS routes, canonical redirects, legacy redirects, query parameters |
| Authentication | Sign-up, sign-in, sign-out, password reset, session expiry, role changes |
| Authorization | Candidate A cannot view/edit candidate B; mentor only sees assigned fellows; employer only sees consented candidates; staff permissions are least-privilege |
| Applications | Submit, edit where allowed, screening, status updates, notifications, duplicate prevention |
| Programme terms | Exact fee/duration/stipend version shown at application, offer, checkout and terms acknowledgement |
| Payments | Sandbox-only payment and reconciliation; refundable deposit lifecycle; no real money in test |
| Marketplace | Source badge, taxonomy, filters, pagination, deduplication, expiry, report listing, employer verification |
| Job detail | Every visible “View & apply” link loads; 404/500 monitoring; logged-in/out states |
| Mentorship | Mentor assignment, capacity, calendar/session link, review queue, escalation |
| Sprint workflow | Task assignment, branch/PR link, review, rework, merge, release, attribution |
| Stipend | Eligibility, milestone calculation, approvals, paid state, disputes, audit log |
| Credentials | Issue, verify, revoke, correct, historical URL, QR, privacy-safe output |
| Talent roster | Candidate opt-in/out, role filters, freshness, employer permissions, no private fields in public API |
| Privacy | Exact-ID verification only, public-directory opt-in, access/erasure workflow, log redaction |
| Security | IDOR, CSRF, XSS, SQL injection, rate limit, upload validation, secret scanning, dependency audit |
| Accessibility | Keyboard, focus, labels, semantic structure, contrast, mobile screen-reader basics |
| Reliability | Build, lint, typecheck, unit, integration, E2E, migration dry-run, backup restore, rollback drill |

### Critical regression user journeys

1. New learner registers and verifies email (if configured).
2. Learner completes application and sees the exact selected programme and terms.
3. Staff reviews application and records a decision.
4. Selected candidate receives an offer with legal entity, dates, hours, stipend and IP terms.
5. Candidate joins cohort and receives mentor/project assignment.
6. Fellow completes task, opens PR and receives mentor review.
7. Approved milestone updates stipend ledger.
8. Completion triggers certificate/LOR only when eligible.
9. Employer verifies an exact credential ID.
10. Candidate separately opts into the talent roster and an employer accesses only permitted fields.
11. Existing user can still sign in and access historical application/certificate pages.
12. Existing job board URLs and saved links still resolve.

---

## 6. KPIs and operating dashboard

Start by measuring a 30-day baseline. Do not set aggressive goals from vanity numbers. Proposed targets below are operational aspirations and must be validated with real capacity.

### Trust and transparency
- 100% of active programme pages render from approved programme configuration.
- 100% of accepted fellows receive written terms before starting.
- 100% of stipend-bearing engagements have an individual stipend schedule.
- 0 public claims that contradict the signed cohort terms.
- Every public outcome metric has a definition, denominator, cohort and as-of date.

### Marketplace quality
- 100% of active listings have a source class.
- 100% of direct/partner badges have a verification record.
- At least 95% of active partner roles reconfirmed within the configured freshness window.
- Track false-positive domain classification, duplicate rate, stale listing rate and user-reported issue rate.
- Measure click-to-application success and detail-page 5xx rate.

### Mentorship and project delivery
- Every active fellow has a named mentor and backup.
- Track first mentor response time, PR review turnaround and missed-review rate.
- Track PR acceptance rate and rework cycles by cohort, not to punish learners but to improve coaching.
- Count releases/features accepted, not just raw commits.
- Record project delivery satisfaction from project owners and fellows.

### Stipend and learner outcomes
- Track eligible vs paid fellows and median actual paid amount.
- Track payment on-time rate and dispute resolution time.
- Track completion, withdrawal, credential issuance and reason for non-completion.
- Track placement outcomes only where verified and consented; use a defined 3/6/12-month follow-up window.

### Talent marketplace
- Number of opt-in vetted engineers by domain/level.
- Percentage with current availability and recent evidence.
- Time to qualified shortlist, interview and offer.
- Offer acceptance, trial conversion, 30/90-day retention and employer repeat rate.
- Candidate satisfaction, drop-off and grievance rate.

### Platform health
- Build/test pass rate.
- Availability and error rate by application surface.
- API latency and search latency.
- Payment/email/credential webhook failure rate.
- Backup restore success and security patch SLA.

---

## 7. Navigation and content structure recommendation

Preserve current URLs but gradually make the user experience consistent.

### `dbert.in`

- `/` — clear studio proposition and three paths: Startups, Learners, Employers.
- `/studio` or existing equivalent — venture studio model, portfolio and incubated projects.
- `/products` — real SaaS products with status/demo/docs.
- `/labs` — publications, open source, model cards and reproducible results.
- `/learners` — pathway comparison and cohort discovery.
- `/learners/programmes/*` — authoritative programme pages.
- `/about/team` — approved staff/mentor/advisor roster.
- `/about/credentials` — legal identity, Udyam verification and clear accreditation disclaimer.
- `/verify` — exact-ID credential verification.
- `/talent` — public summary of hiring standards and opt-in talent process; no bulk private directory.
- `/outcomes` — cohort outcome dashboard with definitions.

### `lms.dbert.in`

- `/` — learner dashboard/landing, clear programme chooser.
- `/courses` — learning products, separately labelled.
- `/internships` — active direct/partner/sourced roles with clear source badges.
- `/internships/{slug}` — complete role description.
- `/jobs` — permanent/contract jobs separately from internships.
- `/application/*` — application status and required actions.
- `/cohorts/*` — cohort calendar, onboarding and milestones.
- `/tasks` — sprint tasks and deliverables.
- `/mentors` — assigned mentor, session scheduling, review queue.
- `/portfolio` — learner's private proof-of-work and exportable public portfolio controls.
- `/payments` — private fee/deposit/stipend history.
- `/credentials` — learner's own credentials and exact-ID verification.
- `/employer/*` — employer onboarding and candidate discovery if existing architecture supports this role.

These are target IA suggestions, not instructions to rename all existing routes. Prefer route aliases and redirects over breaking URL changes.

---

## 8. Prioritisation: what should be built first

| Priority | Work item | Why |
|---|---|---|
| P0 | Repository map, baseline tests and safety checks | Prevent accidental regressions |
| P0 | Programme/fee/stipend/offer consistency | Highest trust and legal/financial risk |
| P0 | Candidate privacy and exact-ID verification | Protects existing learner data |
| P1 | Listing source verification and taxonomy | Makes the internship board credible |
| P1 | Named mentor operations and capacity | Makes the mentorship promise deliverable |
| P1 | Intern lifecycle and stipend ledger | Turns promises into trackable operations |
| P1 | GitHub/PR evidence and proof-of-work graph | Creates the core differentiation |
| P2 | Employer portal and consented talent roster | Creates a real hiring marketplace |
| P2 | Research/product evidence and portfolio | Strengthens technical credibility |
| P2 | UX, accessibility, performance and advanced analytics | Improves reach and usability |

### First 30-day implementation target

Do not attempt to build the entire roadmap in one sprint. A realistic first release should focus on:
1. Complete Phase 0 audit.
2. Approve programme/fee/stipend policy decisions.
3. Implement one source of truth for programme facts and update the most visible pages.
4. Fix candidate-directory privacy exposure after owner/legal review.
5. Add accurate listing source badges and correct the most obvious category errors.
6. Add smoke tests for all public and application-critical routes.

### 60–90-day target

1. Launch mentor profiles and internal mentor capacity view.
2. Launch role-specific candidate vetting workflow.
3. Add project briefs, PR review evidence and stipend ledger.
4. Publish the first cohort outcome dashboard with audited definitions.
5. Pilot a consented employer-facing talent shortlist with one or two verified employers.

These dates are planning horizons, not delivery guarantees. The agent must report blockers and avoid compressing testing to meet a calendar target.

---

## 9. Human approval gates

The agent must stop and ask for approval before:

- Changing any fee, deposit, refund, stipend or placement policy.
- Editing legal terms, privacy policy, IP terms, employment/contract status or partner agreement templates.
- Publishing staff, mentor, fellow, intern or employer identities.
- Exposing any candidate profile or performance score publicly.
- Changing certificate issuance, hashes, identifiers, revocation or verification rules.
- Modifying production payment, email, domain, DNS, auth or storage integrations.
- Running production migrations, backfills, bulk updates or deployment.
- Publishing claims such as “top 1%”, “top 3%”, “guaranteed”, “accredited”, “peer-reviewed”, “on-chain”, “production”, “live”, “verified” or “placement rate”.

For each gate, present: proposed change, affected routes/tables, user impact, legal/privacy impact, test evidence, rollback plan and unresolved questions.

---

## 10. Definition of done for the complete roadmap

DBERT should not call the platform transformation complete until all of the following are true:

- The two domains have clear, consistent responsibilities and working cross-domain journeys.
- Every programme's current terms are defined in one approved source and match the user-facing pages.
- Training, internship, fellowship, job and sourced lead are clearly distinguished.
- The internship marketplace has reliable taxonomy, source labels, employer verification, freshness, deduplication and correct counts.
- Staff, mentors, fellows, interns, alumni and pre-vetted engineers are separate, governed concepts.
- Every active fellow has an approved agreement, project brief, mentor and deliverables.
- Mentors have verified profiles, capacity and review SLAs.
- “Pre-vetted engineer” is backed by a versioned assessment rubric and consented evidence.
- Public credential verification is privacy-preserving and exact-ID based.
- Accepted project contributions are traceable to issue, PR, review, test and release evidence.
- Stipends and refunds are auditable and visible to the right user.
- Public outcomes are generated from data with definitions, denominators and timestamps.
- Research and product claims link to reproducible evidence or are labelled accurately.
- Security, accessibility, performance, backup/restore and regression testing are established.
- Existing users, historical records, certificates, saved URLs and application journeys continue to work.

---

## 11. Instructions to the local AI coding agent

Use this as your operating prompt:

> You are the implementation agent for the DBERT Platform Evolution Roadmap. Work only in the provided local repository and authorised local/staging environment. Start with Phase 0 in read-only mode. Inspect the current code, data model, routes, APIs, integrations and tests before suggesting code changes. Do not assume that the public website description is the implementation truth. Produce the Phase 0 audit deliverables and a dependency-aware plan.
>
> After Phase 0, implement one phase at a time in a separate branch/commit series. Before each phase, state the files, tables, routes, APIs and integrations likely to be affected. Prefer existing abstractions and additive, backward-compatible changes. Preserve user data, historical records, public URLs, certificate IDs and payment behaviour. Do not run destructive commands or production migrations. Do not change legal/financial policy, publish personal data, make hiring decisions automatically, or deploy without explicit approval.
>
> For every change, add tests, run the complete relevant regression suite, compare with the Phase 0 baseline and write a concise implementation report. If a test fails, identify whether it is pre-existing or introduced by the change; never silence, delete or weaken a test merely to get a green build. If the existing architecture cannot support a requirement safely, stop and propose options rather than rewriting the application.
>
> Treat all public claims, people records, company relationships, stipend terms and programme outcomes as untrusted until verified against authorised source data. Keep candidate/staff/mentor data private by default. Only publish profiles with recorded consent. Use human review for all candidate vetting and placement decisions.
>
> Do not continue to the next phase until the current phase's acceptance criteria, tests, rollback plan and human approval gates are satisfied.

### Expected final report after each phase

1. Phase and goal.
2. What was inspected.
3. Files/routes/API/database entities changed.
4. Migration details and backward-compatibility approach.
5. Tests run and exact results.
6. Screenshots or evidence of changed user journeys.
7. Security/privacy impact.
8. Known limitations and unresolved owner decisions.
9. Rollback procedure.
10. Recommendation: proceed, hold or rollback.

---

## 12. Public sources used for this audit

All observations below are from publicly accessible pages reviewed on **9 November 2026**. Counts and listings are dynamic and can change. The public review does not prove the accuracy of every DBERT-authored claim and does not provide access to private LMS records or source code.

### Corporate, team and talent

- [DBERT homepage](https://dbert.in/)
- [DBERT About](https://dbert.in/about)
- [DBERT technical leadership / mentors](https://dbert.in/about/team)
- [DBERT credentials and institutional information](https://dbert.in/about/credentials)
- [DBERT pre-vetted engineer hiring page](https://dbert.in/hire/pre-vetted-engineers)
- [DBERT careers and hiring cohorts](https://dbert.in/about/careers)
- [Aivara Technologies 2026 cohort](https://dbert.in/cohorts/aivara)
- [DBERT Labs](https://dbert.in/labs)
- [DBERT open-source page](https://dbert.in/labs/opensource)
- [DBERT publications](https://dbert.in/labs/publications)
- [Alkame case study](https://dbert.in/startups/portfolio/alkame)

### Learner and LMS platform

- [DBERT LMS homepage](https://lms.dbert.in/)
- [Internship marketplace](https://lms.dbert.in/internships)
- [AI Agent Development internship domain](https://lms.dbert.in/internships/ai-agent-development)
- [Courses](https://lms.dbert.in/courses)
- [Jobs](https://lms.dbert.in/jobs)
- [Paid programme](https://lms.dbert.in/program)
- [Terms](https://lms.dbert.in/terms)
- [Privacy policy](https://lms.dbert.in/privacy)
- [Public credential directory](https://dbert.in/verify/directory)
- [Credential verification](https://dbert.in/verify)
- [Domain migration notice](https://dbert.in/dbert-online)
- [Public Alkame GitHub repository](https://github.com/Alkameinc/alkame-nifty-50-educational/)

---

**End of roadmap.**
