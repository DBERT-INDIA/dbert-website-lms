# DBERT India --- Complete Website Audit & Frontend Makeover Master Plan

**Target repository:**
`https://github.com/DBERT-INDIA/dbert-website-lms`\
**Target application:** `apps/website` (Next.js / React)\
**Connected application:** `apps/portal` (Flask LMS)\
**Primary domain:** `https://dbert.in`\
**Document type:** Repository-aware implementation specification for a
local AI coding agent\
**Status:** Planning baseline --- do not start destructive
implementation until Phase 0 gates pass\
**Version:** 1.0\
**Audience:** Frontend engineering agent, product owner, QA agent,
content/SEO agent

------------------------------------------------------------------------

## 0. Executive direction

Redesign DBERT as an **Indian technology education and
career-development institution** with a modern, youthful startup visual
language. The public website serves several audiences, not just
students:

1.  Students and fresh graduates looking for practical courses and
    career direction.
2.  Working professionals and career switchers.
3.  Founders and early-stage startups seeking incubation, product
    engineering and technical support.
4.  Candidates looking for internships and real project experience.
5.  Institutional and ecosystem partners.
6.  Employers or hiring partners evaluating talent and projects.

The public site must explain DBERT's education offering clearly without
hiding its wider startup ecosystem. However, it must not present
unrelated products, internships, courses and incubation as one confusing
purchase.

### 0.1 Confirmed owner decisions

Treat these as the current product-owner decisions unless the owner
changes them:

  -----------------------------------------------------------------------
  Decision                            Approved direction
  ----------------------------------- -----------------------------------
  Primary audience                    Broad: students, graduates,
                                      professionals, founders and
                                      ecosystem users

  Brand                               DBERT --- Indian technology
                                      education institution

  Products to feature                 Courses, Fellowship, Internship,
                                      Incubation

  Geography                           Pan-India, selected cities

  Delivery                            Local institutional / college /
                                      ecosystem partners are part of the
                                      model

  City pages                          SEO and paid campaign conversion

  Programme structure                 Keep Launchpad, Accelerate and
                                      Fellowship as three distinct
                                      products

  Pricing                             Retain current baseline: ₹7,999 /
                                      ₹4,999 / ₹1,999, subject to data
                                      reconciliation

  Career promise                      Outcomes-led: skills, portfolio,
                                      projects, credentials, mentorship
                                      and interview preparation; no
                                      blanket job guarantee

  Public proof                        GitHub, certificates, project demos
                                      and approved partners

  Enrollment                          Lead capture → counselling →
                                      enrollment

  Languages                           English and Hindi

  Visual direction                    Modern Indian startup / technology
                                      education aesthetic

  Scope                               Entire public website and all
                                      landing pages

  Priorities                          Conversion, credibility, SEO and
                                      brand, balanced

  Additional requirements             Build sample homepage and
                                      startup/incubation page; use
                                      suitable open-stock imagery; reuse
                                      existing hand-drawn and engagement
                                      components
  -----------------------------------------------------------------------

### 0.2 Non-negotiable product principles

-   Do not rewrite or replace the LMS backend as part of a frontend
    makeover.
-   Do not change API contracts, database schemas, payment logic,
    authentication, enrollment states or lead-capture semantics without
    explicit approval.
-   Do not invent student counts, placement rates, hiring partners,
    startup grants, incubation outcomes, physical centres, mentors,
    testimonials, accreditations or success metrics.
-   Do not imply that a city has a DBERT office or training centre
    unless a real, approved address and operating model are supplied.
-   Do not imply that a partner relationship is active, contracted or
    endorsed unless it is approved for public display.
-   Do not make a job guarantee. Clearly distinguish training,
    internship selection/assignment, internship completion, placement
    assistance, referral, interview and employment.
-   Do not turn every page into an SEO doorway page. City pages must
    provide useful, truthful local information.
-   Do not sacrifice accessibility, performance, readability or mobile
    usability for animation.
-   Do not use AI-generated fake people, fake screenshots, fabricated
    code reviews or fake testimonials as evidence.
-   The coding agent must preserve existing routes and provide redirects
    for any approved route changes.

------------------------------------------------------------------------

## 1. Repository baseline and inspected implementation

The initial audit inspected the public GitHub repository and key files
in the default branch. The implementation baseline found:

-   Next.js / React public website under `apps/website`.
-   Flask LMS / portal under `apps/portal`.
-   Public homepage: `apps/website/src/app/page.tsx`.
-   Startup page: `apps/website/src/app/startups/page.tsx`.
-   Learner hub: `apps/website/src/app/learners/page.tsx`.
-   Course catalogue: `apps/website/src/app/learners/courses/page.tsx`.
-   Fellowship page:
    `apps/website/src/app/learners/fellowship/page.tsx`.
-   Dynamic city programme template:
    `apps/website/src/components/programs/ProgramCityLanding.tsx`.
-   City/domain registry: `apps/website/src/data/geo_domains.config.ts`.
-   Course data: `apps/website/src/data/courses.core.ts`,
    `courses.specialized.ts`, and `courses.config.ts`.
-   Programme data: `launchpadDomains.ts`, `accelerateDomains.ts`.
-   Pricing: `apps/website/src/config/pricing.config.ts`.
-   Internship city page:
    `apps/website/src/app/internships/[role]/[city]/page.tsx`.
-   Lead form:
    `apps/website/src/components/forms/TrackLeadCaptureForm.tsx`.
-   Navigation: `apps/website/src/components/layout/MegaMenu.tsx`,
    `apps/website/src/data/nav.config.json`.
-   Global design tokens: `apps/website/src/app/globals.css`.
-   Existing visual/engagement components include `HandNote`,
    `HandDrawnArrow`, `Reveal`, `CareerLadder`, `StudioInPractice`,
    `AudienceDoors`, `PrReviewTerminal`, `CountUp`, `ProcessSteps`,
    `ProductCard`, `CaseProof`, `FounderNote`, `FastCalculator`,
    `FAQAccordion`, `StepTimeline`, and analytics-aware `TrackedLink` /
    `trackEvent`.

**Important limitation:** This is a source-code audit and architecture
review, not a completed browser-based test of every deployed route,
every breakpoint, every form submission, every payment callback or every
external integration. The coding agent must run the full runtime audit
before claiming a route or flow is fixed.

### 1.1 Existing strengths to retain

1.  **Reusable Next.js route architecture.** Dynamic routes and shared
    templates can be improved without rewriting the entire app.
2.  **Central programme data.** Course and programme data are already
    separated into configuration modules.
3.  **Central pricing configuration exists.** `pricing.config.ts` is a
    useful source-of-truth starting point, although hardcoded copies
    still exist.
4.  **Lead capture has a real API path.** `TrackLeadCaptureForm` submits
    to `/api/leads/capture`, handles loading, errors and success, and
    produces a lead reference.
5.  **Analytics primitives exist.** `trackEvent`, `TrackedLink` and
    navigation analytics can be reused and normalized.
6.  **Handcrafted design components exist.** Keep selective use of
    `HandNote`, `HandDrawnArrow`, and other hand-crafted elements as
    supporting accents.
7.  **Career progression storytelling exists.** `CareerLadder` can be
    repurposed to explain Launchpad → Accelerate → Fellowship, provided
    eligibility and progression rules are accurate.
8.  **Interactive engagement exists.** `StudioInPractice`,
    `FastCalculator`, FAQ accordions, timelines and project proof
    components can be reused after accessibility and content validation.
9.  **Public evidence assets exist.** The repository contains
    certificate preview images, logos and product images. Audit each
    asset for privacy, authorization, authenticity, image quality and
    relevance before showing it.
10. **Existing SEO foundations exist.** Metadata helpers, canonical URLs
    and structured data should be repaired rather than discarded.

