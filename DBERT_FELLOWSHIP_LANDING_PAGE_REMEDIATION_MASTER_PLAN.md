# DBERT Fellowship Landing Pages --- Local Remediation Master Plan

**Purpose:** Give a local AI coding agent a safe, phase-by-phase
implementation plan to audit and fix the DBERT fellowship landing pages,
course catalogue, UX, content consistency, trust signals, application
funnel, accessibility, performance, and analytics.

**Target website:** https://dbert.in/\
**Execution mode:** Local repository first; inspect before editing;
preserve the existing backend, database, authentication, payment,
application, and LMS integrations unless a change is explicitly
approved.\
**Status:** Planning baseline --- 24 November 2026\
**Document owner:** DBERT\
**Working rule:** Do not assume the previous public-site audit is a
complete technical specification. Re-verify every route, claim,
component, API, and integration against the current repository and live
site before changing it.

------------------------------------------------------------------------

## 0. Instructions to the local AI agent

You are acting as a senior product engineer, UX engineer, QA lead, and
technical writer. Your task is to remediate DBERT's fellowship
landing-page experience without destabilising the existing application.

### 0.1 Non-negotiable rules

1.  **Inspect first. Do not start by redesigning.** Identify the
    framework, routes, components, design system, API contracts,
    database models, authentication flow, payment flow, deployment
    configuration, and existing tests.
2.  **Preserve working functionality.** Do not replace or bypass
    existing APIs, database tables, authentication, payment gateways,
    application workflows, LMS links, or admin controls merely to
    simplify the frontend.
3.  **No invented claims.** Never invent placement rates, salary
    outcomes, alumni names, testimonials, employer partnerships, mentor
    credentials, project commitments, cohort dates, seat counts,
    accreditation, or refund terms.
4.  **No fake proof.** Do not create fabricated GitHub PRs, alumni
    profiles, ratings, certificates, logos, company partnerships, or
    success metrics.
5.  **No silent fallbacks.** Broken course routes must not quietly
    redirect to an unrelated course. Show a useful not-found or
    temporarily-unavailable state and log the issue.
6.  **Do not change business rules without approval.** If the
    repository's actual eligibility, fees, duration, stipend, guarantee,
    refund, or selection rules conflict with website copy, stop and ask
    through `/grill-me`.
7.  **Keep a single source of truth.** Course data should not be
    duplicated independently across homepage cards, course detail pages,
    menus, application forms, SEO metadata, and dashboards.
8.  **Use the existing stack and conventions.** Do not introduce a new
    framework, component library, state manager, CMS, analytics vendor,
    or database migration unless necessary and approved.
9.  **Work in small, reviewable increments.** Complete a phase, run its
    checks, update this document, and report changed files before
    continuing.
10. **Protect secrets and personal data.** Never print API keys,
    credentials, student PII, payment details, or production environment
    values into logs, commits, screenshots, or this plan.
11. **Do not deploy automatically.** Local changes only unless the user
    explicitly authorises deployment.
12. **Do not delete existing content or routes** until references,
    inbound links, analytics, and backend dependencies have been
    checked.

### 0.2 Required use of `/grill-me`

Use `/grill-me` whenever a decision affects business policy, user
promises, data, or an ambiguous integration. Ask one focused set of
questions at a time and record the decision in `docs/decisions/`.

Mandatory clarification topics:

-   Exact canonical list of nine fellowship tracks and their public
    names.
-   Whether the six homepage tracks are the first six of the nine or a
    featured subset.
-   Canonical URL for every course and whether old URLs must redirect.
-   Fellowship fee, duration, hours/week, cohort dates, selection
    process, and prerequisites for each track.
-   Whether the ₹1,999 amount is application fee, tuition,
    seat-confirmation fee, deposit, or total program fee.
-   Exact meaning and enforceable conditions of "100% Guaranteed
    Internship Placement".
-   Whether placement means internal internship, external internship,
    employment, referral, or interview opportunity.
-   Stipend amounts, performance conditions, payment schedule, and
    eligibility.
-   Whether the ₹5,000--₹18,000 stipend range applies to all tracks or
    only specific programs.
-   Difference between the two-month fellowship and any three-month
    comprehensive course.
-   Approved venture/project mapping for each track and what work is
    genuinely available to fellows.
-   Approved mentor names, credentials, availability, and review
    responsibilities.
-   Approved alumni evidence and permission to publish names, photos,
    projects, and outcomes.
-   Salary/compensation claims and the source, sample size, period, and
    calculation method.
-   Refund, cancellation, deferral, and guarantee-remedy policy.
-   Which application, payment, CRM, WhatsApp, LMS, and analytics
    integrations are production-critical.

If no answer is available, use neutral copy or mark the field as
"Pending verification" in internal content data. Do not publish a guess.

### 0.3 Working directory and branch

-   Confirm repository root and current branch.
-   Create a feature branch such as `fix/fellowship-landing-pages`
    unless the user specifies another workflow.
-   Check `git status` before editing. Never overwrite uncommitted user
    work.
-   Record baseline commit SHA and date in the progress log.
-   Do not commit `.env`, secrets, database dumps, uploads, generated
    student data, or build artifacts.

------------------------------------------------------------------------

## 1. Outcomes and acceptance criteria

The project is complete only when all applicable criteria below pass.

### Product and information architecture

-   [ ] One authoritative catalogue contains exactly the approved nine
    tracks.
-   [ ] Homepage featured tracks and "View all" catalogue use the same
    course data source.
-   [ ] Every advertised track has one canonical, working detail URL.
-   [ ] Old URLs have deliberate redirects or useful 404 pages.
-   [ ] No internal link points to a 404, unrelated page, placeholder,
    or stale course.
-   [ ] Course names, fees, duration, dates, and CTAs are consistent
    across the site.
-   [ ] Two-month fellowship and any separate three-month course are
    clearly distinguished.

### Course detail pages

-   [ ] Every course page explains who it is for, prerequisites,
    outcomes, duration, weekly commitment, curriculum, capstone,
    evaluation, mentor/review model, fee, application steps, and FAQs.
-   [ ] Every project claim is approved and backed by a real
    repository/demo or clearly labelled as a proposed project.
