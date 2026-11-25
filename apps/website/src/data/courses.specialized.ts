import type { FellowshipTrack } from './courses.types';

export const SPECIALIZED_FELLOWSHIP_TRACKS: FellowshipTrack[] = [
  {
    id: 'ui-ux-design',
    slug: 'ui-ux-design',
    canonicalPath: '/learners/courses/ui-ux-design',
    name: 'UI/UX Design',
    shortName: 'UI/UX & Design Systems',
    badge: 'Design Track',
    category: 'Product & Growth',
    featured: false,
    displayOrder: 7,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Design accessible, token-driven Figma component systems and developer-ready product flows for live web applications.',
    shortDescription:
      'Figma Auto-Layout, atomic design tokens, user journey mapping, WCAG 2.2 AA accessibility, and React/Tailwind developer handoff.',
    fullDescription:
      'UI/UX Design trains product designers to work directly inside engineering squads. Instead of isolated static Dribbble shots, fellows build responsive Figma component libraries, run usability audits, enforce WCAG contrast/focus standards, and deliver clean specs for React/Next.js engineers.',
    whoShouldApply: [
      'Aspiring product designers and frontend-leaning creators who want real engineering-squad handoff experience.',
      'Designers looking to master Figma component variants, design tokens, and accessibility.',
    ],
    prerequisites: [
      'Basic familiarity with Figma or any visual layout tool.',
      'Willingness to collaborate asynchronously with frontend engineers using structured specs.',
    ],
    outcomes: [
      'Build scalable Figma component libraries using Auto-Layout and semantic design tokens.',
      'Conduct structured user journey mapping and usability evaluations.',
      'Audit interfaces against WCAG 2.2 AA contrast, typography, and keyboard-focus standards.',
      'Deliver developer-ready Tailwind/CSS handoff specifications.',
    ],
    technologies: [
      { name: 'Figma & FigJam', role: 'Auto-Layout systems, component variants, and user flow mapping' },
      { name: 'Design Tokens', role: 'Semantic color, spacing, and typography variables for code parity' },
      { name: 'WCAG 2.2 AA', role: 'Contrast verification, focus states, and accessible form patterns' },
      { name: 'Tailwind CSS Specs', role: 'Developer-ready responsive breakpoints and spacing handoff' },
      { name: 'Git / PR Review', role: 'Collaborating on live UI polish and design QA issues' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Information Architecture & User Flows',
        topics: [
          'Task-first user journey mapping and wireframe flows',
          'Visual hierarchy, typographic scale, and spacing grids',
          'First design critique and squad onboarding',
        ],
        deliverable: 'Annotated user flow and low-fidelity wireframe spec for a live portal module.',
      },
      {
        period: 'Weeks 3–4',
        title: 'Figma Component Systems & Auto-Layout',
        topics: [
          'Responsive Auto-Layout constraints (320px to 1440px)',
          'Atomic component variants (buttons, inputs, error/empty/loading states)',
          'Semantic color and surface tokens',
        ],
        deliverable: 'Reusable Figma component library with documented states.',
      },
      {
        period: 'Weeks 5–6',
        title: 'Prototyping, Usability & Accessibility Audits',
        topics: [
          'Interactive prototypes for multi-step application/checkout flows',
          'WCAG 2.2 AA contrast, touch-target, and keyboard-order audits',
          'Heuristic evaluation of live web pages',
        ],
        deliverable: 'Accessibility & usability audit report with redesigned screens.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Developer Handoff & Capstone Release',
        topics: [
          'Writing exact responsive specs and edge-case states for engineers',
          'Design QA against staging builds',
          'Final portfolio dossier and 3-document credential issuance',
        ],
        deliverable: 'Complete product design system, prototype, and verified credential packet.',
      },
    ],
    capstone: {
      title: 'Venture Portal Design System & Responsive Flow',
      description:
        'Design and specify a complete accessible multi-step user flow and reusable Figma token system for Gayatri AI or the DBERT LMS Portal.',
      status: 'active',
      ventureName: 'Gayatri AI & DBERT Portal',
      repositoryUrl: 'https://github.com/DBERT-INDIA/Internshipportal',
      acceptanceCriteria: [
        'Full responsive specs for 320px, 375px, 768px, and 1440px viewports.',
        'All text/surface pairs pass WCAG AA contrast.',
        'Includes explicit loading, empty, and error states.',
      ],
    },
    evaluation: [
      'System Consistency: Reusable tokens and Auto-Layout discipline.',
      'Accessibility: Verified contrast, focus order, and mobile touch targets.',
      'Engineering Handoff: Clear edge-case states and responsive rules.',
      'Documentation: Concise case study explaining design trade-offs.',
    ],
    faqs: [
      {
        question: 'Do UI/UX fellows need to write production code?',
        answer:
          'No coding is required, though you will learn how CSS/Tailwind tokens map to Figma variables so your handoffs are immediately usable by engineers.',
      },
    ],
    relatedSlugs: ['full-stack-development', 'digital-marketing', 'mobile-app-development'],
    regionalOpportunities: [
      {
        title: 'Product & UI/UX Design Intern',
        roleDescription: 'Build Figma design systems, prototypes, and accessibility specs.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/ui-ux-design',
        tags: ['Figma', 'Design Systems', 'WCAG', 'Prototyping'],
      },
    ],
  },
  {
    id: 'devops-cloud',
    slug: 'devops-cloud',
    canonicalPath: '/learners/courses/devops-cloud',
    name: 'DevOps & Cloud Engineering',
    shortName: 'DevOps & Cloud',
    badge: 'Infra Track',
    category: 'Software & Cloud',
    featured: false,
    displayOrder: 8,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Automate reproducible builds, containerized deployments, reverse-proxy TLS, and operational monitoring on Linux and cloud servers.',
    shortDescription:
      'Linux administration, multi-stage Docker builds, GitHub Actions CI/CD, Nginx reverse proxies, Terraform basics, and observability.',
    fullDescription:
      'DevOps & Cloud Engineering focuses on reliable deployment and operational hygiene. Fellows learn Linux process supervision, multi-stage Dockerfiles, CI/CD pipelines with GitHub Actions, Nginx reverse-proxy configuration, and structured monitoring/rollback procedures.',
    whoShouldApply: [
      'Developers and sysadmin-leaning learners who want hands-on Linux, Docker, and CI/CD experience.',
      'Backend/full-stack engineers who want to own build pipelines and production reliability.',
    ],
    prerequisites: [
      'Basic command-line comfort and Git fundamentals.',
      'Familiarity with at least one web/backend stack (Node.js or Python).',
    ],
    outcomes: [
      'Write lean multi-stage Dockerfiles and Docker Compose stacks.',
      'Build automated lint, test, and build CI pipelines in GitHub Actions.',
      'Configure Nginx reverse proxies, TLS termination, and systemd services.',
      'Document reproducible deployment, backup, and rollback runbooks.',
    ],
    technologies: [
      { name: 'Linux & Bash', role: 'Process supervision (systemd), permissions, and diagnostics' },
      { name: 'Docker & Compose', role: 'Multi-stage builds and isolated service networking' },
      { name: 'GitHub Actions', role: 'Automated CI checks, build verification, and artifact pipelines' },
      { name: 'Nginx', role: 'Reverse proxying, compression, and TLS/security headers' },
      { name: 'Terraform / AWS Basics', role: 'Declarative cloud resource provisioning concepts' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Linux Diagnostics & Shell Automation',
        topics: [
          'Linux file permissions, networking, ports, and systemd units',
          'Safe Bash scripting with strict error handling',
          'First reviewed PR on repository build/ops scripts',
        ],
        deliverable: 'Automated server health-check and backup verification script.',
      },
      {
        period: 'Weeks 3–4',
        title: 'Containerization with Docker & Compose',
        topics: [
          'Multi-stage Dockerfiles for Next.js and Python services',
          'Non-root containers, healthchecks, and environment hygiene',
          'Local multi-service orchestration with PostgreSQL & Redis',
        ],
        deliverable: 'Hardened multi-stage Dockerfile and Compose stack.',
      },
      {
        period: 'Weeks 5–6',
        title: 'CI/CD Pipelines & Reverse Proxies',
        topics: [
          'GitHub Actions workflows for lint, typecheck, test, and build',
          'Nginx reverse proxy rules, caching headers, and TLS basics',
          'Zero-downtime restart and rollback patterns',
        ],
        deliverable: 'Automated CI pipeline and Nginx configuration template.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Observability, Runbooks & Capstone Audit',
        topics: [
          'Structured log inspection, disk/memory alerts, and incident runbooks',
          'Security audit (no committed secrets, least-privilege IAM)',
          'Final review and 3-document credential issuance',
        ],
        deliverable: 'Production deployment & rollback blueprint with verified CI.',
      },
    ],
    capstone: {
      title: 'Reproducible CI/CD & Containerized Deployment Blueprint',
      description:
        'Containerize a full-stack/API service, automate its CI verification pipeline in GitHub Actions, and document a tested rollback runbook.',
      status: 'active',
      ventureName: 'DBERT Infrastructure',
      repositoryUrl: 'https://github.com/DBERT-INDIA/Internshipportal',
      acceptanceCriteria: [
        'Container runs as non-root user and passes healthcheck.',
        'CI workflow catches lint/type/build failures automatically.',
        'Rollback runbook verified on local/staging container setup.',
      ],
    },
    evaluation: [
      'Security Hygiene: Non-root containers, zero hardcoded secrets, safe permissions.',
      'Reproducibility: Deterministic builds and pinned base image tags.',
      'Automation: Clean CI workflows and idempotent scripts.',
      'Documentation: Clear architecture and rollback runbook.',
    ],
    faqs: [
      {
        question: 'Do I need a paid AWS account to complete this track?',
        answer:
          'No. All container, CI/CD, Nginx, and IaC dry-run exercises can be completed locally and on GitHub Actions without incurring cloud bills.',
      },
    ],
    relatedSlugs: ['full-stack-development', 'cybersecurity', 'python-automation'],
    regionalOpportunities: [
      {
        title: 'DevOps & Cloud Automation Intern',
        roleDescription: 'Maintain Docker builds, GitHub Actions CI, and Linux deployment scripts.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/devops-cloud',
        tags: ['Docker', 'GitHub Actions', 'Linux', 'Nginx'],
      },
    ],
  },
  {
    id: 'mobile-app-development',
    slug: 'mobile-app-development',
    canonicalPath: '/learners/courses/mobile-app-development',
    name: 'Mobile App Development',
    shortName: 'Mobile (Flutter / RN)',
    badge: 'Mobile Track',
    category: 'Software & Cloud',
    featured: false,
    displayOrder: 9,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Build cross-platform iOS and Android applications with clean state management, offline persistence, and authenticated REST API sync.',
    shortDescription:
      'Flutter/Dart or React Native architecture, offline SQLite caching, authenticated API integration, and release build verification.',
    fullDescription:
      'Mobile App Development focuses on shipping reliable cross-platform apps that handle real-world network conditions gracefully. Fellows implement typed navigation, predictable state management, local SQLite offline caching, and authenticated backend synchronization.',
    whoShouldApply: [
      'Students and developers who want to ship cross-platform mobile apps backed by real APIs.',
      'Web developers transitioning into Flutter or React Native.',
    ],
    prerequisites: [
      'Basic OOP or JavaScript/TypeScript fundamentals.',
      'Familiarity with REST APIs and Git.',
    ],
    outcomes: [
      'Structure modular cross-platform mobile apps with clean state management.',
      'Integrate authenticated REST APIs with loading, retry, and offline fallback states.',
      'Persist structured user data locally using SQLite.',
      'Package signed Android release builds and run automated widget/component tests.',
    ],
    technologies: [
      { name: 'Flutter / Dart', role: 'Cross-platform UI widgets, async streams, and native compilation' },
      { name: 'React Native / TypeScript', role: 'Alternative cross-platform mobile stack option' },
      { name: 'SQLite', role: 'Reliable offline-first local caching and sync queues' },
      { name: 'REST APIs & JWT', role: 'Authenticated mobile networking and token refresh' },
      { name: 'Git & CI', role: 'Pull request reviews and automated build checks' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Cross-Platform UI & Navigation Architecture',
        topics: [
          'Responsive layouts across small and large mobile screens',
          'Typed navigation stacks and form validation',
          'First reviewed PR on mobile module',
        ],
        deliverable: 'Multi-screen mobile shell with validated input forms.',
      },
      {
        period: 'Weeks 3–4',
        title: 'State Management & Authenticated Networking',
        topics: [
          'Predictable state management (Riverpod/BLoC or Zustand/Context)',
          'Typed API clients, timeouts, and error/retry UX',
          'Secure token storage',
        ],
        deliverable: 'Authenticated API-connected feature flow.',
      },
      {
        period: 'Weeks 5–6',
        title: 'Offline Persistence & Device Capabilities',
        topics: [
          'Local SQLite caching and offline-to-online sync patterns',
          'Handling permissions, deep links, and notifications cleanly',
          'Performance profiling (frame drops & list virtualization)',
        ],
        deliverable: 'Offline-capable list/detail module with sync status indicator.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Testing, Release Packaging & Credential Audit',
        topics: [
          'Widget/unit testing and reproducible Android APK/AAB builds',
          'Store readiness checklist and documentation',
          'Final PR review and 3-document credential issuance',
        ],
        deliverable: 'Tested cross-platform mobile capstone and verified credential packet.',
      },
    ],
    capstone: {
      title: 'Offline-Capable Companion Mobile App',
      description:
        'Build a cross-platform mobile client for an internal DBERT or venture API featuring authentication, offline SQLite caching, and clean error recovery.',
      status: 'proposed',
      ventureName: 'DBERT Mobile Workbench',
      acceptanceCriteria: [
        'App remains usable offline for cached views and recovers gracefully on reconnect.',
        'All forms validate inputs and announce errors accessibly.',
        'Builds cleanly into a verifiable Android release artifact.',
      ],
    },
    evaluation: [
      'UX Resilience: Clear loading, empty, offline, and error states.',
      'Code Architecture: Separation of UI, state, and networking layers.',
      'Testing: Passing unit/widget tests.',
      'Documentation: Setup steps and architecture overview.',
    ],
    faqs: [
      {
        question: 'Do I need a Mac to join Mobile App Development?',
        answer:
          'No. You can develop, test, and build Android APKs on Windows or Linux.',
      },
    ],
    relatedSlugs: ['full-stack-development', 'ui-ux-design', 'devops-cloud'],
    regionalOpportunities: [
      {
        title: 'Cross-Platform Mobile App Intern',
        roleDescription: 'Build Flutter/React Native screens, offline caching, and API integrations.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/mobile-app-development',
        tags: ['Flutter', 'React Native', 'SQLite', 'REST APIs'],
      },
    ],
  },
  {
    id: 'cybersecurity',
    slug: 'cybersecurity',
    canonicalPath: '/learners/courses/cybersecurity',
    name: 'Cybersecurity & Threat Defense',
    shortName: 'Cybersecurity',
    badge: 'Security Track',
    category: 'Software & Cloud',
    featured: false,
    displayOrder: 10,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Identify web and infrastructure vulnerabilities, harden applications against OWASP Top 10 risks, and write actionable security audit reports.',
    shortDescription:
      'OWASP Top 10 testing, network packet analysis with Wireshark, Linux hardening, security headers, and defensive SOC log triage.',
    fullDescription:
      'Cybersecurity & Threat Defense teaches practical defensive and offensive fundamentals on authorized, isolated targets and real web application codebases. Fellows learn how vulnerabilities happen in code, how to verify them safely, and how to submit remediation PRs.',
    whoShouldApply: [
      'CS/IT students and developers aiming for AppSec, SOC Analyst, or Junior Security Engineer roles.',
      'Software engineers who want to master secure coding and vulnerability remediation.',
    ],
    prerequisites: [
      'Basic understanding of HTTP, TCP/IP, DNS, and Linux command line.',
      'Ability to read basic web/backend code (Python or JavaScript).',
    ],
    outcomes: [
      'Audit web applications for OWASP Top 10 flaws (injection, broken auth/BOLA, XSS, CSRF, SSRF).',
      'Inspect network traffic with Wireshark and perform authorized service enumeration.',
      'Harden Linux hosts, HTTP security headers (CSP, HSTS), and rate-limiting rules.',
      'Write clear CVSS-scored remediation reports and security-fix pull requests.',
    ],
    technologies: [
      { name: 'OWASP Top 10', role: 'Structured web application threat modeling and verification' },
      { name: 'Burp Suite & Nmap', role: 'Authorized HTTP proxy inspection and service auditing' },
      { name: 'Wireshark', role: 'Packet capture analysis and protocol troubleshooting' },
      { name: 'Wazuh / SIEM Logs', role: 'Defensive log correlation and alert triage' },
      { name: 'Linux & Python', role: 'Host hardening and security automation scripts' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Networking, Linux Hardening & Traffic Analysis',
        topics: [
          'TCP/IP, TLS handshakes, and Wireshark packet inspection',
          'Linux file permissions, SSH hardening, and firewall rules',
          'First security hygiene PR (headers, secret scanning)',
        ],
        deliverable: 'Network capture analysis and Linux hardening checklist.',
      },
      {
        period: 'Weeks 3–4',
        title: 'Web App Security & OWASP Top 10',
        topics: [
          'Authentication/session flaws, BOLA/IDOR, and access control testing',
          'SQL injection, XSS, CSRF, and SSRF mechanics and defenses',
          'Authorized proxy inspection with Burp Suite Community',
        ],
        deliverable: 'Vulnerability verification report on an isolated sandbox target.',
      },
      {
        period: 'Weeks 5–6',
        title: 'Defensive Monitoring, SIEM & Code Remediation',
        topics: [
          'Log analysis and anomaly detection concepts',
          'Writing parameterized queries, CSP policies, and rate limiters',
          'Submitting remediation pull requests',
        ],
        deliverable: 'Reviewed code remediation PR fixing simulated security findings.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Security Audit Dossier & Credential Release',
        topics: [
          'CVSS severity scoring and executive remediation summaries',
          'Turnitin originality check and final senior review',
          '3-document verifiable credential issuance',
        ],
        deliverable: 'Comprehensive security audit report and verified credential packet.',
      },
    ],
    capstone: {
      title: 'Application Security Audit & Remediation PR',
      description:
        'Conduct a structured OWASP Top 10 audit on an authorized staging/sandbox web application, document findings with reproducible steps, and submit code-level fixes.',
      status: 'active',
      ventureName: 'DBERT Security Suite',
      repositoryUrl: 'https://github.com/DBERT-INDIA/Internshipportal',
      acceptanceCriteria: [
        'All findings include clear reproduction steps and remediation code.',
        'Zero unauthorized scanning outside approved sandbox targets.',
        'Turnitin < 5% on final audit report.',
      ],
    },
    evaluation: [
      'Ethical & Legal Discipline: Strict adherence to authorized scope.',
      'Technical Accuracy: Validated root causes without false positives.',
      'Remediation Quality: Clean, tested security fixes in code.',
      'Reporting: Clear severity ranking and actionable developer guidance.',
    ],
    faqs: [
      {
        question: 'Are offensive tests run against live public websites?',
        answer:
          'Never. All offensive testing exercises run strictly on isolated, authorized sandbox environments.',
      },
    ],
    relatedSlugs: ['devops-cloud', 'full-stack-development', 'python-automation'],
    regionalOpportunities: [
      {
        title: 'AppSec & Threat Defense Intern',
        roleDescription: 'Perform OWASP audits, harden HTTP headers, and triage security logs.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/cybersecurity',
        tags: ['OWASP', 'Wireshark', 'Burp Suite', 'Linux'],
      },
    ],
  },
  {
    id: 'digital-marketing',
    slug: 'digital-marketing',
    canonicalPath: '/learners/courses/digital-marketing',
    name: 'Digital Marketing & Growth',
    shortName: 'Digital Marketing',
    badge: 'Growth Track',
    category: 'Product & Growth',
    featured: false,
    displayOrder: 11,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Execute measurable technical SEO, funnel analytics, and conversion-focused content campaigns backed by real GA4 telemetry.',
    shortDescription:
      'Technical SEO, structured schema, GA4 funnel attribution, landing-page CRO, and B2B/B2C growth experimentation.',
    fullDescription:
      'Digital Marketing & Growth treats growth as an analytical discipline rather than guesswork. Fellows audit technical SEO, sitemaps, and JSON-LD structured data, instrument privacy-safe GA4 funnel events, run landing-page conversion audits, and produce evidence-backed growth reports.',
    whoShouldApply: [
      'Marketing graduates, content strategists, and technical generalists who want measurable, data-driven growth skills.',
      'Builders interested in technical SEO, analytics attribution, and conversion rate optimization.',
    ],
    prerequisites: [
      'Strong written communication and comfort working with spreadsheets and web analytics.',
      'Basic familiarity with HTML/CMS concepts is helpful; technical SEO tooling is taught in Weeks 1–2.',
    ],
    outcomes: [
      'Audit crawlability, canonical tags, sitemaps, and JSON-LD structured data.',
      'Configure privacy-compliant GA4 conversion funnels without leaking PII.',
      'Design and evaluate landing-page copy and CTA experiments for clarity and conversion.',
      'Build weekly acquisition and funnel performance reports.',
    ],
    technologies: [
      { name: 'Google Analytics 4 (GA4)', role: 'Event taxonomy, funnel tracking, and attribution analysis' },
      { name: 'Technical SEO & Schema', role: 'Sitemaps, robots.txt, canonicals, and JSON-LD validation' },
      { name: 'Search Console', role: 'Index coverage, query impression analysis, and CTR tuning' },
      { name: 'CRO & Copywriting', role: 'Landing-page value propositions, trust signals, and A/B hypotheses' },
      { name: 'Spreadsheets & Looker', role: 'Cohort/channel ROI reporting' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Technical SEO, Crawling & Information Architecture',
        topics: [
          'Robots.txt, XML sitemaps, canonical tags, and redirect hygiene',
          'Search intent mapping and topic clusters',
          'First live technical SEO audit',
        ],
        deliverable: 'Prioritized technical SEO audit with concrete fix tickets.',
      },
      {
        period: 'Weeks 3–4',
        title: 'Analytics Instrumentation & Funnel Attribution',
        topics: [
          'Designing clean, PII-free GA4 event taxonomies',
          'UTM governance and channel attribution',
          'Identifying funnel drop-offs accurately',
        ],
        deliverable: 'Documented analytics event spec and funnel report.',
      },
      {
        period: 'Weeks 5–6',
        title: 'Content Strategy & Conversion Optimization',
        topics: [
          'Writing honest, outcome-focused landing-page copy',
          'CTA hierarchy, social proof verification, and mobile UX checks',
          'Structured experimentation hypotheses',
        ],
        deliverable: 'Landing-page CRO teardown and revised copy brief.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Growth Experiment Report & Credential Release',
        topics: [
          'Synthesizing campaign metrics and next-quarter roadmap',
          'Turnitin originality audit on written deliverables',
          'Final review and 3-document credential issuance',
        ],
        deliverable: 'End-to-end growth & SEO dossier and verified credential packet.',
      },
    ],
    capstone: {
      title: 'Technical SEO & Funnel Optimization Dossier',
      description:
        'Execute a complete technical SEO, schema, and conversion funnel audit for an active DBERT venture product or portal, with measurable recommendations.',
      status: 'active',
      ventureName: 'DBERT Venture Growth',
      acceptanceCriteria: [
        'Zero PII included in proposed analytics event schemas.',
        'All SEO recommendations backed by crawl/index evidence.',
        'Turnitin < 5% on content and strategy deliverables.',
      ],
    },
    evaluation: [
      'Analytical Rigor: Decisions grounded in funnel/search data rather than vanity metrics.',
      'Technical Accuracy: Valid canonical, sitemap, and schema recommendations.',
      'Copy Clarity: Honest, specific messaging free of unverified claims.',
      'Documentation: Actionable tickets and clear reporting.',
    ],
    faqs: [
      {
        question: 'Is this a social-media-only marketing course?',
        answer:
          'No. We focus on technical SEO, GA4 funnel analytics, landing-page conversion optimization, and measurable growth systems.',
      },
    ],
    relatedSlugs: ['data-analytics', 'ui-ux-design', 'full-stack-development'],
    regionalOpportunities: [
      {
        title: 'Technical SEO & Growth Analytics Intern',
        roleDescription: 'Audit sitemaps, GA4 funnels, and conversion copy for venture products.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/digital-marketing',
        tags: ['Technical SEO', 'GA4', 'CRO', 'Content'],
      },
    ],
  },
];