### 1.2 Core weaknesses and risks

  -----------------------------------------------------------------------------
  ID                Finding               Risk                Priority
  ----------------- --------------------- ------------------- -----------------
  AUD-001           Global CSS describes  Too                 High
                    a "Cyber-Industrial   developer-console   
                    Obsidian Studio" with oriented for a      
                    near-black surfaces,  broad Indian        
                    cyan accent and amber education audience  
                    signal                                    

  AUD-002           Homepage metadata     Brand promise and   Critical
                    calls DBERT an "AI    primary audience    
                    Venture Studio" and   conflict            
                    says "Built in                            
                    Delhi", while the                         
                    approved brand                            
                    direction is an                           
                    Indian technology                         
                    education institution                     

  AUD-003           Homepage audience     Product             High
                    doors route founders, architecture is not 
                    enterprise and        sufficiently        
                    learners, but the     explicit            
                    owner-approved public                     
                    product set includes                      
                    courses, fellowship,                      
                    internship and                            
                    incubation                                

  AUD-004           Learner and course    Beginners may not   High
                    pages contain         understand what     
                    technical jargon such they are buying     
                    as production PRs,                        
                    pgvector, vLLM and                        
                    CI/CD before                              
                    explaining learner                        
                    value                                     

  AUD-005           City template         Blank page / silent Critical
                    requires fellowship,  route failure       
                    launchpad and                             
                    accelerate records                        
                    simultaneously; a                         
                    valid tier can return                     
                    `null` if another                         
                    tier's slug is absent                     

  AUD-006           City/domain config    Structured data or  Critical
                    has city-like street  content can imply a 
                    fields pointing to    physical DBERT      
                    technology parks or   office where none   
                    landmarks             exists              

  AUD-007           Internship city page  Search-engine       Critical
                    emits `JobPosting`    misrepresentation   
                    schema with a city    risk if not a       
                    street address and    genuine job vacancy 
                    hardcoded date fields with real location  
                                          and terms           

  AUD-008           City pages are        Doorway-page / thin High
                    largely assembled     localization risk   
                    from shared copy and                      
                    regional inserts                          

  AUD-009           Internship pages and  Contradicts         Critical
                    fellowship pages use  outcomes-led career 
                    "100% Guaranteed      promise; conflates  
                    Production Internship internship and      
                    with Dedicated        placement           
                    Placement Assistance"                     

  AUD-010           Fellowship FAQ says   Internal            Critical
                    no permanent          contradiction and   
                    employment guarantee, consumer-trust risk 
                    but other headlines                       
                    and CTAs use                              
                    "guaranteed                               
                    placement" language                       

  AUD-011           Catalogue and shared  Fees can drift      High
                    city template repeat  between pages       
                    prices and programme                      
                    claims outside the                        
                    pricing source of                         
                    truth                                     

  AUD-012           Lead form exposes     Duration and        Critical
                    "2-Mo Fellowship" and product mismatch    
                    "3-Mo Professional                        
                    Course", while                            
                    current programme                         
                    configuration                             
                    describes two-month                       
                    tiers                                     

  AUD-013           Lead form has both    Funnel is           High
                    application           inconsistent with   
                    submission and direct counselling-first   
                    seat confirmation     owner decision      
                    links                                     

  AUD-014           Internship            Candidates may      Critical
                    recruitment, paid     misunderstand       
                    fellowship enrollment whether they are    
                    and training          applying for a job, 
                    programme enrollment  paying for a course 
                    share messaging and   or applying to a    
                    CTAs                  fellowship          

  AUD-015           Course catalogue      Counts and          High
                    describes 11 tracks,  availability must   
                    while the underlying  be generated from   
                    data is split across  published data, not 
                    core and specialized  hand-maintained     
                    lists and includes    copy                
                    status distinctions                       

  AUD-016           City registry         Route validity,     High
                    contains 18 named     indexing and        
                    city profiles plus    sitemap coverage    
                    `remote`; route       require systematic  
                    families expose       checks              
                    multiple city                             
                    permutations                              

  AUD-017           City course pages     Wrong or            High
                    expose a "three-tier" unavailable tier    
                    comparison and        can be linked       
                    cross-link to all                         
                    tiers regardless of                       
                    the selected                              
                    programme                                 

  AUD-018           Hardcoded "live",     Claims need a fact  Critical
                    "verified", "active   registry and        
                    users", partner,      approval workflow   
                    stipend and outcome                       
                    statements are not                        
                    automatically proof                       

  AUD-019           Startup page contains Legal/financial     Critical
                    high-stakes           promises must be    
                    statements about      verified and        
                    2--8% equity, IP      qualified before    
                    assignment, grants of publication         
                    ₹50,000--₹5,00,000,                       
                    FAST agreements,                          
                    investor networks and                     
                    legal support                             

  AUD-020           Existing engagement   Fake telemetry must High
                    widgets include       not be presented as 
                    decorative or         live system         
                    simulated operational activity            
                    telemetry                                 

  AUD-021           `PrReviewTerminal`    Confirm every       Critical
                    contains a specific   detail is real,     
                    PR number,            authorized and      
                    repository,           reproducible or     
                    contributor, reviewer replace with a      
                    and performance       clearly labelled    
                    figures               illustrative        
                                          example             

  AUD-022           Homepage comments     Reconfirm every     High
                    indicate some figures figure; do not      
                    were founder-approved infer current       
                    as of 2026-07-26 but  status from         
                    treated as            comments            
                    placeholders for                          
                    local edits                               

  AUD-023           Existing city lead    Privacy notice,     High
                    form has fields for   purpose, consent,   
                    personal details,     retention and       
                    college, city and     access controls     
                    graduation year       need review         

  AUD-024           Hindi is approved,    Add proper          High
                    but no language       localization, not a 
                    architecture or       superficial         
                    translation QA was    language toggle     
                    established in the                        
                    inspected files                           

  AUD-025           Existing UI uses many Redesign must avoid Medium
                    specialized           one-off visual      
                    components and CSS    systems and         
                    modules               duplicated          
                                          components          

  AUD-026           Open-stock            Attribution,        Medium
                    photography is        source, license,    
                    requested, but no     download date and   
                    asset licensing       optimized local     
                    manifest exists       asset storage       
                                          required            
  -----------------------------------------------------------------------------

------------------------------------------------------------------------

## 2. Product strategy and information architecture

### 2.1 DBERT's public positioning

Recommended primary statement:

> **Learn by building. Grow by shipping. Build what comes next.**\
> DBERT helps learners develop practical technology skills, work on
> meaningful projects, explore internship pathways and connect with
> India's startup ecosystem.

Supporting description:

> DBERT is an Indian technology education and venture ecosystem
> connecting learners, mentors, institutions, founders and product teams
> through practical learning, project work and startup collaboration.

Avoid claims that imply DBERT is a university, government institution,
accredited college, staffing agency, guaranteed placement provider or
investor unless those exact statuses are verified and legally approved.

### 2.2 Product boundaries

The public site must keep the following products distinct:

  -------------------------------------------------------------------------------
  Product           What it is                What it is not    Primary CTA
  ----------------- ------------------------- ----------------- -----------------
  Courses           Structured learning in a  Not automatically Explore course /
                    selected technical domain an internship or  Request
                                              job               counselling

  Launchpad         Beginner foundation       Not a guaranteed  Get roadmap
                    programme                 job track         

  Accelerate        Applied intermediate      Not a job         Discuss
                    programme                 placement         eligibility
                                              contract          

  Fellowship        Selective, practical      Not unconditional Apply / Request
                    project/fellowship        employment        counselling
                    experience with clear                       
                    terms                                       

  Internship        Recruitment/application   Not a paid course View openings /
                    route for available       disguised as a    Apply
                    internship roles          job               

  Incubation        Startup support /         Not a guaranteed  Submit startup
                    venture-building          grant or          application
                    engagement                investment        

  Partner ecosystem Colleges, mentors,        Not a fabricated  Become a partner
                    companies and delivery    list of logos     
                    collaborators                               
  -------------------------------------------------------------------------------

### 2.3 Recommended navigation

Desktop navigation:

-   **Explore Learning**
    -   All Courses
    -   Launchpad
    -   Accelerate
    -   Fellowship
    -   Learning Paths
-   **Internships**
    -   Available Opportunities
    -   Internship Domains
    -   How Selection Works
    -   Candidate FAQs
-   **For Founders**
    -   Startup Incubation
    -   Product Engineering
    -   Technical Support
    -   Apply for Incubation
-   **For Institutions**
    -   College Partnerships
    -   Campus Programmes
    -   Partner Enquiry
-   **About DBERT**
    -   Our Approach
    -   Projects & Ventures
    -   Mentors / Team
    -   Credentials & Verification
    -   Contact
-   Primary CTA: **Talk to an Advisor**
-   Secondary utility: **LMS Login**

Mobile navigation must expose the same destinations without requiring
hover.

### 2.4 Audience entry

Homepage must offer four clear entry doors:

1.  **I want to learn** --- courses, programmes, curriculum, fees.
2.  **I want an internship** --- genuine roles, eligibility, selection,
    stipend terms if applicable.
3.  **I am building a startup** --- incubation and product engineering.
4.  **I represent a college / institution** --- partnership and campus
    engagement.

Do not force enterprise AI product buyers into the same path as
students. If AI SaaS products remain part of the broader business, link
to a separate product/solutions hub and preserve it in navigation or
footer as a distinct audience route.

### 2.5 Funnel design

Approved primary funnel:

`Discovery → Product detail → Lead / counselling request → Human counselling → Eligibility / fit → Offer and terms → Payment (if applicable) → Enrollment confirmation → LMS onboarding`

Separate internship funnel:

`Opportunity detail → Eligibility → Application → Screening → Selection / rejection → Offer terms → Onboarding`