-   [ ] Technical stacks are consistent between homepage cards and
    detailed curricula.
-   [ ] Course content is understandable to first-time visitors without
    hiding technical depth.
-   [ ] All claims about placement, stipend, salary, alumni, and
    partnerships are evidence-backed and policy-approved.

### Conversion and trust

-   [ ] Primary and secondary CTAs have distinct purposes.
-   [ ] Visitors can understand the application process before paying.
-   [ ] Application progress and error states are clear.
-   [ ] Payment confirmation is based on verified backend response, not
    frontend assumptions.
-   [ ] Placement guarantee terms are accessible before
    application/payment.
-   [ ] No fake countdown, fake scarcity, fabricated testimonial, or
    unsupported outcome claim exists.

### Quality

-   [ ] Responsive layout works at common mobile, tablet, and desktop
    widths.
-   [ ] Keyboard navigation and accessible labels are implemented.
-   [ ] No critical console errors or broken network requests.
-   [ ] Core routes and application flow have automated or documented
    manual tests.
-   [ ] Performance and SEO metadata are checked.
-   [ ] Analytics events do not contain sensitive personal data.
-   [ ] Existing backend/API/database contracts remain compatible.

------------------------------------------------------------------------

## 2. Initial audit: repository reconnaissance

**Do this before changing code.**

### 2.1 Discover the application

Inspect and report:

-   Framework and version.
-   Build tool and package manager.
-   App entry points and route definitions.
-   Server-side rendering/static generation approach, if any.
-   Styling system and design tokens.
-   Component library and icon system.
-   Content source (hardcoded files, database, CMS, API).
-   Backend endpoints used by course pages and application forms.
-   Authentication and session handling.
-   Payment gateway and callback/webhook handling.
-   LMS, CRM, email, WhatsApp, and analytics integrations.
-   Deployment/build configuration.
-   Existing tests, linting, type checking, and CI workflows.

Useful commands (adapt to the repository; do not assume all are
available):

``` bash
pwd
git status --short --branch
git log -5 --oneline
find . -maxdepth 2 -type f | sort | head -250
```

Then inspect `package.json`, lockfiles, README, environment examples,
route files, API clients, and deployment configuration.

### 2.2 Map the current route inventory

Create `docs/audits/route-inventory.md` with:

  -------------------------------------------------------------------------------------------------------------------------
  Route                               Source           Page purpose           Current    Incoming   Backend      Decision
                                      file/component                          status     links      dependency   
  ----------------------------------- ---------------- ---------------------- ---------- ---------- ------------ ----------
  `/`                                                  Homepage                                                  

  `/internships`                                       Track directory                                           

  `/learners/courses`                                  Course directory                                          

  `/courses/ai-agent-development`                      Course detail                                             

  `/courses/full-stack-development`                    Course detail                                             

  `/courses/generative-ai`                             Course detail                                             

  `/courses/machine-learning`                          Course detail                                             

  `/courses/data-science`                              Course detail                                             

  Backend track route                                  Course detail                                             

  `/learners`                                          Career/program info                                       

  `/pricing`                                           Pricing                                                   

  `/fellows/verified`                                  Fellow evidence                                           

  LMS routes                                           Application/learning                                      
  -------------------------------------------------------------------------------------------------------------------------

The route list above is a starting point, not an assertion that every
path is correct. Discover all nine approved track routes from the
repository and live links.

### 2.3 Audit all links and actions

Find every occurrence of:

-   `/courses/`
-   `/learners/courses`
-   `/internships`
-   `Apply`
-   `Enroll`
-   `Confirm`
-   `Payment`
-   `WhatsApp`
-   `placement`
-   `stipend`
-   `LPA`
-   `₹1,999`
-   `₹34,000`

Build a link/action map showing source component, destination, HTTP
status, expected behaviour, and whether the destination is
authenticated.

Test: - Internal links. - External links. - Buttons and forms. - Mobile
navigation. - Browser back/forward. - Direct URL load and refresh. -
Query-string preservation. - Login redirect and return-to-page
behaviour. - Payment return/callback. - Application submission and
confirmation.

### 2.4 Baseline evidence

Capture screenshots or recordings for: - Homepage desktop and mobile. -
Each of the nine course pages desktop and mobile. - Course catalogue. -
Application form. - Payment/seat confirmation path. - Error and empty
states.

Store only non-sensitive test evidence in `docs/audits/evidence/`. Do
not capture real student information.

### 2.5 Audit report

Create `docs/audits/initial-audit.md` containing:

1.  Repository and stack summary.
2.  Route inventory.
3.  Broken links and 404s.
4.  Duplicate or conflicting course data.
5.  CTA and application flow.
6.  Content inconsistencies.
7.  Backend dependencies.
8.  Accessibility issues.
9.  Performance/SEO observations.
10. Risks and questions requiring `/grill-me`.
11. Prioritised findings: P0, P1, P2, P3.

**Exit gate:** No implementation begins until the route map, integration
map, and unresolved policy questions are documented.

------------------------------------------------------------------------

## 3. Canonical course catalogue and content model

This phase removes the root cause of inconsistent course listings.

### 3.1 Establish a single source of truth

Prefer the repository's existing CMS/database/API if it is the
established source. If course data is currently static, use a typed
central data module as a transitional source. Do not create a second
competing source.

Suggested logical schema (adapt to existing models; do not blindly add a
database table):

``` ts
type FellowshipTrack = {
  id: string;                 // stable identifier, e.g. "ai-agent-engineering"
  slug: string;               // canonical URL slug
  name: string;               // approved public name
  shortDescription: string;
  fullDescription: string;
  featured: boolean;
  displayOrder: number;
  status: "published" | "draft" | "archived";
  duration: string;           // approved display value
  fee: {
    amount: number;
    currency: "INR";
    label: string;            // approved explanation of what fee represents
  };
  weeklyCommitment?: string;
  prerequisites: string[];
  outcomes: string[];
  technologies: string[];
  curriculum: Array<{
    week: number;
    title: string;
    topics: string[];
    deliverable: string;
  }>;
  capstone: {
    title: string;
    description: string;
    status: "available" | "proposed" | "example";
    repositoryUrl?: string;
    demoUrl?: string;
  };
  evaluation: string[];
  mentorIds: string[];
  projectIds: string[];
  placementPolicyUrl?: string;
  faq: Array<{ question: string; answer: string }>;
  seo: {
    title: string;
    description: string;
    canonicalUrl: string;
  };
};
```

