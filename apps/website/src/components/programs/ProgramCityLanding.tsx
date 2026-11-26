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
          ? 'Zero hidden fees; enroll directly at dbert.in/enroll/1999.'
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
      <div className="hero-glow" aria-hidden="true" />

      {/* 1. Breadcrumb */}
      <div className="container" style={{ paddingTop: '2rem', position: 'relative', zIndex: 1 }}>
        <nav aria-label="Breadcrumb" className="text-xs font-mono text-muted mb-6 flex items-center gap-2 flex-wrap">
          <Link href="/" className="hover:text-accent">Home</Link>
          <span aria-hidden="true">/</span>
          <Link href={baseRoutePrefix} className="hover:text-accent">{programLabel}</Link>
          <span aria-hidden="true">/</span>
          <Link href={parentUrl} className="hover:text-accent">{domainShort}</Link>
          <span aria-hidden="true">/</span>
          <span className="text-[var(--text-primary)]">{cityShort}</span>
        </nav>
      </div>

      {/* 2. Hero — Left-aligned, clean, responsive */}
      <div className="container" style={{ paddingBottom: '3.5rem', position: 'relative', zIndex: 1 }}>
        <div style={{ maxWidth: '820px' }}>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-accent/30 bg-accent/10 text-xs font-mono text-accent mb-5">
            <MapPin size={12} aria-hidden="true" />
            <span>{cityShort} Tech Corridor &middot; 2 Months &middot; {fee}</span>
          </div>

          <div className="stack-h items-baseline gap-3 flex-wrap mb-3">
            <h1 style={{ fontSize: 'clamp(2rem, 4.2vw, 3.25rem)', fontWeight: 800, lineHeight: 1.1, color: '#fff', letterSpacing: '-0.025em' }}>
              {trackTitle}
            </h1>
            <HandNote tone="amber">2 months (8 weeks) · {fee} ✍</HandNote>
          </div>

          <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', lineHeight: 1.65, maxWidth: '58ch', marginBottom: '1.5rem' }}>
            {headlineSummary}
          </p>

          <div className="flex gap-2.5 flex-wrap mb-7 text-xs font-mono">
            <span className="proof-mark">
              <MapPin size={13} className="text-accent" aria-hidden="true" />
              <span>{cityName} ({cityData.region})</span>
            </span>
            <span className="proof-mark">
              <Calendar size={13} className="text-accent" aria-hidden="true" />
              <span>2 Months (8 Weeks)</span>
            </span>
            <span className="proof-mark">
              <Award size={13} className="text-ok" aria-hidden="true" />
              <span>Fee: {fee} All Inclusive</span>
            </span>
            <span className="proof-mark proof-mark-signal">
              <ShieldCheck size={13} aria-hidden="true" />
              <span>MSME Accredited · Verified Certificate</span>
            </span>
          </div>

          {/* Primary CTAs */}
          <div className="stack-h gap-3 flex-wrap">
            <a href="#apply-lead-form" className="btn btn-primary btn-lg">
              Request {cityShort} Syllabus &amp; Apply &rarr;
            </a>
            <Link href={primaryHref} className="btn btn-outline btn-lg">
              {primaryCtaLabel}
            </Link>
            <a href="#syllabus" className="btn btn-outline btn-lg">
              View 8-Week Syllabus
            </a>
          </div>

          {/* Responsive Hero Metrics */}
          <div className="hero-metrics">
            <div className="hero-metric">
              <div className="hero-metric-value">{fee}</div>
              <div className="hero-metric-label">All-Inclusive Fee</div>
            </div>
            <div className="hero-metric">
              <div className="hero-metric-value">8 Wks</div>
              <div className="hero-metric-label">Guided Program</div>
            </div>
            <div className="hero-metric">
              <div className="hero-metric-value">1:1</div>
              <div className="hero-metric-label">Mentor Reviews</div>
            </div>
            <div className="hero-metric">
              <div className="hero-metric-value">MSME</div>
              <div className="hero-metric-label">Verified Certificate</div>
            </div>
          </div>
        </div>
      </div>

      {/* 3. City Ecosystem + 3-Tier Comparison */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">Why {domainShort} in {cityName}</h2>
          <p className="section-subheading">
            Localized sprint alignment for {cityName} campuses and tech corridors, with three clear 2-month tracks.
          </p>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="card p-6 bg-card border border-line">
              <div className="text-xs font-mono uppercase tracking-wider text-accent mb-2">
                Local Industry &amp; Campus Fit · {cityShort}
              </div>
              <h3 className="font-mono text-lg font-bold text-white mb-2 flex items-center gap-2">
                <Building2 size={18} className="text-accent" aria-hidden="true" />
                <span>{cityName} Tech Corridor</span>
              </h3>
              <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-3">
                {cityData.techCorridorFocus}
              </p>
              <p className="text-xs text-muted leading-relaxed">
                <strong>Campus &amp; Remote Access ({cityData.locality}, {cityData.region}):</strong>{' '}
                {cityData.campusEcosystem}
              </p>
            </div>

            <div className="card p-6 bg-card border border-accent/40">
              <div className="text-xs font-mono uppercase tracking-wider text-accent mb-2">
                Clear 3-Tier Separation (All 2 Months)
              </div>
              <h3 className="font-mono text-lg font-bold text-white mb-3">
                Compare {domainShort} Tracks in {cityShort}
              </h3>
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
        </div>
      </section>

      {/* 4. Lead Capture Form — Placed directly below City Ecosystem / Trust Strip */}
      <section className="section-band-clear">
        <div className="container">
          <h2 className="section-heading">Get the {cityShort} {domainShort} Syllabus</h2>
          <p className="section-subheading">
            Submit your details to receive the 2-month ({fee}) roadmap and connect with DBERT Admissions for {cityName}.
          </p>
          <div className="max-w-xl mx-auto">
            <TrackLeadCaptureForm
              initialDomain={slug}
              initialCity={cityShort}
              initialProgram={tier === 'fellowship' ? 'fellowship' : 'course'}
              title={`Request ${cityShort} ${domainShort} Syllabus`}
              subtitle={`Get the 2-month (${fee}) roadmap & talk with DBERT Admissions for ${cityName}.`}
            />
          </div>
        </div>
      </section>

      {/* 5. 8-Week Syllabus */}
      <section id="syllabus" className="section-alt">
        <div className="container">
          <h2 className="section-heading">8-Week Learning Roadmap</h2>
          <p className="section-subheading">
            Four bi-weekly mentor-reviewed project modules designed for learners in {cityName} ({cityData.region}).
          </p>
          <div className="grid gap-4 md:grid-cols-2">
            {curriculumBlocks.map((block, idx) => (
              <div key={idx} className="card p-5 bg-card border border-line">
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="tag-chip text-xs font-mono">{block.period}</span>
                  <span className="text-[11px] font-mono text-accent flex items-center gap-1">
                    <GitPullRequest size={12} aria-hidden="true" /> Mentor-Reviewed Project
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
        </div>
      </section>

      {/* 6. Tech Stack & Capstones (Combined) */}
      <section className="section-band-clear">
        <div className="container">
          <h2 className="section-heading">Tools &amp; Real-World Projects</h2>
          <p className="section-subheading">
            Industry tools you will master and live team projects you will build for your portfolio.
          </p>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="card p-6 bg-card border border-line">
              <div className="text-xs font-mono uppercase tracking-wider text-accent mb-2">Tools You Will Master</div>
              <h3 className="font-mono text-lg font-bold text-white mb-3">
                Core Technologies in {domainShort}
              </h3>
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
              <div className="text-xs font-mono uppercase tracking-wider text-accent mb-2">Real-World Projects</div>
              <h3 className="font-mono text-lg font-bold text-white mb-3">
                Live Projects &amp; Deliverables
              </h3>
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
          </div>
        </div>
      </section>

      {/* 7. Mid-Page CTA Conversion Banner */}
      <section className="section-alt">
        <div className="container">
          <div className="cta-banner">
            <div className="cta-inline-band">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  Ready to start {domainShort} in {cityShort}?
                </h2>
                <p className="text-sm text-[var(--text-secondary)]">
                  All-inclusive {fee} tuition for 2 months. Join the upcoming Monday sprint cohort from {cityName}.
                </p>
              </div>
              <div className="stack-h gap-3 flex-wrap" style={{ minWidth: 'max-content' }}>
                <Link href={primaryHref} className="btn btn-primary btn-lg inline-flex items-center gap-2">
                  <span>{primaryCtaLabel}</span>
                </Link>
                <Link href={`/internships/${slug}/${city}`} className="btn btn-outline btn-lg inline-flex items-center gap-2">
                  <span>{domainShort} Internship in {cityShort} &rarr;</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 8. Cross-City Mesh */}
      <section className="section-band-clear">
        <div className="container">
          <h2 className="section-heading">Explore {domainShort} in Nearby Corridors</h2>
          <p className="section-subheading">
            Compare {domainShort} ({fee}) cohorts across other Indian tech cities.
          </p>
          <div className="card p-6 bg-card border border-line">
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
          </div>
        </div>
      </section>

      {/* 9. FAQs */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">{cityShort} Enrollment &amp; Syllabus FAQs</h2>
          <p className="section-subheading">
            Common questions from learners in {cityName} regarding tuition, schedule, and credentials.
          </p>
          <div className="measure mx-auto">
            <FAQAccordion items={faqs} />
          </div>
        </div>
      </section>

      {/* 10. Final Conversion Banner */}
      <section className="section-band-clear">
        <div className="container">
          <div className="cta-banner">
            <div className="cta-inline-band">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  Confirm Your 2-Month Seat ({cityShort})
                </h2>
                <p className="text-sm text-[var(--text-secondary)]">
                  Weekly 1:1 mentor reviews, evaluated project milestones, and government-recognized (MSME) verified certificates on /verify.
                </p>
              </div>
              <div className="stack-h gap-3 flex-wrap" style={{ minWidth: 'max-content' }}>
                <Link href={primaryHref} className="btn btn-primary btn-lg inline-flex items-center gap-2">
                  <span>{primaryCtaLabel}</span>
                </Link>
                <Link href={parentUrl} className="btn btn-outline btn-lg inline-flex items-center gap-2">
                  <span>View Full Program</span>
                  <ArrowRight size={15} aria-hidden="true" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