Separate incubation funnel:

`Founder landing page → Startup application → Technical review → Human discussion → Written proposal / term sheet → Contract → Kickoff`

Never mix the three funnels.

------------------------------------------------------------------------

## 3. Design system --- modern Indian startup education

### 3.1 Visual principles

-   Bright, energetic, clean and credible.
-   Modern Indian startup character without excessive flag colours or
    stereotypical cultural decoration.
-   Real people and real work, not stock-photo wallpaper.
-   Strong typography and clear reading hierarchy.
-   Warm neutrals with navy/indigo and controlled saffron accents.
-   Handcrafted details should add personality, not make the page look
    childish.
-   Technical details should appear as proof after the user understands
    the benefit.
-   Use whitespace, strong cards, editorial layouts, real screenshots
    and useful interactive components.

### 3.2 Proposed tokens

Use CSS custom properties in one central theme file. The values below
are the initial design direction; validate contrast before finalizing.

``` css
:root {
  --color-canvas: #F7F7F2;
  --color-surface: #FFFFFF;
  --color-surface-soft: #EEF2F6;
  --color-ink: #17243A;
  --color-ink-muted: #536174;
  --color-border: #DDE3EA;

  --color-primary: #193B68;
  --color-primary-hover: #102D52;
  --color-accent: #F2A33A;
  --color-accent-soft: #FFF1D9;
  --color-success: #23734D;
  --color-danger: #B42318;
  --color-info: #2463A6;

  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 22px;
  --radius-xl: 30px;

  --shadow-card: 0 8px 28px rgba(23, 36, 58, 0.07);
  --shadow-hover: 0 16px 38px rgba(23, 36, 58, 0.12);

  --content-width: 1200px;
  --reading-width: 760px;
}
```

### 3.3 Typography

Use a restrained type system:

-   Display: modern geometric sans, e.g. Bricolage Grotesque or an
    approved locally hosted equivalent.
-   Body: Inter / system sans.
-   Hindi: a Devanagari-compatible font such as Noto Sans Devanagari.
-   Code: JetBrains Mono only for code samples, not ordinary body copy.
-   Do not use monospace labels for every section heading.
-   Keep paragraph line length around 55--80 characters.
-   Avoid all-caps micro-labels as the dominant hierarchy.

Load fonts through `next/font` where possible. Verify Hindi glyph
rendering, font subsets, layout shifts and fallback behaviour.

### 3.4 Components and states

Create a consistent component library:

-   `SiteHeader`
-   `DesktopNavigation`
-   `MobileNavigation`
-   `SiteFooter`
-   `AudienceEntryCards`
-   `HeroSection`
-   `SectionHeading`
-   `CourseCard`
-   `ProgrammeComparison`
-   `ProgrammeOutcomeList`
-   `CurriculumAccordion`
-   `ProjectShowcase`
-   `ProofCard`
-   `PartnerLogoWall` (only approved partners)
-   `MentorCard` (only verified profiles)
-   `TestimonialCard` (only consented real testimonials)
-   `CityContextPanel`
-   `CounsellingForm`
-   `ApplicationStatusPanel`
-   `PricingPanel`
-   `FAQAccordion`
-   `Breadcrumbs`
-   `LanguageSwitcher`
-   `StickyMobileCTA`
-   `ConsentNotice`
-   `EmptyState`
-   `ErrorState`
-   `LoadingState`

Every interactive component must have hover, focus-visible, active,
disabled, loading, success and error states as applicable.

### 3.5 Handcrafted elements

Reuse existing: - `HandNote` - `HandDrawnArrow` - `Reveal`

Use these only as small accents around key content. Keep decorative SVGs
hidden from screen readers. Do not let handwritten text contain
information that is absent from accessible semantic copy.

Reuse `Reveal` with reduced-motion support. Ensure no content remains
invisible if JavaScript or IntersectionObserver fails.

### 3.6 Engagement features to retain or improve

-   `StudioInPractice`: use as an interactive "How DBERT connects
    learning, projects and startups" explainer.
-   `CareerLadder`: use for Launchpad → Accelerate → Fellowship, but
    state that progression and selection are conditional, not automatic.
-   `FastCalculator`: only keep if it calculates a real, transparent
    value; otherwise remove.
-   `FAQAccordion`: keyboard accessible, proper button semantics and
    `aria-expanded`.
-   `StepTimeline`: use for counselling, application and programme
    journeys.
-   `PrReviewTerminal`: only show verified, consented, real PR evidence;
    otherwise show a labelled "Illustrative example" with fictional
    names and no fabricated production metrics.
-   `CountUp`: animate only real, dated metrics and show the same value
    without animation for assistive technology.
-   `AudienceDoors`: expand from three doors to four approved audiences.
-   `TrackedLink`: keep analytics but never block navigation if
    analytics fails.

------------------------------------------------------------------------

## 4. Homepage sample --- page structure and approved draft copy

### 4.1 Route and goal

Route: `/`\
Goal: make the DBERT proposition understandable within five seconds,
route each audience to the right section, and generate qualified
counselling / partnership enquiries.

### 4.2 Desktop wireframe

1.  Header: logo, Explore Learning, Internships, For Founders, For
    Institutions, About, language selector, Talk to an Advisor.
2.  Hero: left-side message and CTA; right-side authentic image /
    collage showing Indian learners building a real project.
3.  Trust strip: only approved proof types --- GitHub work, verifiable
    certificates, project demos, named institutional partners.
4.  Four audience cards.
5.  "Learn by building" programme ladder.
6.  Project proof gallery.
7.  How DBERT works --- learning, practice, mentor review, portfolio.
8.  City / partner ecosystem section.
9.  Founder / incubation preview.
10. Learner stories / outcome evidence.
11. FAQs.
12. Final counselling CTA and full footer.

### 4.3 Sample homepage copy

**Eyebrow:** PRACTICAL TECHNOLOGY LEARNING · BUILT IN INDIA

**H1:** Learn technology by building things that matter.

**Subheading:** Build practical skills, work through real projects, get
feedback from experienced practitioners and discover your next
opportunity with DBERT.

**Primary CTA:** Explore learning programmes\
**Secondary CTA:** Talk to an advisor

**Small trust statement:** Explore public projects, credential
verification and approved ecosystem partners before you apply.

**Audience section heading:** What brings you to DBERT?

Card 1 --- **I want to learn**\
Choose a technical domain, understand the curriculum and find a
programme that matches your current skill level.\
CTA: Explore courses

Card 2 --- **I am looking for an internship**\
Explore available roles, selection requirements, expected work and
programme terms.\
CTA: View opportunities

Card 3 --- **I am building a startup**\
Get technical guidance, product engineering support and a clear view of
DBERT's incubation model.\
CTA: Explore incubation

Card 4 --- **I represent an institution**\
Explore campus learning programmes, project collaborations and
partnership possibilities.\
CTA: Partner with DBERT

**Section heading:** A learning path for where you are now

Launchpad --- Start with the foundations\
For beginners who need structure, practical exercises and a guided first
portfolio project.\
Fee: ₹7,999 · 2 months (confirm exact inclusions and cohort dates)\
CTA: Explore Launchpad

Accelerate --- Turn knowledge into applied skills\
For learners ready to build domain-specific systems and complete more
challenging projects.\
Fee: ₹4,999 · 2 months (confirm exact inclusions and cohort dates)\
CTA: Explore Accelerate

Fellowship --- Learn through reviewed project work\
For candidates who meet the programme's eligibility and selection
criteria. Understand the actual work, mentor review, evaluation and
credential terms before applying.\
Fee: ₹1,999 · 2 months (confirm exact inclusions and whether fee applies
to all candidate types)\
CTA: Understand Fellowship

**Section heading:** See the work, not just the promise

Show 3--6 project cards. Each must include: - Project name. - Problem
being solved. - What DBERT / learner contributed. - Technology used,
explained in plain language. - Demo or repository link. - Project status
and last updated date. - Whether it is a DBERT internal project, partner
project or learner capstone. - Permission / attribution confirmation.

**Section heading:** From learning to opportunity

Explain the journey without suggesting guaranteed employment: 1. Learn
the foundations. 2. Build guided projects. 3. Get feedback and improve.
4. Publish a portfolio. 5. Apply for suitable internships or
opportunities. 6. Prepare for interviews and demonstrate your work.

**Final CTA:** Not sure which programme fits?\
Tell us what you want to learn and where you are starting from. A DBERT
advisor can help you understand the options, requirements and fees.\
CTA: Request a counselling call

### 4.4 Homepage interaction requirements

-   Audience cards are clickable with a clear hover/focus state.
-   Programme cards have "Compare programmes" anchor.
-   Project gallery filters by domain only if filter data is real.
-   Counselling form opens as an accessible dialog or a dedicated page;
    do not create a tiny modal with too many fields.