Only include fields supported by the existing business model. Do not add
unsupported promises just because the schema has a field.

### 3.2 Approved catalogue candidates

The earlier public homepage presented these six featured tracks:

1.  Autonomous AI Agent Engineering.
2.  Full Stack Web Development.
3.  Generative AI & LLM Systems.
4.  Machine Learning & MLOps.
5.  Data Science & Predictive Analytics.
6.  Backend Systems & Microservices.

The earlier directory appeared to contain additional tracks such as
DevOps, Python Automation, UI/UX, Cybersecurity, and Mobile Development.
**Do not assume these are the final nine.** Use `/grill-me` to confirm
the canonical nine and their display names.

### 3.3 Catalogue consistency rules

-   Homepage featured cards must be derived from the canonical
    catalogue.
-   "View all tracks" must display the same catalogue, filtered by
    published status.
-   Search, filters, navigation, course detail pages, and application
    track choices must use the same IDs.
-   A course must not be selectable in the application form if it is
    unpublished or closed.
-   Display order must be data-driven.
-   Do not duplicate fee, duration, or course name in multiple
    components.
-   Add schema validation and tests for missing slugs, duplicate IDs,
    duplicate slugs, invalid URLs, and unpublished courses being
    exposed.

### 3.4 Route strategy

Choose one canonical route pattern. Recommended only if compatible with
current routing:

``` text
/fellowships
/fellowships/ai-agent-engineering
/fellowships/full-stack-web-development
/fellowships/generative-ai-llm-systems
/fellowships/machine-learning-mlops
/fellowships/data-science-predictive-analytics
/fellowships/backend-systems-microservices
```

If existing `/courses/...` URLs already have search traffic or external
links, they may remain canonical. Do not migrate URLs just for naming
preference.

For every legacy route: - Add a permanent redirect only when the
destination is semantically equivalent. - Preserve query parameters when
required. - Do not redirect unrelated courses to the homepage. - Use a
proper 404 for removed pages without an equivalent. - Add canonical
metadata to avoid duplicate indexing.

**Exit gate:** All nine approved courses appear in the same catalogue,
and all advertised course links resolve correctly.

------------------------------------------------------------------------

## 4. Phase-by-phase implementation plan

Track progress using the checkboxes and status table. Update this file
after every completed phase.

### Phase 0 --- Safety, baseline, and decision capture

**Priority:** P0\
**Estimated effort:** 0.5--1 day, depending on repository size.

Tasks: - \[ \] Confirm repository, branch, and clean/dirty working
tree. - \[ \] Record baseline commit SHA. - \[ \] Identify framework,
backend, database, auth, payment, LMS, and analytics. - \[ \] Create
`docs/audits/initial-audit.md`. - \[ \] Create
`docs/audits/route-inventory.md`. - \[ \] Capture baseline
screenshots. - \[ \] Identify all course routes and CTA destinations. -
\[ \] Record policy/content questions for `/grill-me`. - \[ \] Confirm
backup/rollback method.

Deliverables: - Initial audit. - Route inventory. - Integration map. -
Decision log. - Baseline screenshots.

Tests: - \[ \] Existing build passes. - \[ \] Existing tests pass or
baseline failures are documented. - \[ \] No uncommitted work was
overwritten.

**Exit gate:** Baseline is documented and business-critical unknowns are
listed.

### Phase 1 --- Repair route failures and navigation

**Priority:** P0\
**Estimated effort:** 1--3 days.

Tasks: - \[ \] Fix broken ML/MLOps course destination. - \[ \] Fix
broken Data Science destination. - \[ \] Create/repair Backend Systems
destination. - \[ \] Verify all nine course destinations. - \[ \] Repair
homepage "View all" destination. - \[ \] Reconcile homepage, internship
directory, learner course directory, and application choices. - \[ \]
Remove dead links and stale CTA targets. - \[ \] Add useful not-found
and temporarily-unavailable states. - \[ \] Add redirects only for
equivalent legacy pages. - \[ \] Ensure direct URL loading and refresh
work. - \[ \] Verify mobile navigation and browser history.

Tests: - \[ \] Automated route smoke test for all published tracks. - \[
\] No internal 404 links. - \[ \] All course cards navigate to the
matching detail page. - \[ \] All course pages link back to the correct
catalogue. - \[ \] No unrelated redirect. - \[ \] No console errors
during navigation.

Deliverables: - Working course routes. - Unified navigation. - Route
test report.

**Exit gate:** No advertised track leads to a broken or unrelated
destination.

### Phase 2 --- Canonical course data and catalogue

**Priority:** P0\
**Estimated effort:** 1--3 days.

Tasks: - \[ \] Confirm final nine-track list through `/grill-me`. - \[
\] Implement or reuse one authoritative data source. - \[ \] Define
stable course IDs and canonical slugs. - \[ \] Set featured flags and
display order. - \[ \] Ensure all catalogue surfaces consume the same
source. - \[ \] Ensure application form uses canonical course IDs. - \[
\] Add validation for duplicate IDs/slugs and missing required fields. -
\[ \] Add published/draft/archived handling. - \[ \] Confirm fee and
duration are not independently hardcoded. - \[ \] Add tests for course
data integrity.

Tests: - \[ \] Homepage featured courses match the approved catalogue. -
\[ \] "View all" shows every published course. - \[ \] No duplicate
course. - \[ \] Application selection matches published courses. - \[ \]
Draft courses are not publicly accessible unless preview is authorised.

Deliverables: - Canonical course model/data source. - Updated
catalogue. - Data integrity tests.

**Exit gate:** One course record controls every public representation of
that course.

### Phase 3 --- Shared landing-page design system

**Priority:** P1\
**Estimated effort:** 2--4 days.

Build reusable components using the current design system:

-   [ ] Course hero.
-   [ ] Trust/evidence strip.
-   [ ] Course outcome summary.
-   [ ] Project/capstone showcase.
-   [ ] Technology stack list.
-   [ ] Prerequisite section.
-   [ ] Week-by-week curriculum accordion.
-   [ ] Mentor profile.
-   [ ] Evaluation and deliverables.
-   [ ] Fellowship fee/duration panel.
-   [ ] Placement-policy summary.
-   [ ] Alumni/project evidence card.
-   [ ] FAQ accordion.
-   [ ] Primary and secondary CTA.
-   [ ] Application confirmation state.
-   [ ] Breadcrumbs.
-   [ ] Related tracks.

Design rules: - Keep one primary CTA per viewport where practical. - Use
clear heading hierarchy and short paragraphs. - Avoid excessive badges,
animations, carousels, and decorative cards. - Do not make salary claims
the visual hero. - Use real project screenshots only when approved and
current. - Use neutral placeholders for missing assets; do not fabricate
project UI. - Maintain the existing light-theme direction unless the
product owner approves otherwise. - Ensure layouts work at 320px, 375px,
768px, 1024px, and 1440px widths.

Tests: - \[ \] Shared components render with missing optional data. - \[
\] No layout overflow at target widths. - \[ \] Keyboard focus is
visible. - \[ \] Heading order is logical. - \[ \] CTA destinations are
correct.

Deliverables: - Shared component library. - Responsive page template. -
Component tests or documented manual checks.

**Exit gate:** All course pages can use a consistent template without
forcing identical course content.

### Phase 4 --- Rewrite and verify course content

**Priority:** P1\
**Estimated effort:** 3--6 days, dependent on policy approvals.

For every track, complete the content worksheet below. The agent may
draft copy, but any factual claim must be verified by an authorised
source.

#### 4.1 Required content worksheet for every track

-   [ ] Approved course title.
-   [ ] One-sentence outcome-focused value proposition.
-   [ ] Who should apply.
-   [ ] Who should not apply / prerequisite level.
-   [ ] Required weekly time commitment.
-   [ ] Exact duration and cohort dates.
-   [ ] What students will learn.
-   [ ] Week-by-week topics and deliverables.
-   [ ] Final capstone project.
-   [ ] Repository/demo link, if available.
-   [ ] Whether the project is live, proposed, or illustrative.
-   [ ] Technologies and why each is used.
-   [ ] Mentor/reviewer details.
-   [ ] Evaluation and completion criteria.
-   [ ] Fee and what it covers.
-   [ ] Application and selection process.
-   [ ] Placement policy link and conditions.
-   [ ] Stipend policy, if applicable.
-   [ ] Refund/cancellation terms.
-   [ ] FAQs.
-   [ ] SEO title and description.

#### 4.2 Track-specific content direction

**A. Autonomous AI Agent Engineering**

Explain: - Agent loops and state. - Tool calling and permissions. -
LangGraph/CrewAI roles and trade-offs. - Memory and persistence. -
Human-in-the-loop approval. - Evaluation, tracing, failure recovery, and
security.

Suggested capstone concept: a research/task agent that plans, delegates,
uses approved tools, validates outputs, and produces a cited report.
Label it proposed unless a real project is approved.

**B. Full Stack Web Development**

Explain: - React/Next.js fundamentals. - TypeScript and component
architecture. - API integration. - Authentication and role-based
access. - PostgreSQL schema and migrations. - Testing, deployment,
observability, and security.

Suggested capstone concept: a complete SaaS workflow with
authentication, role-based dashboard, database, APIs, and deployment.

**C. Generative AI & LLM Systems**

Explain: - Data ingestion and chunking. - Embeddings and vector
stores. - Hybrid retrieval and reranking. - RAG evaluation. -
Prompt/model routing. - Fine-tuning/QLoRA prerequisites and
limitations. - Inference serving and monitoring.

Suggested capstone concept: an evaluated knowledge assistant with
ingestion, hybrid retrieval, reranking, LLM response, and measurable
quality metrics.

**D. Machine Learning & MLOps**

Do not conflate classical ML, LLM fine-tuning, and MLOps. Explain the
actual balance.

Where applicable cover: - Data validation and feature engineering. -
Baselines and model evaluation. - Experiment tracking. - Model
registry. - Reproducible training. - Docker/model serving. - Monitoring
and drift. - Retraining and rollback.

Suggested capstone concept: a reproducible predictive model with tracked
experiments, deployed inference endpoint, monitoring, and documented
evaluation.

**E. Data Science & Predictive Analytics**

Clearly distinguish analytics from data science.

Cover the approved balance of: - SQL and data extraction. - Data
cleaning and quality. - Statistics and exploratory analysis. - Feature
engineering. - Forecasting/predictive modelling. - Dashboarding and
business interpretation. - Communicating uncertainty and model
limitations.

Suggested capstone concept: a business dataset analysis with a dashboard
and a defensible predictive component.

**F. Backend Systems & Microservices**

Explain: - API design and versioning. - Authentication and
authorisation. - SQL transactions and migrations. - Caching. -
Queues/event-driven architecture. - Observability and error handling. -
Integration and load testing. - Deployment and security.

Do not claim Kafka, Go, or microservices are used in a live project
unless confirmed. Clearly distinguish required tools from optional
exposure.

**G--I. Remaining tracks**

Wait for the approved catalogue. Do not invent the remaining track names
or curricula. Apply the same content worksheet once confirmed.

#### 4.3 Technology consistency

For each course, compare: - Homepage stack badges. - Detail-page
curriculum. - Project repository dependencies. - Mentor delivery
capability. - Application form description.

If the homepage lists a technology not taught or used, remove it or
explain its role. Avoid technology-name stuffing.

**Exit gate:** All public course claims are approved, consistent,
understandable, and backed by evidence where required.

### Phase 5 --- Placement, stipend, pricing, and policy transparency

**Priority:** P0 for public claims\
**Estimated effort:** 1--3 days after business decisions.

This phase is not a legal opinion. Route final policies through DBERT's
authorised management/legal reviewer.

