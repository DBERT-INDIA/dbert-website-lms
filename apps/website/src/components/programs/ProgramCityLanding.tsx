import React from 'react';
import Link from 'next/link';
import {
  MapPin,
  Calendar,
  Award,
  GitPullRequest,
  ShieldCheck,
  CheckCircle2,
  Building2,
  ArrowRight,
  ExternalLink
} from 'lucide-react';
import TrackLeadCaptureForm from '@/components/forms/TrackLeadCaptureForm';
import FAQAccordion from '@/components/ui/FAQAccordion';
import HandNote from '@/components/ui/HandNote';
import { getTrackBySlug } from '@/data/courses.config';
import { LAUNCHPAD_DOMAINS } from '@/data/launchpadDomains';
import { ACCELERATE_DOMAINS } from '@/data/accelerateDomains';
import { GEO_CITIES, GEO_SHORT_DOMAIN_LABELS } from '@/data/geo_domains.config';

export type ProgramTierKey = 'fellowship' | 'launchpad' | 'accelerate';

interface ProgramCityLandingProps {
  tier: ProgramTierKey;
  slug: string;
  city: string;
}

export default function ProgramCityLanding({ tier, slug, city }: ProgramCityLandingProps) {
  const cityData = GEO_CITIES[city];
  const fellowshipTrack = getTrackBySlug(slug);
  const launchpadTrack = LAUNCHPAD_DOMAINS[slug];
  const accelerateTrack = ACCELERATE_DOMAINS[slug];

  if (!cityData || !fellowshipTrack || !launchpadTrack || !accelerateTrack) {
    return null;
  }

  const cityName = cityData.name;
  const cityShort = cityData.shortName;
  const domainShort = GEO_SHORT_DOMAIN_LABELS[slug] || fellowshipTrack.name;

  const isFellowship = tier === 'fellowship';
  const isLaunchpad = tier === 'launchpad';

  const fee = isLaunchpad ? '₹7,999' : tier === 'accelerate' ? '₹4,999' : '₹1,999';
  const numericFee = isLaunchpad ? '7999' : tier === 'accelerate' ? '4999' : '1999';
  const programLabel = isLaunchpad
    ? 'DBERT Launchpad (Beginner 0-to-1)'
    : tier === 'accelerate'
    ? 'DBERT Accelerate (Applied Sprints)'
    : 'DBERT Fellowship (Production Internship)';

  const baseRoutePrefix = isLaunchpad
    ? '/learners/launchpad'
    : tier === 'accelerate'
    ? '/learners/accelerate'
    : '/learners/courses';

  const canonicalUrl = `https://dbert.in${baseRoutePrefix}/${slug}/${city}`;
  const parentUrl = isLaunchpad
    ? `/learners/launchpad?domain=${slug}`
    : tier === 'accelerate'
    ? `/learners/accelerate?domain=${slug}`
    : `/learners/courses/${slug}`;

  const primaryHref = isFellowship
    ? `/enroll/1999?domain=${encodeURIComponent(fellowshipTrack.name)}&city=${encodeURIComponent(cityShort)}`
    : isLaunchpad
    ? `/learners/launchpad?domain=${encodeURIComponent(slug)}`
    : `/learners/accelerate?domain=${encodeURIComponent(slug)}`;

  const primaryCtaLabel = isFellowship
    ? `Enroll in ${cityShort} Fellowship — ₹1,999 →`
    : isLaunchpad
    ? `Enroll in ${cityShort} Launchpad — ₹7,999 →`
    : `Enroll in ${cityShort} Accelerate — ₹4,999 →`;

  const curriculumBlocks = isLaunchpad
    ? launchpadTrack.curriculum
    : tier === 'accelerate'
    ? accelerateTrack.curriculum
    : fellowshipTrack.curriculum;

  const headlineSummary = isLaunchpad
    ? launchpadTrack.outcome
    : tier === 'accelerate'
    ? accelerateTrack.outcome
    : fellowshipTrack.heroOutcome;

  const trackTitle = isLaunchpad
    ? `${domainShort} Launchpad in ${cityName}`
    : tier === 'accelerate'
    ? `${domainShort} Accelerate in ${cityName}`
    : `${fellowshipTrack.name} Course in ${cityName}`;

  const repos = isLaunchpad
    ? launchpadTrack.githubRepos
    : tier === 'accelerate'
    ? accelerateTrack.githubRepos
    : fellowshipTrack.capstone.repositoryUrl
    ? [
        {
          name: fellowshipTrack.capstone.ventureName,
          url: fellowshipTrack.capstone.repositoryUrl,
          role: `${fellowshipTrack.name} Capstone`,
          badgeText: 'Client Production Repo',
          description: fellowshipTrack.capstone.description,
          keyModules: fellowshipTrack.capstone.acceptanceCriteria
        }
      ]
    : [];

  const faqs = [
    {
      question: `How does DBERT deliver the ${domainShort} ${programLabel} for learners in ${cityName}?`,
      answer: `Every DBERT cohort runs strictly for 2 months (8 weeks) with 100% remote weekly sprint delivery, 1:1 mentor code reviews, and verified credentials accessible anywhere in ${cityName} (${cityData.locality}, ${cityData.region}) without relocation.`
    },
    {
      question: `What is the fee for ${trackTitle} and are there any extra charges?`,
      answer: `The complete ${programLabel} tuition is ${fee} (all inclusive) for 2 months (8 weeks). ${
        isFellowship
          ? 'Candidates who already paid the ₹499 caution deposit pay only the remaining ₹1,500 balance at dbert.in/enroll/1999.'
          : 'Zero hidden fees; includes full curriculum labs and evaluated reviews.'
      }`
    },
    {
      question: `What is the difference between Launchpad (₹7,999), Accelerate (₹4,999), and Fellowship (₹1,999) in ${cityShort}?`,
      answer: `Launchpad (₹7,999 · 2 Months) builds 0-to-1 beginner foundations. Accelerate (₹4,999 · 2 Months) focuses on intermediate applied industry builds. Fellowship (₹1,999 · 2 Months) places job-ready builders directly onto live client repositories with 3-doc verification and placement support.`
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: trackTitle,
        description: `${programLabel} (2 Months · 8 Weeks · ${fee}) tailored for learners in ${cityName}: ${headlineSummary}`,
        provider: {
          '@type': 'Organization',
          name: 'DBERT (Digital Blinc Education Research and Technology)',
          sameAs: 'https://dbert.in'
        },
        url: canonicalUrl,
        hasCourseInstance: {
          '@type': 'CourseInstance',
          courseMode: 'online',
          courseWorkload: 'P2M',
          location: {
            '@type': 'Place',
            name: `${cityName} Remote & Tech Corridor Hub`,
            address: {
              '@type': 'PostalAddress',
              streetAddress: cityData.street,
              addressLocality: cityData.locality,
              addressRegion: cityData.region,
              postalCode: cityData.postalCode,
              addressCountry: 'IN'
            }
          }
        },
        offers: {
          '@type': 'Offer',
          category: 'Paid',
          price: numericFee,
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          url: isFellowship ? 'https://dbert.in/enroll/1999' : `https://dbert.in${parentUrl}`
        }
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqs.map((f) => ({
          '@type': 'Question',
          name: f.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: f.answer
          }
        }))
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://dbert.in' },
          { '@type': 'ListItem', position: 2, name: 'Learners', item: 'https://dbert.in/learners' },
          {
            '@type': 'ListItem',
            position: 3,
            name: domainShort,
            item: `https://dbert.in${parentUrl}`
          },
          { '@type': 'ListItem', position: 4, name: cityShort, item: canonicalUrl }
        ]
      }
    ]
  };

  const otherCities = Object.values(GEO_CITIES)
    .filter((c) => c.slug !== city)
    .slice(0, 10);

  return (
    <div className="glow-wrapper">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="glow-spot" />

      <div className="container page-head">
        <nav aria-label="Breadcrumb" className="text-xs font-mono text-muted mb-4 flex items-center justify-center gap-2 flex-wrap">
          <Link href="/" className="hover:text-accent">Home</Link>
          <span aria-hidden="true">/</span>
          <Link href={baseRoutePrefix} className="hover:text-accent">{programLabel}</Link>
          <span aria-hidden="true">/</span>
          <Link href={parentUrl} className="hover:text-accent">{domainShort}</Link>
          <span aria-hidden="true">/</span>
          <span className="text-[var(--text-primary)]">{cityShort}</span>
        </nav>

        <div className="doclabel">
          § 01 — {cityShort.toUpperCase()} CORRIDOR · 2 MONTHS <span className="rev">{fee}</span>
        </div>

        <div className="stack-h justify-center align-baseline gap-3 flex-wrap">
          <h1 className="page-title">{trackTitle}</h1>
          <HandNote tone="amber">2 months (8 weeks) · {fee} ✍</HandNote>
        </div>

        <p className="lede-wide">{headlineSummary}</p>

        <div className="flex justify-center gap-3 flex-wrap mt-6 text-xs font-mono">
          <span className="proof-mark">
            <MapPin size={13} className="text-accent" aria-hidden="true" />
            <span>{cityName} ({cityData.region})</span>
          </span>
          <span className="proof-mark">
            <Calendar size={13} className="text-accent" aria-hidden="true" />
            <span>Duration: 2 Months (8 Weeks)</span>
          </span>
          <span className="proof-mark">
            <Award size={13} className="text-ok" aria-hidden="true" />
            <span>Fee: {fee} All Inclusive</span>
          </span>
          <span className="proof-mark proof-mark-signal">
            <ShieldCheck size={13} aria-hidden="true" />
            <span>MSME Accredited · SHA-256 Verified</span>
          </span>
        </div>

        {/* Strict On-Site Primary CTA — Zero LMS Main Button */}
        <div className="stack-h gap-4 justify-center flex-wrap mt-8">
          <Link href={primaryHref} className="btn btn-primary btn-lg">
            {primaryCtaLabel}
          </Link>
          <a href="#syllabus" className="btn btn-outline btn-lg">
            Inspect 8-Week Syllabus
          </a>
          <Link href={`/internships/${slug}/${city}`} className="btn btn-outline btn-lg">
            {domainShort} Internship in {cityShort} →
          </Link>
        </div>
      </div>

      {/* City Ecosystem + 3-Program Parity Strip */}
      <div className="container pb-block">
        <div className="grid gap-6 md:grid-cols-2 mb-8">
          <div className="card p-6 bg-card border border-line">
            <div className="doclabel text-xs mb-2">§ LOCAL INDUSTRY &amp; CAMPUS FIT · {cityShort.toUpperCase()}</div>
            <h2 className="font-mono text-lg font-bold text-white mb-2 flex items-center gap-2">
              <Building2 size={18} className="text-accent" aria-hidden="true" />
              <span>Why {domainShort} in {cityName}</span>
            </h2>
            <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-3">
              {cityData.techCorridorFocus}
            </p>
            <p className="text-xs text-muted leading-relaxed">
              <strong>Campus &amp; Remote Access ({cityData.locality}, {cityData.region}):</strong>{' '}
              {cityData.campusEcosystem}
            </p>
          </div>

          <div className="card p-6 bg-card border border-accent/40">
            <div className="doclabel text-xs mb-2">§ CLEAR 3-TIER SEPARATION (ALL 2 MONTHS)</div>
            <h2 className="font-mono text-lg font-bold text-white mb-3">
              Compare {domainShort} Tracks in {cityShort}
            </h2>
            <div className="space-y-2 text-xs">
              <Link
                href={`/learners/launchpad/${slug}/${city}`}
                className={`block p-2.5 rounded border ${
                  tier === 'launchpad' ? 'border-accent bg-accent/10 text-white' : 'border-line text-[var(--text-secondary)] hover:border-accent'
                }`}
              >
                <strong>Launchpad (₹7,999 · 2 Months):</strong> 0-to-1 Beginner Foundations &amp; Syntax Labs
              </Link>
              <Link
                href={`/learners/accelerate/${slug}/${city}`}
                className={`block p-2.5 rounded border ${
                  tier === 'accelerate' ? 'border-accent bg-accent/10 text-white' : 'border-line text-[var(--text-secondary)] hover:border-accent'
                }`}
              >
                <strong>Accelerate (₹4,999 · 2 Months):</strong> Applied Industrial Systems &amp; Architecture Sprints
              </Link>
              <Link
                href={`/learners/courses/${slug}/${city}`}
                className={`block p-2.5 rounded border ${
                  tier === 'fellowship' ? 'border-emerald-400 bg-emerald-500/10 text-white' : 'border-line text-[var(--text-secondary)] hover:border-accent'
                }`}
              >
                <strong>Fellowship (₹1,999 · 2 Months):</strong> Live Client Production Repo, 1:1 Code Reviews &amp; Placement
              </Link>
            </div>
          </div>
        </div>

        {/* 8-Week Syllabus */}
        <section id="syllabus" className="mb-10">
          <div className="doclabel text-xs mb-2">§ 02 — 8-WEEK SYLLABUS ({cityShort.toUpperCase()})</div>
          <h2 className="section-title mb-4">Structured 2-Month Curriculum</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {curriculumBlocks.map((block, idx) => (
              <div key={idx} className="card p-5 bg-card border border-line">
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="tag-chip text-xs font-mono">{block.period}</span>
                  <span className="text-[11px] font-mono text-accent flex items-center gap-1">
                    <GitPullRequest size={12} aria-hidden="true" /> Reviewed PR Sprint
                  </span>
                </div>
                <h3 className="font-mono text-base font-bold text-white mb-2">{block.title}</h3>
                <ul className="space-y-1.5 text-xs text-[var(--text-secondary)]">
                  {block.topics.map((t, tIdx) => (
                    <li key={tIdx} className="flex items-start gap-2">
                      <CheckCircle2 size={13} className="text-ok shrink-0 mt-0.5" aria-hidden="true" />
                      <span>{t}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* Tech Stack & Capstones */}
        <section className="grid gap-6 md:grid-cols-2 mb-10">
          <div className="card p-6 bg-card border border-line">
            <div className="doclabel text-xs mb-2">§ 03 — CORE TOOLING &amp; STACK</div>
            <h2 className="font-mono text-lg font-bold text-white mb-3">
              Technologies Mastered in {domainShort}
            </h2>
            <div className="space-y-2.5">
              {fellowshipTrack.technologies.map((tech, idx) => (
                <div key={idx} className="text-xs border-b border-line/40 pb-2 last:border-0">
                  <strong className="text-white font-mono">{tech.name}:</strong>{' '}
                  <span className="text-[var(--text-secondary)]">{tech.role}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="card p-6 bg-card border border-line">
            <div className="doclabel text-xs mb-2">§ 04 — VERIFIED REPOSITORY CAPSTONES</div>
            <h2 className="font-mono text-lg font-bold text-white mb-3">
              Production Codebases &amp; Deliverables
            </h2>
            <div className="space-y-4">
              {repos.map((repo, idx) => (
                <div key={idx} className="p-3 rounded bg-black/20 border border-line/60">
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className="font-mono text-sm font-bold text-white">{repo.name}</span>
                    {repo.url && (
                      <a
                        href={repo.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-accent inline-flex items-center gap-1 hover:underline"
                      >
                        GitHub <ExternalLink size={11} aria-hidden="true" />
                      </a>
                    )}
                  </div>
                  <p className="text-xs text-[var(--text-secondary)] mb-2">{repo.description}</p>
                  <div className="flex flex-wrap gap-1.5">
                    {repo.keyModules.slice(0, 4).map((m, mIdx) => (
                      <span key={mIdx} className="tag-chip text-[11px]">{m}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Cross-City Mesh (eliminates orphans) */}
        <section className="card p-6 bg-card border border-line mb-10">
          <div className="doclabel text-xs mb-2">§ 05 — OTHER INDIAN TECH HUBS FOR {domainShort.toUpperCase()}</div>
          <h2 className="font-mono text-base font-bold text-white mb-3">
            Explore {domainShort} ({fee}) in Nearby Corridors
          </h2>
          <div className="flex flex-wrap gap-2">
            {otherCities.map((c) => (
              <Link
                key={c.slug}
                href={`${baseRoutePrefix}/${slug}/${c.slug}`}
                className="tag-chip text-xs font-mono hover:border-accent hover:text-accent"
              >
                📍 {c.shortName}
              </Link>
            ))}
          </div>
        </section>

        {/* FAQs */}
        <section className="mb-10">
          <div className="doclabel text-xs mb-2">§ 06 — FREQUENTLY ASKED QUESTIONS</div>
          <h2 className="section-title mb-4">{cityShort} Enrollment &amp; Syllabus FAQs</h2>
          <div className="measure">
            <FAQAccordion items={faqs} />
          </div>
        </section>

        {/* Bottom On-Site Conversion CTA + Lead Capture */}
        <section className="grid gap-8 lg:grid-cols-2 items-start">
          <div className="card p-8 bg-card border border-accent/40">
            <div className="doclabel mb-2">§ 07 — CONFIRM YOUR 2-MONTH SEAT ({cityShort.toUpperCase()})</div>
            <h2 className="text-2xl font-bold text-white mb-3">
              Start {domainShort} in {cityShort} ({fee})
            </h2>
            <p className="text-sm text-[var(--text-secondary)] mb-6">
              Join the upcoming Monday cohort from {cityName}. Weekly 1:1 mentor reviews, evaluated GitHub milestones, and MSME-accredited credentials verified on /verify.
            </p>
            <div className="stack-h gap-3 flex-wrap">
              <Link href={primaryHref} className="btn btn-primary btn-lg inline-flex items-center gap-2">
                <span>{primaryCtaLabel}</span>
              </Link>
              <Link href={parentUrl} className="btn btn-outline btn-lg inline-flex items-center gap-2">
                <span>Full Track Dossier</span>
                <ArrowRight size={15} aria-hidden="true" />
              </Link>
            </div>
          </div>

          <TrackLeadCaptureForm
            initialDomain={slug}
            initialProgram={tier === 'fellowship' ? 'fellowship' : 'course'}
            title={`Request ${cityShort} ${domainShort} Syllabus`}
            subtitle={`Get the 2-month (${fee}) roadmap & talk with DBERT Admissions for ${cityName}.`}
          />
        </section>
      </div>
    </div>
  );
}