-   Language switcher changes actual page copy and preserves route
    context when translation exists.
-   Mobile sticky CTA must not cover form fields, cookie notices or
    navigation.
-   Do not autoplay carousels or background video.
-   Use a static poster if video is used; lazy-load the video.

------------------------------------------------------------------------

## 5. Startup / incubation sample page

### 5.1 Route and goal

Route: `/startups`\
Audience: early-stage founders, technical founders, product owners and
startup teams.\
Goal: explain DBERT's incubation and technical support model, qualify
founders, and generate serious applications.

### 5.2 Critical claims gate

The current startup page contains claims about: - 2--8% equity. - IP
ownership and assignment. - FAST agreements and common stock. -
Non-dilutive infrastructure grants of ₹50,000--₹5,00,000. - Investor
network introductions. - MCA / UDYAM / Startup India legal support. -
MVP delivery in 4--8 weeks.

These are not to be repeated automatically. The owner must verify the
exact legal entity, availability, contractual structure, partner
authorization, funding source, eligibility and limitations. Do not
describe introductions as investment commitments. Do not describe a
grant as guaranteed. Do not publish legal advice unless a qualified
professional has approved the service and copy.

### 5.3 Startup page wireframe

1.  Header.
2.  Hero with a founder/product image or authentic team-at-work image.
3.  Short model explanation: engineering, product execution and
    ecosystem support.
4.  Three engagement tracks:
    -   Product engineering / technical co-development.
    -   Founder support / incubation.
    -   Talent and project collaboration.
5.  What DBERT can help build: MVP, AI workflow, SaaS platform, data
    product, internal automation.
6.  How engagement works: discovery → technical review → scope → written
    proposal → agreement → delivery.
7.  Selected project case studies with real repositories/demos.
8.  Engagement model explanation with exact caveats.
9.  Partner / ecosystem proof.
10. Founder application form.
11. FAQ and contact.
12. Footer.

### 5.4 Sample startup page copy

**Eyebrow:** FOR INDIAN FOUNDERS · PRODUCT & ENGINEERING SUPPORT

**H1:** Turn a promising idea into a product people can use.

**Subheading:** DBERT works with selected founders and early-stage teams
on product planning, software engineering and practical AI
implementation. Start with a clear technical conversation --- not a
vague promise.

**Primary CTA:** Discuss your startup\
**Secondary CTA:** See projects and capabilities

**Section:** What stage are you at?

-   **Idea to first prototype:** validate the problem, define a focused
    MVP and identify the smallest useful build.
-   **Prototype to usable product:** improve architecture, build core
    workflows, integrate data and prepare for early users.
-   **Product to reliable operations:** strengthen security, testing,
    deployment, observability and maintainability.

**Section:** Ways we may work together

1.  **Technical discovery** --- review your problem, product scope,
    architecture and constraints.
2.  **Product engineering** --- define and build agreed features with
    documented milestones.
3.  **Incubation / co-development** --- for selected ventures, explore a
    written engagement structure with responsibilities, ownership and
    commercial terms.
4.  **Talent collaboration** --- where appropriate, discuss supervised
    project work or candidate introductions with clear IP,
    confidentiality and employment terms.

**Section:** A transparent process

1.  Submit a short founder brief.
2.  DBERT reviews the problem, stage and technical fit.
3.  Arrange a discovery discussion if there is a fit.
4.  Receive a written scope, delivery plan, responsibilities,
    fees/equity terms if applicable and legal documents.
5.  Begin only after both parties approve the written agreement.

**Section:** What to prepare

-   A short description of the problem.
-   Target customer and user.
-   Current product status.
-   Existing prototype / repository / demo, if any.
-   What support you need.
-   Timeline and constraints.
-   Contact details.

**CTA:** Tell us what you're building.

### 5.5 Startup application fields

Minimum first step: - Name. - Work email. - Phone / WhatsApp (optional
if email is sufficient). - Startup / project name. - Website or demo URL
(optional). - Stage: idea / prototype / early users / revenue /
scaling. - Support needed: product engineering / AI implementation /
technical review / incubation / other. - Short problem statement. -
Consent checkbox and privacy notice.

Do not ask for pitch deck, cap table, financial statements, sensitive IP
or confidential code in the initial public form. Collect sensitive
documents only through an approved secure process after an initial fit
assessment.

------------------------------------------------------------------------

## 6. Programme pages and course catalogue

### 6.1 Catalogue

Route: `/learners/courses`

Required: - Search by course name and plain-language goal. - Filter by
domain, skill level, duration, format and availability only where data
exists. - Show total price clearly. - Show prerequisites. - Show what
learner will build. - Show weekly commitment. - Show language / support
mode. - Show next cohort only if backed by live schedule data. - Show
"Request counselling" as the primary CTA. - Compare up to three
programmes. - Never label a programme "live" unless cohort and delivery
are actually active.

### 6.2 Course detail page

Every course page must use a common layout: 1. Course title and learner
outcome. 2. Who it is for / not for. 3. Prerequisites. 4. What you will
learn in plain English. 5. Week-by-week curriculum. 6. Projects and
deliverables. 7. Tools and technologies. 8. Assessment and feedback. 9.
Mentor / support model. 10. Time commitment and schedule. 11. Format and
partner delivery details. 12. Fee and what it includes. 13. Certificate
details and verification terms. 14. Next steps and counselling. 15.
FAQs.

### 6.3 Three programme tiers

**Launchpad --- ₹7,999 / 2 months**\
Position as beginner foundation programme. Explicitly state whether it
is suitable for a complete beginner and what prerequisite setup is
needed.

**Accelerate --- ₹4,999 / 2 months**\
Position as intermediate, applied programme. Explain expected coding
knowledge and what makes it different from Launchpad.

**Fellowship --- ₹1,999 / 2 months**\
Position as a selective, practical experience / reviewed project-work
programme, only if the underlying delivery model and candidate
eligibility support that description. Explain selection, workload,
project assignment, supervision, stipend eligibility if any, credential
rules and any fee. Do not imply the fee buys a job or guaranteed
placement.

**Important pricing reconciliation:** The prices are not logically
self-explanatory because the more advanced Fellowship is currently
listed at a lower fee than Launchpad and Accelerate. Preserve the
owner's current fee decision, but the agent must surface this as a
`grill-me` question: is the fellowship fee a subsidized cohort fee,
application fee, programme fee, refundable deposit, or a different
product? Never invent the explanation.

### 6.4 Remove conflicting copy

Search all frontend source and content for: - "100% Guaranteed" -
"Guaranteed Placement" - "Guaranteed Production Internship" -
"guaranteed job" - "3-Mo Professional Course" - "12--15 hours" vs other
time commitments - "3-document credential packet" - "₹5,000+ stipend" -
"Round-1 screening waiver" - "MSME-accredited" - "Turnitin-verified" -
"live client" - "active users" - "verified partner" - "seed grant" -
"investor network" - "2--8% equity"

For every result, determine whether the statement is current, accurate,
evidenced, legally approved and consistent with owner-approved product
terms. Do not perform a blind global replacement; each claim requires
context.

------------------------------------------------------------------------

## 7. City landing pages and local partner strategy

### 7.1 Approved city strategy

City pages support both SEO and paid campaigns. Delivery includes
institutional / local partners, but the exact partner footprint must be
verified city by city.

The page must distinguish: - DBERT-operated physical centre. - Approved
partner institution. - Local event / workshop location. - Remote
programme available to residents of the city. - Hiring market context
only (not an office or job vacancy).

Do not use a technology park street address as a DBERT business address.

### 7.2 City page required structure

1.  City-specific H1 and intro.
2.  Truthful delivery statement.
3.  Approved partner card(s), if any.
4.  Local learner context, written uniquely and helpfully.
5.  Programme options available to that city.
6.  City-specific events / workshops, if scheduled.
7.  Local alumni / project stories, only if verified and consented.
8.  Curriculum and fees.
9.  Counselling CTA with city prefilled.
10. City FAQs.
11. Nearby cities only where useful and not an SEO link farm.

### 7.3 City data model

Replace ambiguous `street` with explicit fields:

``` ts
type CityDeliveryMode =
  | "remote"
  | "partner_campus"
  | "db ert_centre"
  | "hybrid_event";

interface CityProfile {
  slug: string;
  name: string;
  state: string;
  country: "India";
  deliveryMode: CityDeliveryMode;
  partnerIds: string[];
  publicAddress?: string; // only for approved physical venue
  localIntro: string;
  localFaqs: Array<{ question: string; answer: string }>;
  localEvents?: Array<{ title: string; date: string; venue?: string; url?: string }>;
  seoIndexable: boolean;
  lastReviewedAt: string;
}
```