Tasks: - \[ \] Define "placement" precisely. - \[ \] Define whether the
guarantee means internal internship, external internship, job, referral,
or interview. - \[ \] Define eligibility and selection conditions. - \[
\] Define attendance and participation requirements. - \[ \] Define
assessment and project completion requirements. - \[ \] Define placement
timeline. - \[ \] Define what happens if no placement is provided. - \[
\] Define stipend eligibility and payment conditions. - \[ \]
Distinguish guaranteed stipend from performance-linked incentives. - \[
\] Explain ₹1,999 and every other fee. - \[ \] Explain fellowship versus
comprehensive course pricing. - \[ \] Publish
refund/cancellation/deferral rules. - \[ \] Link the policy beside
relevant claims and before payment. - \[ \] Remove or qualify
unsupported salary and compensation figures. - \[ \] Record the evidence
source for each published outcome statistic.

#### Claims register

Create `docs/content/claims-register.md`:

  -------------------------------------------------------------------------------------
  Claim          Public      Evidence source        Owner       Approved?   Review date
                 location                                                   
  -------------- ----------- ---------------------- ----------- ----------- -----------
  100% placement             Signed policy                                  
  guarantee                                                                 

  Compensation               Verified outcome                               
  range                      dataset                                        

  Stipend range              Stipend policy                                 

  Alumni count               Completion records                             

  Employer                   Current                                        
  partner                    agreement/permission                           

  Mentor                     Verified profile                               
  experience                                                                

  Live project               Approved project                               
  access                     backlog                                        
  -------------------------------------------------------------------------------------

Rules: - No claim without a named owner and evidence. - No public use of
an employer logo without permission. - No "average" or "median" without
a reproducible calculation. - State sample size and date range for
outcome statistics. - Do not imply internship placement is a full-time
job. - Do not imply every applicant is selected if screening exists.

**Exit gate:** All high-risk public claims have written approval and
accessible terms.

### Phase 6 --- Project, mentor, and alumni proof

**Priority:** P1\
**Estimated effort:** 2--5 days, depending on available evidence.

Tasks: - \[ \] Map each track to approved project opportunities. - \[ \]
Identify whether each project is active, planned, or illustrative. - \[
\] Link real repositories and demos. - \[ \] Show a small, reviewable
example of expected work. - \[ \] Explain code review and acceptance
standards. - \[ \] Publish mentor profiles only with approval. - \[ \]
Publish alumni profiles only with consent. - \[ \] Show actual merged
PRs or project deliverables where permitted. - \[ \] Add a verification
method for public credentials if available. - \[ \] Remove repeated or
generic testimonial cards. - \[ \] Add a clear "no alumni evidence
available yet" state rather than inventing evidence.

Suggested evidence card fields:

-   Fellow name or consented public identifier.
-   Cohort.
-   Track.
-   Project contribution.
-   Repository/PR links.
-   Reviewer.
-   Assessment method.
-   Completion status.
-   Internship outcome, only if verified and consented.

**Exit gate:** Every proof item is real, permissioned, traceable, and
current.

### Phase 7 --- Application funnel and payment UX

**Priority:** P1\
**Estimated effort:** 2--5 days; backend coordination may be required.

First map the existing application/payment workflow. Preserve API
contracts and database behaviour.

Recommended user journey:

1.  Explore a track.
2.  Review curriculum, prerequisites, fee, policies, and outcomes.
3.  Start application.
4.  Authenticate or create account if required.
5.  Enter required application details.
6.  Select the canonical track ID.
7.  Review application.
8.  Submit application.
9.  Receive a real application reference/status.
10. Complete payment only at the correct approved stage.
11. Verify payment through the existing trusted backend/webhook.
12. Show enrolment confirmation only after backend confirmation.
13. Provide a dashboard/application status link.

Tasks: - \[ \] Distinguish "Apply" from "Confirm seat/pay". - \[ \]
Explain whether payment is due before or after selection. - \[ \] Avoid
collecting unnecessary personal information. - \[ \] Preserve partially
completed applications if supported. - \[ \] Add field-level validation
and actionable error messages. - \[ \] Preserve form data after
recoverable errors. - \[ \] Prevent duplicate submissions. - \[ \]
Handle payment pending, failed, cancelled, and successful states. - \[
\] Verify payment status server-side. - \[ \] Never trust a frontend
success redirect as proof of payment. - \[ \] Make confirmation
idempotent. - \[ \] Preserve attribution and course selection through
login. - \[ \] Ensure accessibility and mobile usability. - \[ \] Test
email/WhatsApp confirmation only through approved integrations.

Security checks: - Do not expose payment secrets. - Do not accept
client-supplied price as authoritative. - Verify amount, currency, order
ID, and payment status server-side. - Validate webhook signatures using
existing provider guidance. - Do not log full payment payloads or
personal information. - Apply server-side rate limiting and spam
protection consistent with the existing stack.

**Exit gate:** A test applicant can complete the approved journey
without dead ends, duplicate records, or false success states.

### Phase 8 --- Engagement features

**Priority:** P2\
**Estimated effort:** 2--5 days.

Build only after the core catalogue and funnel work.

Possible features: - \[ \] Fellowship Matchmaker quiz. - \[ \]
Search/filter by domain and experience level. - \[ \] Project demo
gallery. - \[ \] Expandable weekly curriculum. - \[ \] Mentor
introduction video. - \[ \] Cohort timeline. - \[ \] FAQ search. - \[ \]
WhatsApp admissions handoff. - \[ \] Application progress indicator. -
\[ \] Save/resume application. - \[ \] Related course recommendations.

Matchmaker rules: - Recommendations must use approved course metadata. -
Do not promise admission or placement based on quiz answers. - Explain
why a track is recommended. - Allow users to browse all tracks without
completing the quiz. - Do not collect sensitive personal data in the
quiz. - Provide a clear route to a human admissions contact.

**Exit gate:** Added features are useful, accessible, privacy-conscious,
and do not obscure the primary application action.

### Phase 9 --- SEO, accessibility, performance, and analytics

**Priority:** P1/P2\
**Estimated effort:** 2--4 days.

#### SEO