Correct the illustrative typo `db ert_centre` to `dbert_centre` in the
real implementation. The schema above is conceptual and must be
normalized by the agent.

A partner record should contain: - Legal / public name. - Partner
type. - City. - Approved logo. - Approved website. - Relationship
status. - Public display permission. - Start / end date if relevant. -
Exact activity DBERT is authorized to claim. - Last reviewed date.

### 7.4 SEO indexation policy

-   Index only city pages with useful unique local content and a real
    offer.
-   `noindex` pages with no meaningful local differentiation or no
    available programme.
-   Canonical URL must be self-referential for genuine unique pages.
-   Do not generate hundreds of near-identical permutations.
-   Use valid `Course` schema only for actual courses.
-   Use `LocalBusiness` only for a real, staffed and public physical
    location.
-   Use `JobPosting` only for a genuine current job opening with a real
    role, employment type, location/remote policy, compensation
    disclosure where required, posting date and valid-through date.
-   Do not use `JobPosting` schema for a paid course, fellowship
    marketing page or general internship category page.
-   Do not use `Event` schema for unscheduled or hypothetical workshops.
-   Do not create FAQ structured data that is absent from the visible
    page.
-   Add `BreadcrumbList` only where breadcrumbs are visible and correct.

### 7.5 Paid campaign pages

Campaign pages may use a more focused layout but must: - Preserve the
same factual claims and pricing. - Carry UTM parameters. - Explain
remote / partner delivery. - Include a concise privacy notice. - Use one
clear CTA. - Avoid indexing thin paid variants unless they provide
standalone organic value.

------------------------------------------------------------------------

## 8. Internship pages and recruitment separation

Internship pages must look and behave like recruitment pages, not course
sales pages.

Required fields for a real role: - Role title. - Department / domain. -
Responsibilities. - Required skills. - Eligibility. - Location / remote
policy. - Weekly time commitment. - Duration. - Stipend range or unpaid
status, where legally appropriate and confirmed. - Supervisor /
reporting structure. - Selection stages. - Application deadline. - Start
date. - Number of openings only if live and verified. - Employment /
internship status and terms. - Privacy notice.

Primary CTA: Apply for this opportunity.\
Secondary CTA: Understand the selection process.

Do not send an applicant to `/enroll/1999` from a job opening unless the
relationship is clearly explained and legally approved. A job applicant
must not believe that payment is required to be considered for
employment.

Remove or repair `JobPosting` schema if a page is not a genuine role.
Use `EducationalOccupationalProgram` or `Course` only if the page
genuinely represents a learning programme and the schema is appropriate.

------------------------------------------------------------------------

## 9. Incubation and partner pages

### 9.1 Incubation

Build a clear startup landing page as described in Section 5. Create a
separate application process from student lead capture.

### 9.2 Institutional partnership page

Add `/partners` or an equivalent route after confirming route
availability. It should explain: - What DBERT offers to colleges /
institutions. - What DBERT expects from the partner. - Delivery formats:
campus workshop, cohort programme, remote mentorship, project showcase,
hiring event (only if available). - Faculty / coordinator
responsibilities. - Student eligibility and fees. - Data sharing and
consent. - Partner branding rules. - How to initiate a discussion.

Do not show logos without permission. Use "Partner with DBERT" rather
than "Our partners" if the relationship is only a prospective target.

### 9.3 Partnership enquiry form

-   Institution name.
-   Contact person and role.
-   Official email.
-   City / state.
-   Approximate student cohort size (optional).
-   Interested collaboration type.
-   Message.
-   Consent and privacy notice.

------------------------------------------------------------------------

## 10. Hindi and English localization

Implement true locale support. Preferred URL pattern should be selected
after checking existing route structure and SEO configuration: -
`/en/...` and `/hi/...`, or - locale subdomain / Next.js locale routing
if already supported.

Requirements: - English default if that matches current canonical URL
strategy. - Hindi translations must be reviewed by a fluent human,
especially legal, pricing and career outcome statements. - Keep product
names such as Launchpad / Accelerate / Fellowship consistent, with a
short Hindi explanation. - Preserve query parameters and campaign
attribution during language switching. - `hreflang` and canonical tags
must be correct. - Do not machine-translate dynamic data blindly. - If a
page is not translated, do not show a fake Hindi toggle; clearly
indicate language availability. - Hindi typography and layout must be
tested on small Android screens.

------------------------------------------------------------------------

## 11. Images, illustration and stock assets

### 11.1 Image direction

Use authentic Indian education / startup imagery: - Indian college
learners working in groups. - A student building or presenting a
software project. - Mentors reviewing a project. - Founders discussing a
product prototype. - A campus / workshop setting only if it represents
the real delivery model. - Real project screenshots, certificate
examples and product UI where approved.

Avoid: - Generic graduation-cap hero images. - Fake office spaces. -
Unrelated foreign university stock photos. - Artificial AI robots /
glowing brains. - Images that imply a physical DBERT centre where none
exists. - Fake team photos or fabricated testimonials.

### 11.2 Open-stock sourcing

Preferred sources: Unsplash, Pexels and Pixabay, subject to current
license and attribution requirements. Do not assume every asset on a
platform has identical licensing.

For each downloaded asset, maintain
`apps/website/public/media/ASSET_MANIFEST.md` containing: - Local
filename. - Original source URL. - Creator / photographer. - License /
usage terms checked. - Download date. - Intended route. - Crop / focal
point. - Whether model/property release is relevant. - Alt text. -
Approval status.

Use Next.js Image, responsive sizes, AVIF/WebP where supported, explicit
width/height, lazy loading below the fold, and a meaningful poster for
any video. Do not hotlink stock images in production.

### 11.3 Existing assets

Inventory existing public assets before downloading new images: -
`apps/website/public/logo.svg` - `apps/website/public/og-image.jpg` -
product and venture images such as `alkame.png`, `gayatri-ai.png`,
`digital-blaize.png` - certificate preview assets under
`public/certificates/previews/` - existing founder / profile images.

Verify ownership, consent, current branding, resolution and actual
product relevance. Certificate previews may expose personal information;
do not publish a sample without checking for redaction and permission.

------------------------------------------------------------------------

## 12. Accessibility, responsive UX and performance

### 12.1 Accessibility acceptance

Target WCAG 2.2 AA: - Semantic landmarks and correct heading
hierarchy. - Keyboard-operable navigation, menus, accordions, tabs and
dialogs. - Visible focus indicators. - Contrast at least WCAG AA. - Form
labels, instructions and inline errors. - Error summary for long
forms. - Screen-reader status for submission and loading. - Decorative
images have empty alt; meaningful images have descriptive alt. - No
meaning conveyed by colour alone. - Reduced motion support. - Minimum
44px touch targets where feasible. - No keyboard traps. - No hover-only
content. - Language tags on Hindi and English content. - Dialog focus
management and escape-to-close.

### 12.2 Responsive breakpoints

Use the existing design breakpoints only after verifying actual
layout: - Small: 360--479px - Mobile: 480--767px - Tablet: 768--1023px -
Desktop: 1024--1439px - Wide: 1440px+

Test at 360px, 390px, 430px, 768px, 1024px, 1280px and 1440px. Check
horizontal overflow, sticky CTA overlap, long Hindi strings, cards,
tables, navigation and forms.

### 12.3 Performance

Targets (field data and lab data should both be reviewed): - LCP ≤
2.5s - INP ≤ 200ms - CLS ≤ 0.1 - Avoid large JS bundles for static
marketing pages. - Server-render static content wherever possible. - Use
client components only where interaction requires them. - Lazy-load
below-fold galleries and heavy embeds. - Avoid large animation libraries
for small effects. - Do not autoplay background video on mobile. - Use
optimized local fonts and images. - Keep analytics non-blocking and
consent-aware where required.

------------------------------------------------------------------------

## 13. Forms, privacy and analytics

### 13.1 Counselling form

Recommended first step: - Name. - Email. - WhatsApp / phone. - I am
interested in: course / Launchpad / Accelerate / Fellowship / internship
/ incubation / partnership. - City. - Current stage: student / graduate
/ working / founder / institution. - Preferred contact mode / time
(optional). - Consent to be contacted. - Link to privacy notice.

Ask graduation year, college, skill level or portfolio only if needed
for that product. Do not force a large questionnaire for a generic
counselling request.

### 13.2 Form behaviour

-   Preserve current API contract until inspected and approved.
-   Validate on client and server.
-   Use idempotency or duplicate handling where supported.
-   Prevent double submissions.
-   Keep user inputs on recoverable network failure.
-   Show human-readable errors.
-   Show a reference ID after successful submission.
-   Provide next steps and expected response window only if
    operationally true.
-   Do not expose PII in URLs, analytics events or WhatsApp deep links
    unnecessarily.
-   Add spam protection and rate limits.
-   Confirm consent and privacy language with the owner/legal reviewer.

### 13.3 Analytics event plan

Normalize event names: - `nav_click` - `audience_route_select` -
`course_view` - `programme_compare` - `city_page_view` -
`counselling_form_start` - `counselling_form_submit` -
`counselling_form_success` - `counselling_form_error` -
`internship_apply_click` - `startup_application_start` -
`startup_application_submit` - `language_switch` -
`project_demo_click` - `certificate_verify_click` - `lms_login_click`

Properties should be non-sensitive: - page route - product category -
programme slug - city slug - language - CTA location - UTM
campaign/source/medium

Never send name, email, phone, CV content, application narrative or
confidential startup information to analytics.

------------------------------------------------------------------------

## 14. SEO and content governance

### 14.1 Metadata

Every indexable route requires: - Unique title. - Unique description. -
Canonical URL. - Open Graph title / description / image. - Twitter
metadata where required. - Correct robots directives. - Breadcrumbs if
visible. - Valid structured data only where appropriate.

### 14.2 Internal linking

-   Homepage → four audience routes.
-   Learner hub → catalogue and three programme pages.
-   Course detail → related courses, programme comparison and
    counselling.
-   City page → relevant course and local partner information.
-   Internship hub → genuine available roles.
-   Startup page → application and case studies.
-   Partner page → partnership enquiry.
-   About page → real people, projects, credentials and contact.
-   Footer → all critical legal, privacy, support and verification
    routes.

Do not create cross-city link blocks purely to manipulate crawl paths.
Nearby-city links should be useful to the reader.

### 14.3 Content fact registry

Create a structured file such as
`apps/website/src/data/claims.registry.ts` or JSON with: - Claim ID. -
Exact approved text. - Category. - Evidence URL / internal reference. -
Owner. - Approval date. - Expiry / review date. - Routes where it may
appear. - Whether the claim may be used in structured data. - Required
disclaimer.

Examples: fees, duration, hours/week, cohort dates, stipend, internship
status, partner relationships, credential issuer, government
registrations, placement outcomes, number of graduates, project status,
incubation equity terms and grant availability.

Any claim without an evidence record should be hidden or phrased as a
non-claim pending owner approval.

------------------------------------------------------------------------

## 15. Technical implementation contract

### 15.1 Architecture rules

-   Keep the current Next.js App Router unless the repository proves a
    compelling reason to change it.
-   Preserve server components by default.
-   Client components only for actual stateful interactions.
-   Do not create a parallel website app.
-   Do not rewrite `apps/portal`.
-   Do not duplicate course and pricing data.
-   Use typed data models and schema validation.
-   Add route-level `notFound()` handling for invalid slugs.
-   Never return `null` for an invalid page in a way that silently
    produces a blank page.
-   Keep API routes compatible with existing backend contracts.
-   Preserve current authentication and LMS destination URLs unless
    approved.
-   Do not expose secret environment variables to the browser.
-   Use the repo's existing lint, typecheck, test and build scripts.

### 15.2 Specific fix: tier-specific city validation

Current `ProgramCityLanding.tsx` resolves all three programme objects
and returns `null` if any one is missing. Fix this by validating only
the selected tier:

``` ts
const cityData = GEO_CITIES[city];
if (!cityData) notFound();

let selectedProgram;

if (tier === "launchpad") {
  selectedProgram = LAUNCHPAD_DOMAINS[slug];
} else if (tier === "accelerate") {
  selectedProgram = ACCELERATE_DOMAINS[slug];
} else {
  selectedProgram = getTrackBySlug(slug);
}

if (!selectedProgram) notFound();
```

Adapt to the actual component / route shape; do not paste this blindly
if `notFound()` cannot be called in the current component. Prefer
route-level validation and pass a typed valid model into the component.

### 15.3 Pricing source of truth

Use `pricing.config.ts` or a new validated pricing model as the single
source. Remove hardcoded price literals from page components and FAQs.
All displayed fees, balance amounts and programme durations must derive
from the same typed configuration.

Do not change the actual amounts until approved. Add a test that fails
if the same programme has conflicting fees or duration labels across
routes.

### 15.4 Route migration

Before changing routes: - Export current route inventory. - Record
status codes and canonical URLs. - Record indexed URL set and sitemap. -
Add redirects for changed URLs. - Keep query strings and UTM parameters
where appropriate. - Check LMS callback and login URLs. - Check external
QR / payment / verification links. - Verify no CTA points to a removed
or stale destination.

------------------------------------------------------------------------

## 16. Phase-by-phase implementation plan

The coding agent must execute phases sequentially. Do not skip gates.
Update the progress tracker after each task and before stopping.

### Phase 0 --- Discovery, backup and safety baseline

**Goal:** Establish what exists and protect business-critical behaviour.

Tasks: - \[ \] Identify default branch and latest commit SHA. - \[ \]
Create a dedicated branch: `feat/indian-education-website-redesign`. -
\[ \] Confirm local working tree is clean. - \[ \] Record Node / package
manager / Next.js versions. - \[ \] Read root README and app README
files. - \[ \] Read all website routes and nav config. - \[ \] Export
full route inventory. - \[ \] Export current sitemap and metadata. - \[
\] Identify API routes and backend dependencies. - \[ \] Identify form
endpoints and request/response contracts. - \[ \] Identify payment, LMS,
auth and verification links. - \[ \] Run existing lint, typecheck, unit
tests and production build. - \[ \] Capture screenshots of homepage,
startup, learner hub, catalogue, course detail, city page, internship
page, about, contact and mobile navigation. - \[ \] Inventory all assets
and licenses. - \[ \] Create `docs/redesign/BASELINE_AUDIT.md`.

**Gate 0:** No destructive code changes until the baseline build and
core user journeys are documented. If build is already failing, record
baseline failures separately.

### Phase 1 --- Business truth and claim audit

**Goal:** Resolve factual contradictions before designing the UI.

Tasks: - \[ \] Create claims inventory for all routes. - \[ \] Find
every placement / job / internship guarantee phrase. - \[ \] Find every
stipend, fee, deposit and certification fee. - \[ \] Find every duration
and weekly commitment. - \[ \] Find all partner and institution
names/logos. - \[ \] Find all city address and local presence
statements. - \[ \] Find all startup equity, IP, grant, legal and
investor claims. - \[ \] Find all numeric metrics and testimonials. - \[
\] Mark each claim: approved / needs evidence / remove / rewrite. - \[
\] Create `claims.registry.ts`. - \[ \] Update owner questions in
`docs/redesign/GRILL_ME.md`.

**Gate 1:** Any unverified claim is not displayed as fact. High-risk
legal, financial, employment and accreditation claims require owner
approval.

### Phase 2 --- Information architecture and route contract

**Goal:** Establish page hierarchy and separate product funnels.

Tasks: - \[ \] Approve navigation structure. - \[ \] Define homepage
audience entry points. - \[ \] Define course / programme / fellowship /
internship boundaries. - \[ \] Define startup and institution partner
routes. - \[ \] Map old route → new route. - \[ \] Define canonical and
redirect policy. - \[ \] Define English / Hindi route strategy. - \[ \]
Define city page eligibility and indexation rules. - \[ \] Create
`docs/redesign/ROUTE_MAP.md`.

**Gate 2:** Every route has an audience, purpose, owner, CTA, data
source and SEO status.

### Phase 3 --- Design tokens and reusable component foundation

**Goal:** Build a cohesive design system before rebuilding individual
pages.

Tasks: - \[ \] Create light-first design tokens. - \[ \] Add typography
with Devanagari support. - \[ \] Create shared spacing, container, grid
and breakpoint rules. - \[ \] Rebuild buttons, links, cards, form
controls and badges. - \[ \] Rebuild header, mega menu, mobile drawer
and footer. - \[ \] Create focus, hover, active, loading, disabled and
error states. - \[ \] Preserve hand-drawn elements as subtle accents. -
\[ \] Audit `Reveal` reduced-motion and no-JS behaviour. - \[ \] Build
Storybook or a local component showcase if repository tooling supports
it. - \[ \] Add visual regression screenshots for core components.

**Gate 3:** Components pass keyboard, responsive and contrast checks
before page migration.

### Phase 4 --- Sample homepage and startup page

**Goal:** Prove the new system on two distinct audience experiences.

Tasks: - \[ \] Build homepage using Section 4. - \[ \] Build startup
page using Section 5. - \[ \] Use authentic existing project/product
assets where approved. - \[ \] Add licensed stock imagery and asset
manifest. - \[ \] Reuse `HandNote`, `HandDrawnArrow`, `Reveal`,
`StudioInPractice`, `AudienceDoors`, `ProcessSteps`, `ProductCard`,
`CaseProof` only where appropriate. - \[ \] Add four audience doors. -
\[ \] Add real project proof. - \[ \] Add counselling CTA. - \[ \] Add
founder application CTA. - \[ \] Ensure startup page claims are
approved. - \[ \] Test desktop and mobile.