-   [ ] Unique title and meta description per course.
-   [ ] Canonical URL.
-   [ ] Correct index/noindex behaviour.
-   [ ] Open Graph and social preview metadata.
-   [ ] Sitemap includes only canonical published pages.
-   [ ] Robots rules checked.
-   [ ] Breadcrumbs and semantic headings.
-   [ ] Structured data only when accurate and eligible.
-   [ ] Internal links use canonical routes.
-   [ ] No duplicate course descriptions across URLs.
-   [ ] Verify redirects and canonical tags.

Do not add fake review/rating structured data or unsupported
job-placement schema.

#### Accessibility

-   [ ] Semantic landmarks.
-   [ ] One clear H1 per page.
-   [ ] Logical heading order.
-   [ ] Keyboard-operable navigation and accordions.
-   [ ] Visible focus states.
-   [ ] Accessible labels and error descriptions.
-   [ ] Sufficient text/background contrast.
-   [ ] Meaningful alt text for informative images.
-   [ ] Empty alt text for decorative images.
-   [ ] Reduced-motion support.
-   [ ] No colour-only status indicators.
-   [ ] Touch targets appropriate for mobile.

Target WCAG 2.2 AA where practical.

#### Performance

Measure before and after: - Largest Contentful Paint (LCP). -
Interaction to Next Paint (INP). - Cumulative Layout Shift (CLS). -
Image payload. - JavaScript bundle size. - Font loading. - Third-party
scripts. - Server/API response time.

Optimise: - Responsive images and modern formats. - Lazy-load
below-the-fold media. - Avoid loading large video embeds before
interaction. - Remove unused scripts and styles. - Use appropriate
caching. - Avoid layout shifts from images and fonts. - Do not sacrifice
accessibility or tracking correctness for synthetic scores.

#### Analytics

Use the existing approved analytics platform. If none exists, ask before
adding one.

Recommended events:

``` text
page_view
fellowship_catalogue_view
fellowship_card_click
fellowship_detail_view
curriculum_expand
project_demo_click
placement_policy_view
faq_expand
application_start
application_step_complete
application_submit
eligibility_result
payment_start
payment_success
payment_failure
enrolment_confirmed
whatsapp_admissions_click
```

Rules: - Never send name, email, phone, CV contents, application
answers, payment details, or other PII in analytics event properties. -
Use canonical course ID as a non-sensitive event property. - Do not
count a payment redirect as payment success. - Define event ownership
and consent requirements. - Test event firing and duplicate
prevention. - Build a funnel report only after events are validated.

**Exit gate:** Core pages meet agreed quality thresholds and analytics
reflect real backend-confirmed states.

### Phase 10 --- Full regression, documentation, and handover

**Priority:** P0 before release\
**Estimated effort:** 1--3 days.

Tasks: - \[ \] Run production build. - \[ \] Run lint and type checks. -
\[ \] Run unit/component tests. - \[ \] Run route tests. - \[ \] Run
application-flow tests. - \[ \] Run payment sandbox tests if available
and authorised. - \[ \] Run mobile and desktop checks. - \[ \] Check
accessibility. - \[ \] Check SEO metadata and sitemap. - \[ \] Check
browser console and network requests. - \[ \] Verify no secrets or
personal data entered Git. - \[ \] Compare before/after screenshots. -
\[ \] Document changed files and architecture. - \[ \] Document
environment variables without values. - \[ \] Document deployment and
rollback steps. - \[ \] Update README and developer setup
instructions. - \[ \] Prepare release notes. - \[ \] Obtain explicit
approval before deployment.

Deliver: - `docs/audits/final-audit.md` -
`docs/decisions/decision-log.md` - `docs/content/claims-register.md` -
`docs/testing/regression-report.md` - `docs/release/rollback.md` -
Updated README/development guide.

**Exit gate:** All critical tests pass, unresolved issues are disclosed,
and the user approves release.

------------------------------------------------------------------------

## 5. Track-by-track landing page specification

Use this as the minimum content checklist for each course. Do not
publish proposed project ideas as existing live projects.

### 5.1 Autonomous AI Agent Engineering

**Hero outcome:** Build and evaluate tool-using AI agents that can plan,
execute, recover from errors, and request human approval.

Required content: - Agent architecture and state management. -
Tool/function calling. - LangGraph/CrewAI roles and trade-offs. - Memory
and persistence. - Permission boundaries and human approval. -
Observability, tracing, and evaluation. - Failure recovery and
security. - Capstone and measurable acceptance criteria.

Potential capstone: research/task agent with controlled tools,
delegation, source validation, and structured output.

### 5.2 Full Stack Web Development

**Hero outcome:** Build, test, and deploy a complete web application
with frontend, backend, database, authentication, and operational
basics.

Required content: - React/Next.js and TypeScript. - Component
architecture. - API design and integration. - PostgreSQL and
migrations. - Authentication and role-based access. - Testing and
deployment. - Security and performance. - Capstone acceptance criteria.

Potential capstone: a full SaaS workflow with user roles, dashboard,
APIs, database, and deployment.

### 5.3 Generative AI & LLM Systems

**Hero outcome:** Build an evaluated LLM application using retrieval,
orchestration, and reliable inference.

Required content: - Data ingestion and chunking. - Embeddings/vector
database. - Hybrid retrieval and reranking. - RAG evaluation. -
Prompt/model routing. - Fine-tuning prerequisites and limits. -
Inference deployment and monitoring.

Potential capstone: enterprise knowledge assistant with an evaluation
report.

### 5.4 Machine Learning & MLOps

**Hero outcome:** Train, evaluate, deploy, and monitor a reproducible
machine-learning model.

Required content: - Data quality and feature engineering. - Baseline
models and metrics. - Experiment tracking. - Model registry. -
Reproducible pipelines. - Containerised serving. - Drift monitoring and
retraining.

Potential capstone: deployed predictive model with tracked experiments
and monitoring.

### 5.5 Data Science & Predictive Analytics

**Hero outcome:** Turn raw data into defensible analysis, useful
predictions, and decision-ready dashboards.

Required content: - SQL and data ingestion. - Cleaning and validation. -
Statistics and EDA. - Feature engineering. - Forecasting/model
evaluation. - Visualisation and dashboards. - Business interpretation
and uncertainty.

Potential capstone: business analytics project with a predictive
component and dashboard.