**Gate 4:** Product owner reviews homepage and startup page before
applying the visual system to all other routes.

### Phase 5 --- Learner hub and programme architecture

Tasks: - \[ \] Redesign `/learners`. - \[ \] Redesign
`/learners/courses`. - \[ \] Redesign Launchpad overview. - \[ \]
Redesign Accelerate overview. - \[ \] Redesign Fellowship overview. - \[
\] Redesign course detail pages with a common template. - \[ \] Create
comparison table. - \[ \] Clarify eligibility, prerequisites, weekly
workload, outcomes and fee inclusions. - \[ \] Remove conflicting
duration labels and old placement claims. - \[ \] Make lead capture
counselling-first. - \[ \] Add clear LMS handoff only when appropriate.

**Gate 5:** Every programme can be accurately explained by a first-time
learner in under two minutes.

### Phase 6 --- Internship recruitment funnel

Tasks: - \[ \] Redesign internship hub. - \[ \] Redesign domain pages. -
\[ \] Separate real vacancies from general programme pages. - \[ \]
Display role responsibilities, eligibility, duration, hours, location
and compensation terms where verified. - \[ \] Remove course-payment CTA
from recruitment pages unless explicitly approved and clearly
disclosed. - \[ \] Repair `JobPosting` schema. - \[ \] Validate
application submission and LMS handoff. - \[ \] Add clear no-openings
state.

**Gate 6:** A candidate can tell whether they are applying for an actual
internship role or requesting course counselling.

### Phase 7 --- City and partner landing pages

Tasks: - \[ \] Rebuild city profile schema. - \[ \] Remove technology
park addresses masquerading as DBERT addresses. - \[ \] Add partner
status and public-display permission. - \[ \] Build city page
template. - \[ \] Add local delivery mode and partner details. - \[ \]
Add genuinely unique local content. - \[ \] Add city-prefilled
counselling. - \[ \] Add index / noindex rules. - \[ \] Repair
canonical, sitemap and structured data. - \[ \] Fix tier-specific route
validation. - \[ \] Remove invalid or empty programme-city
combinations. - \[ \] Test all generated route combinations.

**Gate 7:** No city page publishes a false physical location, false
partner claim or thin duplicate content.

### Phase 8 --- Institution partner and about pages

Tasks: - \[ \] Build institution partnership landing page. - \[ \]
Redesign About DBERT. - \[ \] Redesign Team / Mentors only with verified
profiles. - \[ \] Redesign credentials / verification information. - \[
\] Redesign contact and careers. - \[ \] Review all logos and partner
claims. - \[ \] Add institution enquiry form.

**Gate 8:** Institutional offer and delivery responsibilities are clear
and factually approved.

### Phase 9 --- English / Hindi localization

Tasks: - \[ \] Implement locale routing. - \[ \] Translate navigation
and core page copy. - \[ \] Translate forms, errors, confirmation and
privacy language. - \[ \] Add Hindi typography and layout checks. - \[
\] Add canonical and `hreflang`. - \[ \] Test route-preserving language
switch. - \[ \] Human-review legal and programme wording.

**Gate 9:** No visible language toggle points to untranslated or broken
content.

### Phase 10 --- SEO, performance and accessibility hardening

Tasks: - \[ \] Validate all metadata. - \[ \] Validate canonical URLs. -
\[ \] Validate sitemap / robots. - \[ \] Validate schema with Google's
Rich Results Test where applicable. - \[ \] Remove invalid JobPosting
schema. - \[ \] Add image alt text. - \[ \] Run Lighthouse mobile /
desktop. - \[ \] Run axe or equivalent accessibility checks. - \[ \]
Check keyboard-only navigation. - \[ \] Check reduced motion. - \[ \]
Check Hindi rendering. - \[ \] Optimize image sizes and fonts. - \[ \]
Check Core Web Vitals. - \[ \] Check broken links and redirect chains.

**Gate 10:** No critical accessibility, SEO or performance regressions.

### Phase 11 --- Conversion, analytics and privacy

Tasks: - \[ \] Normalize analytics events. - \[ \] Validate UTM
attribution. - \[ \] Validate lead capture success / failure. - \[ \]
Validate duplicate submission handling. - \[ \] Validate privacy notice
and consent. - \[ \] Confirm PII is not sent to analytics. - \[ \] Test
counselling confirmation. - \[ \] Test startup enquiry. - \[ \] Test
internship application. - \[ \] Test mobile sticky CTA. - \[ \] Verify
CRM / backend delivery where applicable.

**Gate 11:** Every primary CTA has a measured and tested destination.

### Phase 12 --- Full regression, launch and handover

Tasks: - \[ \] Run all automated tests. - \[ \] Run production build. -
\[ \] Run route crawl. - \[ \] Test every form. - \[ \] Test every
external link. - \[ \] Test payment / LMS / verification links without
making real charges. - \[ \] Test mobile devices and major browsers. -
\[ \] Run visual comparison. - \[ \] Review analytics. - \[ \] Review
SEO indexation. - \[ \] Review redirects. - \[ \] Create deployment and
rollback instructions. - \[ \] Create
`docs/redesign/RELEASE_REPORT.md`. - \[ \] Update README / DEVELOPMENT
docs. - \[ \] Record unresolved owner questions.

**Gate 12:** Do not deploy if core application, payment, authentication,
lead capture or recruitment paths fail.

------------------------------------------------------------------------

## 17. Progress tracking and resume protocol

Create `docs/redesign/PROGRESS.md` with this structure and update it on
every work session:

``` md
# DBERT Website Redesign — Progress

## Current status
- Current phase:
- Current task:
- Last completed checkpoint:
- Next action:
- Branch:
- Last commit:
- Last successful build:
- Blockers:

## Phase checklist
- [ ] Phase 0 — Baseline
- [ ] Phase 1 — Claims
- [ ] Phase 2 — IA and routes
- [ ] Phase 3 — Design system
- [ ] Phase 4 — Homepage + Startup
- [ ] Phase 5 — Learner and programme pages
- [ ] Phase 6 — Internship
- [ ] Phase 7 — City / partners
- [ ] Phase 8 — About / institution
- [ ] Phase 9 — Hindi / English
- [ ] Phase 10 — SEO / accessibility / performance
- [ ] Phase 11 — Conversion / analytics
- [ ] Phase 12 — Regression / release

## Task log
| Date | Phase | Task | Files changed | Validation | Result | Commit |
|---|---|---|---|---|---|---|

## Decisions
| ID | Question | Decision | Owner | Date |
|---|---|---|---|---|

## Known regressions
| ID | Route / component | Description | Severity | Status |
|---|---|---|---|---|
```

### Resume rules

When restarting: 1. Read `PROGRESS.md`. 2. Read `GRILL_ME.md`. 3. Read
the last phase report. 4. Check current branch and git status. 5.
Inspect the last commit and modified files. 6. Run the relevant tests
before editing. 7. Continue from the first incomplete task; do not
repeat completed work. 8. Update progress and changelog before stopping.
9. Never overwrite uncommitted user work. 10. If the state is ambiguous,
stop and ask via `/grill-me`.

------------------------------------------------------------------------

## 18. Mandatory `/grill-me` questions

The agent must ask these questions at the correct phase and must not
invent answers. Questions may be batched only when the owner can answer
them efficiently.

### Business / factual questions

1.  What is the exact legal entity name to display, and what
    registrations may be publicly claimed?
2.  Which Indian cities have active institutional partners today?
    Provide partner name, address, relationship status and publication
    permission.
3.  Are partners delivering classes, hosting workshops, referring
    learners, providing venues or only supporting outreach?
4.  Is DBERT fully remote in any cities without a current partner?
5.  What exactly does each fee include: ₹7,999 Launchpad, ₹4,999
    Accelerate, ₹1,999 Fellowship?
6.  Why is Fellowship cheaper than Launchpad and Accelerate? Is ₹1,999 a
    fee, subsidized programme fee, deposit or separate offering?
7.  Are the three products all two months? Confirm weekly hours and
    actual mentor support.
8.  Is Fellowship selective? What are selection criteria and rejection /
    refund terms?
9.  Does any internship role currently have an actual stipend? Provide
    role-specific terms and eligibility.
10. What is the exact relationship between Fellowship and Internship
    recruitment?
11. Which certificate is issued, by which legal entity, and what exactly
    is verified?
12. What can DBERT legally and operationally promise about internship
    assignment, project work, referrals and employment?
13. Which partner logos may be shown and what exact relationship may be
    stated?
14. Which project screenshots / GitHub repositories can be shown
    publicly?