### 5.6 Backend Systems & Microservices

**Hero outcome:** Build secure, testable backend services with reliable
data and event-processing workflows.

Required content: - API design and versioning. - Authentication and
authorisation. - SQL transactions and migrations. - Caching. - Queues
and event-driven patterns. - Observability and failure handling. -
Integration/load testing. - Deployment and security.

Potential capstone: internship/application management API. Confirm
project access and scope before presenting it as a live assignment.

### 5.7--5.9 Remaining tracks

Do not infer names from old pages or search snippets. Confirm the
official catalogue through `/grill-me`, then complete the same
specification.

------------------------------------------------------------------------

## 6. UX content and interaction standards

### 6.1 Recommended course page order

1.  Breadcrumb.
2.  Course title and outcome-focused description.
3.  Fee, duration, cohort, and weekly commitment --- only verified
    values.
4.  Primary application CTA.
5.  Trust/evidence strip.
6.  "What you will build" demo.
7.  Who should apply and prerequisites.
8.  Learning outcomes.
9.  Week-by-week curriculum and deliverables.
10. Capstone and repository/demo.
11. Mentorship and code review.
12. Assessment/completion criteria.
13. Placement and stipend policy summary.
14. Fee and payment explanation.
15. FAQs.
16. Final CTA.

### 6.2 CTA language

Use labels that accurately describe the next step:

-   `Explore curriculum`
-   `View project demo`
-   `Check eligibility`
-   `Apply for fellowship`
-   `Continue application`
-   `Confirm selection`
-   `Proceed to payment`

Do not use "Confirm seat" if the student has not been selected or if
payment is not actually the next step.

### 6.3 Empty/error/loading states

Every dynamic section needs: - Loading state. - Empty state. - Error
state. - Retry action where appropriate. - Accessible status
announcement.

Examples: - Course temporarily unavailable. - No cohort currently
open. - Project demo not yet published. - Application could not be
submitted; saved data remains available if supported. - Payment
verification pending; do not pay again until status is checked.

------------------------------------------------------------------------

## 7. Test plan

### 7.1 Route and catalogue tests

-   [ ] All published course routes return expected status.
-   [ ] All course cards link to the correct slug.
-   [ ] Every canonical URL loads directly.
-   [ ] Browser refresh works.
-   [ ] Legacy redirects are correct.
-   [ ] No duplicate course IDs/slugs.
-   [ ] Unpublished courses are not exposed.
-   [ ] Catalogue and application choices match.

### 7.2 Content consistency tests

Where practical, add automated checks for: - Same fee displayed on card
and detail page. - Same duration displayed on card and detail page. -
Course stack labels are consistent. - No stale course name. - No
unsupported placeholder salary claim. - Every placement CTA links to the
approved policy. - Every public claim has a claims-register entry.

### 7.3 Form and payment tests

Use test accounts and sandbox credentials only.

-   [ ] Required field validation.
-   [ ] Invalid email/phone handling.
-   [ ] Double-click/duplicate submit.
-   [ ] Network timeout.
-   [ ] Server validation error.
-   [ ] Login expiry.
-   [ ] Back/forward navigation.
-   [ ] Payment pending.
-   [ ] Payment failure.
-   [ ] Payment cancellation.
-   [ ] Successful verified payment.
-   [ ] Invalid/duplicate webhook.
-   [ ] Refresh after payment.
-   [ ] Confirmation email/notification failure.

### 7.4 Responsive tests

Test at minimum: - 320 × 568. - 375 × 667. - 390 × 844. - 768 × 1024. -
1024 × 768. - 1440 × 900.

Check: - No horizontal overflow. - CTA visibility. - Menu operation. -
Typography and line wrapping. - Accordions. - Form inputs and
validation. - Images/video dimensions. - Footer and legal links.

### 7.5 Accessibility tests

-   Keyboard-only navigation.
-   Screen-reader labels.
-   Heading hierarchy.
-   Contrast.
-   Focus order.
-   Error association.
-   Reduced motion.
-   Alt text.
-   Modal/accordion behaviour.

### 7.6 Security and privacy checks

-   No secrets in client bundles.
-   No personal data in analytics.
-   No client-trusted payment status.
-   No open redirect in login return URLs.
-   No unsafe HTML injection.
-   Server-side validation for application submissions.
-   Existing CSRF/CORS/session protections remain intact.
-   No test data copied into production.

------------------------------------------------------------------------

## 8. Progress tracking

The agent must update this table after each work session. Use
`Not started`, `In progress`, `Blocked`, `Done`, or `Not applicable`.

  -------------------------------------------------------------------------------------------------------------
  Phase                                     Status     Owner      Start date Completion   Evidence / Blockers
                                                                             date         PR /       
                                                                                          commit     
  ----------------------------------------- ---------- ---------- ---------- ------------ ---------- ----------
  0\. Baseline and reconnaissance           Done       AI Agent   2026-11-24 2026-11-24   `docs/audits/initial-audit.md`, `4bfa105`

  1\. Routes and navigation                 Done       AI Agent   2026-11-24 2026-11-24   Redirects, homepage, sitemap, QA

  2\. Canonical course catalogue            Done       AI Agent   2026-11-24 2026-11-24   \courses.config.ts\, \check-catalogue.mjs
  3\. Shared landing-page system            Done       AI Agent   2026-11-24 2026-11-24   \FellowshipTrackTemplate.tsx
  4\. Course content                        Done       AI Agent   2026-11-24 2026-11-24   All 11 tracks unified & upgraded

  5\. Placement/pricing policies            Done       AI Agent   2026-11-24 2026-11-24   \claims-register.md\, \#placement-policy
  6\. Project/mentor/alumni proof           Done       AI Agent   2026-11-24 2026-11-24   Real registry alumni & venture repos

  7\. Application/payment UX                Done       AI Agent   2026-11-24 2026-11-24   Preserved APIs, \/enroll/1999\, LMS flow

  8\. Engagement features                   Done       AI Agent   2026-11-24 2026-11-24   \CoursesCatalogueClient.tsx\ filter/search

  9\.                                       Done       AI Agent   2026-11-24 2026-11-24   JSON-LD, WCAG accordion, \check:seo  SEO/accessibility/performance/analytics                                                            

  10\. Regression and handover              Done       AI Agent   2026-11-24 2026-11-24   \inal-audit.md\, egression-report.md  -------------------------------------------------------------------------------------------------------------