15. Which learner photos and testimonials have written consent?
16. Which startup incubation services are currently available versus
    aspirational?
17. Are equity, grant, legal, investor and IP services actually offered?
    Provide approved agreement / policy details.
18. Who owns deliverables created by DBERT, fellows and external
    contributors?
19. What response time can admissions / founder relations actually meet?
20. Who will review Hindi translations?

### Technical questions

21. What is the current production branch and deployment environment?
22. Are current lead forms connected to CRM, database, email or
    WhatsApp?
23. Is there a consent / privacy policy endpoint already in production?
24. Is bilingual routing already implemented elsewhere?
25. Which analytics events and dashboards are currently active?
26. Which external integrations must remain unchanged?
27. Is the current payment checkout still active and what is the exact
    flow?
28. Which pages are indexed and receiving organic traffic? Do not delete
    or redirect without evidence.
29. Are any city pages used by active paid campaigns?
30. Which assets may be reused and which are obsolete?

### Decision rule

If the owner does not answer: - Do not invent. - Keep the feature behind
a disabled flag or omit it. - Use a neutral, accurate statement. - Add
the question to the unresolved decisions list. - Continue only on tasks
that do not depend on the answer.

------------------------------------------------------------------------

## 19. QA test matrix

### 19.1 Route tests

-   [ ] `/`
-   [ ] `/startups`
-   [ ] `/about`
-   [ ] `/about/team`
-   [ ] `/about/contact`
-   [ ] `/learners`
-   [ ] `/learners/courses`
-   [ ] `/learners/launchpad`
-   [ ] `/learners/accelerate`
-   [ ] `/learners/fellowship`
-   [ ] All published course detail routes
-   [ ] `/internships`
-   [ ] All published internship domain routes
-   [ ] All valid city routes
-   [ ] `/partners` if implemented
-   [ ] `/verify` and directory
-   [ ] LMS login and application handoffs

For each route: - HTTP status correct. - No blank render. - No console
errors. - No hydration mismatch. - No missing images. - Correct title /
description / canonical. - Correct CTA destination. - Mobile layout
passes. - Hindi route passes where available.

### 19.2 Funnel tests

**Counselling** - Valid form submits once. - Invalid email rejected. -
Invalid phone handled. - Network failure retains values. - Duplicate
click does not create duplicate lead. - Success shows reference. -
Consent recorded. - PII not present in analytics.

**Startup** - Application can be started and submitted. - Optional URLs
do not block. - Sensitive information is not requested prematurely. -
Confirmation and next step are accurate.

**Internship** - Actual job application is distinct from course
enquiry. - No payment required unless explicitly and lawfully part of a
disclosed programme. - Role details are consistent. - Expired roles are
not presented as open. - Job schema only on genuine vacancies.

**LMS** - Login link works. - Enrollment handoff preserves intended
programme. - Existing authentication is not broken. - No payment
transaction is executed during QA.

### 19.3 Visual tests

-   [ ] 360px mobile
-   [ ] 390px mobile
-   [ ] 430px mobile
-   [ ] 768px tablet
-   [ ] 1024px laptop
-   [ ] 1280px desktop
-   [ ] 1440px wide desktop
-   [ ] English long content
-   [ ] Hindi long content
-   [ ] Keyboard navigation
-   [ ] Reduced motion
-   [ ] 200% zoom
-   [ ] Slow network
-   [ ] No JavaScript fallback for key content

------------------------------------------------------------------------

## 20. Definition of done

The redesign is complete only when:

1.  All public pages follow the new design system.
2.  Homepage and startup page are approved examples of the design.
3.  Courses, Launchpad, Accelerate, Fellowship and internships are
    clearly differentiated.
4.  The counselling-first flow works end-to-end.
5.  City pages show real partner/delivery facts and no fabricated
    locations.
6.  Startup claims are verified and legally reviewed.
7.  Placement and internship claims are consistent with actual terms.
8.  Pricing is sourced centrally and consistent across every route.
9.  English and Hindi work on all approved routes.
10. Existing LMS, auth, API, payment and verification paths remain
    functional.
11. All high-priority QA checks pass.
12. SEO metadata and structured data are valid.
13. No critical accessibility issue remains.
14. Performance targets are met or exceptions are documented.
15. `PROGRESS.md`, `GRILL_ME.md`, `ROUTE_MAP.md`, `BASELINE_AUDIT.md`
    and `RELEASE_REPORT.md` are updated.
16. The final report lists every changed file, migration, known issue
    and rollback instruction.

------------------------------------------------------------------------

## 21. Agent operating prompt

You are the senior frontend architect and implementation agent working
inside the existing DBERT repository.

Your task is to implement this specification in the existing codebase,
not to generate a disconnected mock website.

### Required behaviour

-   Start at Phase 0.
-   Inspect before editing.
-   Keep a clean branch and preserve user work.
-   Ask `/grill-me` questions for unresolved business decisions.
-   Do not fabricate claims, proof, metrics, partners, locations or
    legal terms.
-   Keep API contracts and backend behaviour intact.
-   Use the current app architecture and existing reusable components
    where appropriate.
-   Replace generic AI-slop layouts with clear, purposeful information
    architecture and authentic visual evidence.
-   Build homepage and startup sample pages first.
-   Validate each phase before continuing.
-   Update progress files and commit-sized change logs.
-   Do not claim a test passed unless it was actually run.
-   Do not silently swallow errors or return blank pages.
-   Do not remove routes without a redirect and SEO impact assessment.
-   Do not use stock images without recording their source and license.
-   Do not deploy or perform real payment actions without explicit
    authorization.

### First action

Read the repository instructions and run baseline checks. Then create: -
`docs/redesign/BASELINE_AUDIT.md` - `docs/redesign/PROGRESS.md` -
`docs/redesign/GRILL_ME.md` - `docs/redesign/ROUTE_MAP.md`

After Phase 0, present the findings and unresolved owner questions. Wait
for approval at Gate 0 / Gate 1 where business truth is required. Do not
immediately rewrite all pages in one large commit.

------------------------------------------------------------------------

## Appendix A --- Existing files to inspect first

  ---------------------------------------------------------------------------------------------------
  File                                                            Purpose
  --------------------------------------------------------------- -----------------------------------
  `apps/website/src/app/page.tsx`                                 Homepage

  `apps/website/src/app/startups/page.tsx`                        Startup/incubation page

  `apps/website/src/app/learners/page.tsx`                        Learner hub

  `apps/website/src/app/learners/courses/page.tsx`                Course catalogue

  `apps/website/src/app/learners/fellowship/page.tsx`             Fellowship details

  `apps/website/src/components/programs/ProgramCityLanding.tsx`   Shared city programme template

  `apps/website/src/data/geo_domains.config.ts`                   City and domain registry

  `apps/website/src/data/courses.core.ts`                         Core course data

  `apps/website/src/data/courses.specialized.ts`                  Specialized course data

  `apps/website/src/data/launchpadDomains.ts`                     Launchpad programme data

  `apps/website/src/data/accelerateDomains.ts`                    Accelerate programme data

  `apps/website/src/config/pricing.config.ts`                     Pricing configuration

  `apps/website/src/components/forms/TrackLeadCaptureForm.tsx`    Lead capture form

  `apps/website/src/components/layout/MegaMenu.tsx`               Navigation

  `apps/website/src/data/nav.config.json`                         Navigation data

  `apps/website/src/app/globals.css`                              Global tokens and styles

  `apps/website/src/app/about/page.tsx`                           About page

  `apps/website/src/components/ui/HandNote.tsx`                   Handcrafted annotation

  `apps/website/src/components/ui/HandDrawnArrow.tsx`             Handcrafted arrow

  `apps/website/src/components/ui/Reveal.tsx`                     Scroll reveal

  `apps/website/src/components/ui/StudioInPractice.tsx`           Interactive engagement

  `apps/website/src/components/ui/AudienceDoors.tsx`              Audience routing cards

  `apps/website/src/components/ui/CareerLadder.tsx`               Programme progression

  `apps/website/src/components/ui/PrReviewTerminal.tsx`           Code review proof component; verify
                                                                  data before reuse
  ---------------------------------------------------------------------------------------------------

## Appendix B --- Visual inspiration search terms

Use these as art direction, not as references to clone: - modern Indian
startup education website - premium Indian technology institute
website - Indian students collaborative coding workshop - Indian founder
product team working on SaaS - modern editorial education landing page -
warm neutral navy saffron web design - Indian university innovation lab
photography

## Appendix C --- Repository links

-   Repository: https://github.com/DBERT-INDIA/dbert-website-lms
-   Public website: https://dbert.in
-   LMS: https://lms.dbert.in
-   Certificate verification: https://dbert.in/verify/
-   Certificate directory: https://dbert.in/verify/directory

**End of specification.**