### 8.1 Issue tracker

Maintain `docs/audits/remediation-issues.md`:

  ------------------------------------------------------------------------------------------------
  ID          Priority   Issue         Route/component   Reproduction   Fix      Test     Status
  ----------- ---------- ------------- ----------------- -------------- -------- -------- --------
  DBERT-001   P0         Broken course                                                    Open
                         destination                                                      

  ------------------------------------------------------------------------------------------------

Priority definitions: - **P0:** Broken route, false/misleading claim,
payment/security risk, data loss, application dead end. - **P1:** Major
content, UX, accessibility, or conversion issue. - **P2:** Useful
improvement with a workaround. - **P3:** Cosmetic or low-impact
enhancement.

### 8.2 Session log

Append to `docs/audits/agent-session-log.md` after each session:

``` md
## YYYY-MM-DD — Session N

### Completed
- ...

### Files changed
- ...

### Commands/tests run
- ...

### Results
- ...

### Decisions needed
- ...

### Risks/blockers
- ...

### Next actions
- ...
```

### 8.3 Progress rules

-   Never mark a phase Done without evidence.
-   Record tests that failed before the work as baseline failures.
-   If a phase is blocked by a business decision, mark Blocked and
    continue only with independent safe tasks.
-   Keep the issue tracker and this master plan synchronised.
-   Do not silently skip a task.
-   If scope changes, record the reason and approval in the decision
    log.

------------------------------------------------------------------------

## 9. Decision log

Create `docs/decisions/decision-log.md`:

``` md
# DBERT Fellowship Remediation — Decision Log

## DEC-001 — Canonical nine fellowship tracks
- Date:
- Decision owner:
- Decision:
- Alternatives:
- Reason:
- Affected routes/data:
- Approved by:

## DEC-002 — Placement guarantee definition
- Date:
- Decision owner:
- Decision:
- Eligibility:
- Remedy if not fulfilled:
- Approved by:

## DEC-003 — Fellowship versus comprehensive course
- Date:
- Decision owner:
- Decision:
- Fee/duration/scope:
- Approved by:
```

Add further decisions as required. Do not bury policy decisions in code
comments.

------------------------------------------------------------------------

## 10. Release checklist and rollback

### Pre-release

-   [ ] Product owner approves final course names and catalogue.
-   [ ] Management approves all placement/stipend/fee claims.
-   [ ] All P0 issues closed.
-   [ ] P1 issues closed or explicitly accepted.
-   [ ] Build and tests pass.
-   [ ] All course routes verified.
-   [ ] Application flow verified.
-   [ ] Payment flow verified in the authorised environment.
-   [ ] Analytics events validated.
-   [ ] Mobile and accessibility checks complete.
-   [ ] SEO metadata and redirects checked.
-   [ ] No secrets or personal data committed.
-   [ ] Backup and rollback procedure documented.
-   [ ] Deployment explicitly authorised.

### Rollback plan

The agent must document: - Previous release identifier/commit. -
Deployment method. - How to restore previous frontend assets. - Whether
any backend/API changes were made. - Whether database migrations were
made. - Whether migrations are reversible. - How to disable newly
introduced features via feature flags. - How to verify the previous
release is healthy.

Do not run destructive database migrations as part of a frontend
remediation without explicit approval and a tested rollback.

------------------------------------------------------------------------

## 11. Final handover report template

At completion, produce `docs/audits/final-audit.md`:

``` md
# DBERT Fellowship Landing Pages — Final Remediation Report

## Executive summary
- ...

## Routes repaired
- ...

## Course catalogue
- Approved tracks:
- Canonical routes:
- Legacy redirects:

## UX and content changes
- ...

## Placement/pricing/policy changes
- ...

## Application and payment changes
- ...

## Accessibility, SEO, and performance
- ...

## Backend/database impact
- No change / details:
- Migrations:
- API contract changes:

## Tests
- Build:
- Lint:
- Typecheck:
- Unit/component:
- Route:
- Application:
- Payment:
- Accessibility:
- Responsive:

## Remaining issues
- ...

## Files changed
- ...

## Deployment and rollback
- ...

## Approvals still required
- ...
```

------------------------------------------------------------------------

## 12. Definition of done

The remediation is complete only when:

1.  The approved nine tracks have a consistent catalogue.
2.  Every published track has a working, accurate landing page.
3.  No advertised CTA leads to a broken or unrelated destination.
4.  Course data is centrally managed and consistent.
5.  Each course page clearly explains the practical outcome and
    curriculum.
6.  Proposed projects are not represented as existing production work.
7.  Placement, stipend, salary, and fee claims are documented and
    approved.
8.  The two-month fellowship is clearly distinguished from any other
    course offering.
9.  Application and payment paths work with existing backend rules.
10. Mobile, accessibility, SEO, and performance checks are complete.
11. Tests pass or accepted exceptions are documented.
12. Progress tracking, decision log, issue tracker, and handover report
    are updated.
13. No deployment occurs without explicit authorisation.

------------------------------------------------------------------------

## 13. First instruction to the agent

Start with **Phase 0 only**.

Do not redesign the homepage, rewrite course copy, change URLs, alter
database schemas, or modify payment/application logic yet.

Inspect the local repository and produce:

1.  `docs/audits/initial-audit.md`
2.  `docs/audits/route-inventory.md`
3.  `docs/audits/remediation-issues.md`
4.  `docs/decisions/decision-log.md`
5.  `docs/audits/agent-session-log.md`

Then report: - What framework and backend are present. - Which six
advertised course routes exist and which are broken. - What the actual
nine-track catalogue appears to be. - Where course data is stored. - How
applications and payments currently work. - Which claims require
management confirmation. - Any risks to existing database/backend
functionality.

If a decision is ambiguous, use `/grill-me` before implementing it. Once
Phase 0 is reviewed and approved, proceed sequentially through the
phases, updating this plan and the evidence after every phase.
