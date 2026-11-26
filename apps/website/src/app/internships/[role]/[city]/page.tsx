import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import {
  GEO_CITIES,
  GEO_ROLES,
  buildGeoInternshipDescription,
  buildGeoInternshipTitle,
  generateCityHeadline,
} from '@/data/geo_domains.config';
import TrackLeadCaptureForm from '@/components/forms/TrackLeadCaptureForm';

export async function generateStaticParams() {
  const roles = Object.keys(GEO_ROLES);
  const cities = Object.keys(GEO_CITIES);
  const params: { role: string; city: string }[] = [];
  for (const role of roles) {
    for (const city of cities) {
      params.push({ role, city });
    }
  }
  return params;
}

interface PageProps {
  params: Promise<{
    role: string;
    city: string;
  }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { role, city } = await params;
  const roleData = GEO_ROLES[role];
  const cityData = GEO_CITIES[city];

  if (!roleData || !cityData) {
    return {
      title: 'Internship Not Found',
      description: 'The requested internship category was not found.'
    };
  }

  const title = buildGeoInternshipTitle(role, city);
  const description = buildGeoInternshipDescription(role, city);

  return {
    title,
    description,
    alternates: {
      canonical: `https://dbert.in/internships/${role}/${city}`
    },
    openGraph: {
      title: `${title} | DBERT`,
      description,
      url: `https://dbert.in/internships/${role}/${city}`,
      type: 'website'
    }
  };
}

export default async function ProgrammaticInternshipPage({ params }: PageProps) {
  const { role, city } = await params;
  const roleData = GEO_ROLES[role];
  const cityData = GEO_CITIES[city];

  if (!roleData || !cityData) {
    notFound();
  }

  const cityName = cityData.name;
  const isRemote = city.toLowerCase() === 'remote';
  const cityHeadline = generateCityHeadline(roleData.title, cityName);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'JobPosting',
        title: `${roleData.title} Intern (${cityName})`,
        description: `<p>${roleData.desc}</p><p><strong>Required Skills:</strong> ${roleData.skills.join(', ')}</p><p><strong>Outcome:</strong> ${cityHeadline}</p><p><strong>Location:</strong> ${cityName}</p>`,
        datePosted: '2026-11-01T00:00:00+05:30',
        validThrough: '2027-06-30T23:59:59+05:30',
        employmentType: 'INTERN',
        hiringOrganization: {
          '@type': 'Organization',
          name: 'DBERT Technical Council',
          sameAs: 'https://dbert.in',
          logo: 'https://dbert.in/logo.svg'
        },
        ...(isRemote
          ? {
              jobLocationType: 'TELECOMMUTE',
              applicantLocationRequirements: {
                '@type': 'Country',
                name: 'IN'
              }
            }
          : {
              jobLocation: {
                '@type': 'Place',
                address: {
                  '@type': 'PostalAddress',
                  streetAddress: cityData.street,
                  addressLocality: cityData.locality,
                  addressRegion: cityData.region,
                  postalCode: cityData.postalCode,
                  addressCountry: 'IN'
                }
              }
            }),
        directApply: true
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'Home',
            item: 'https://dbert.in'
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: 'Internships',
            item: 'https://dbert.in/internships'
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: `${roleData.title} in ${cityName}`,
            item: `https://dbert.in/internships/${role}/${city}`
          }
        ]
      },
      {
        '@type': 'FAQPage',
        mainEntity: [
          {
            '@type': 'Question',
            name: `What are the eligibility requirements for ${roleData.title} internships in ${cityName}?`,
            acceptedAnswer: {
              '@type': 'Answer',
              text: `Applicants should have basic competence in ${roleData.skills.slice(0, 3).join(', ')}. Students across all engineering colleges in India (B.Tech, BCA, MCA, B.Sc) are eligible. DBERT offers no free internship track; candidates join via either the ₹499 Security Deposit Track on lms.dbert.in or the ₹1,999 Applied Fellowship Program.`
            }
          },
          {
            '@type': 'Question',
            name: `What career outcome is guaranteed for the ${cityName} cohort?`,
            acceptedAnswer: {
              '@type': 'Answer',
              text: `Fellows receive 100% Guaranteed Production Internship with Dedicated Placement Assistance across internal DBERT portfolio ventures (Gayatri AI, Alkame, Aivara) or verified corporate hiring partners upon completing sprint milestones.`
            }
          },
          {
            '@type': 'Question',
            name: `How do I apply for the next ${cityName} cohort?`,
            acceptedAnswer: {
              '@type': 'Answer',
              text: `Applications are processed directly on our LMS portal at lms.dbert.in. Choose your track during signup to auto-fill your application.`
            }
          }
        ]
      }
    ]
  };

  return (
    <div className="glow-wrapper">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="glow-spot"></div>
      <div className="hero-glow" aria-hidden="true" />

      {/* 1. Breadcrumb */}
      <div className="container" style={{ paddingTop: '2rem', position: 'relative', zIndex: 1 }}>
        <nav aria-label="Breadcrumb" className="text-xs font-mono text-muted mb-6 flex items-center gap-2 flex-wrap">
          <Link href="/" className="hover:text-accent">Home</Link>
          <span aria-hidden="true">/</span>
          <Link href="/internships" className="hover:text-accent">Internships</Link>
          <span aria-hidden="true">/</span>
          <Link href={`/internships/${role}`} className="hover:text-accent">{roleData.title}</Link>
          <span aria-hidden="true">/</span>
          <span className="text-[var(--text-primary)]">{cityName}</span>
        </nav>
      </div>

      {/* 2. Hero — Left-aligned, consistent with course & city pages */}
      <div className="container" style={{ paddingBottom: '3.5rem', position: 'relative', zIndex: 1 }}>
        <div style={{ maxWidth: '820px' }}>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-accent/30 bg-accent/10 text-xs font-mono text-accent mb-5">
            <span>{cityName} Regional Sprint &middot; 2026/2027 Cohort</span>
          </div>

          <h1 style={{ fontSize: 'clamp(2rem, 4.2vw, 3.25rem)', fontWeight: 800, lineHeight: 1.1, color: '#fff', marginBottom: '1rem', letterSpacing: '-0.025em' }}>
            {roleData.title} Internships
            <br />
            <span style={{ background: 'linear-gradient(90deg, #38bdf8, #818cf8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', display: 'inline-block' }}>
              in {cityName}
            </span>
          </h1>

          <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', lineHeight: 1.65, maxWidth: '58ch', marginBottom: '1.5rem' }}>
            {roleData.desc} Join our embedded venture squads, receive senior pull-request reviews, secure 100% Guaranteed Production Internship with Dedicated Placement Assistance, and graduate with cryptographic MSME credentials.
          </p>

          <div className="flex gap-2.5 flex-wrap mb-7 text-xs font-mono">
            <span className="proof-mark proof-mark-signal">
              <span>⚡ {cityHeadline}</span>
            </span>
            <span className="proof-mark">
              <span>✓ Plagiarism-Checked Portfolio</span>
            </span>
            <span className="proof-mark">
              <span>✓ {isRemote ? '100% Remote Program' : `${cityName} Hub & Remote`}</span>
            </span>
            <span className="proof-mark">
              <span>✓ MSME Verified Certificate</span>
            </span>
          </div>

          <div className="stack-h gap-3 flex-wrap">
            <a href="#apply-lead-form" className="btn btn-primary btn-lg">
              Apply &amp; Request Syllabus &rarr;
            </a>
            <Link
              href={`/enroll/1999?domain=${encodeURIComponent(roleData.title)}`}
              className="btn btn-outline btn-lg"
            >
              Confirm Fellowship Seat — ₹1,999
            </Link>
            <Link
              href={`/learners/courses/${role}`}
              className="btn btn-outline btn-lg"
            >
              Inspect Course Curriculum
            </Link>
          </div>

          {/* Responsive Hero Metrics */}
          <div className="hero-metrics">
            <div className="hero-metric">
              <div className="hero-metric-value">₹1,999</div>
              <div className="hero-metric-label">Fellowship Seat</div>
            </div>
            <div className="hero-metric">
              <div className="hero-metric-value">₹5,000</div>
              <div className="hero-metric-label">5,000 Coins Stipend</div>
            </div>
            <div className="hero-metric">
              <div className="hero-metric-value">2 Mo</div>
              <div className="hero-metric-label">Sprint Duration</div>
            </div>
            <div className="hero-metric">
              <div className="hero-metric-value">MSME</div>
              <div className="hero-metric-label">3-Doc Credential</div>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Fast-Track Application & Tiered Value Ladder */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">Join {roleData.title} in {cityName}</h2>
          <p className="section-subheading">
            Apply directly to our venture squad. Your profile will be automatically tagged with the {roleData.title} domain track and linked to the {cityName} regional engineering corridor.
          </p>

          <div className="grid gap-6 md:grid-cols-2">
            <div className="card p-6 bg-card border border-accent/30">
              <div className="font-mono text-sm font-bold text-amber-400 mb-2">
                ★ Tiered Value Ladder (Certificate → Stipend → Placement)
              </div>
              <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-4">
                1. Verified Certificate &rarr; 2. ₹5,000 Stipend (5,000 Coins via UPI) unlocked after 2-month completion (10 hrs/wk, 2 certifications, 75 tasks &amp; approved capstone) + up to ₹18,000 Ambassador bonus &rarr; 3. Direct Round-1 Screening Waiver &amp; Placement Assistance.
              </p>
              <div className="flex flex-wrap gap-3">
                <Link
                  href={`/enroll/1999?domain=${encodeURIComponent(roleData.title)}`}
                  className="btn btn-primary btn-sm"
                >
                  Confirm Seat — ₹1,999 &rarr;
                </Link>
                <a
                  href={`https://lms.dbert.in/#signup?domain=${role}&next=/internships/${role}/${city}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline btn-sm"
                >
                  Apply on LMS (₹499 Track) ↗
                </a>
              </div>
            </div>

            <div className="card p-6 bg-card border border-line">
              <div className="font-mono text-sm font-bold text-emerald-400 mb-2">
                ✓ Skill-Based Selection
              </div>
              <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-4">
                Applications are reviewed through practical project checks and originality verification. Selected candidates receive a verified certificate, scorecard, and recommendation letter.
              </p>
              <Link href={`/learners/courses/${role}`} className="text-xs font-mono text-accent hover:underline">
                View {roleData.title} Course Curriculum &rarr;
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Lead Capture Form — Placed directly below Fast-Track / Trust section */}
      <section className="section-band-clear">
        <div className="container">
          <h2 className="section-heading">Register for {roleData.title} ({cityName})</h2>
          <p className="section-subheading">
            Submit your details for priority screening, direct curriculum syllabus download, and admissions squad consultation.
          </p>
          <div className="max-w-xl mx-auto">
            <TrackLeadCaptureForm
              initialCity={cityName}
              initialDomain={role}
              title={`Register for ${roleData.title} (${cityName})`}
              subtitle="Submit your details for priority screening, direct curriculum syllabus download, and admissions squad consultation."
            />
          </div>
        </div>
      </section>

      {/* 5. Tech Stack & Core Competencies */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">Technical Stack &amp; Deliverables</h2>
          <p className="section-subheading">
            Core production tools you will use daily and the verified engineering artifacts you will ship.
          </p>

          <div className="grid gap-6 md:grid-cols-2">
            <div className="card p-6 bg-card border border-line">
              <h3 className="font-mono text-lg font-bold text-white mb-3">Target Stack &amp; Tools</h3>
              <p className="text-xs text-muted mb-4">
                Fellows use these production tools daily to write clean, modular, and maintainable software:
              </p>
              <div className="flex flex-wrap gap-2">
                {roleData.skills.map((skill, idx) => (
                  <span key={idx} className="tag-chip text-xs font-mono">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div className="card p-6 bg-card border border-line">
              <h3 className="font-mono text-lg font-bold text-white mb-3">What You Will Achieve</h3>
              <ul className="text-xs text-[var(--text-secondary)] space-y-2 list-disc list-inside">
                <li>Real-world projects reviewed and graded by senior industry mentors.</li>
                <li>Originality-verified portfolio proving authentic hands-on work.</li>
                <li>Official verified certificate, evaluation scorecard, and recommendation letter.</li>
                <li>Direct referral visibility to partner companies across India.</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* 6. Mid-Page CTA Conversion Banner */}
      <section className="section-band-clear">
        <div className="container">
          <div className="cta-banner">
            <div className="cta-inline-band">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  Ready to start your {roleData.title} sprint in {cityName}?
                </h2>
                <p className="text-sm text-[var(--text-secondary)]">
                  Choose your track: Confirm the ₹1,999 Fellowship seat directly or apply for the ₹499 Security Deposit Track on the DBERT LMS.
                </p>
              </div>
              <div className="stack-h gap-3 flex-wrap" style={{ minWidth: 'max-content' }}>
                <Link
                  href={`/enroll/1999?domain=${encodeURIComponent(roleData.title)}`}
                  className="btn btn-primary btn-lg"
                >
                  Confirm Fellowship Seat — ₹1,999 &rarr;
                </Link>
                <a
                  href={`https://lms.dbert.in/#signup?domain=${role}&next=/internships/${role}/${city}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline btn-lg"
                >
                  Apply on LMS (₹499 Track) ↗
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 7. Regional Internship Hubs */}
      <section className="section-alt">
        <div className="container">
          <h2 className="section-heading">Explore {roleData.title} in Other Cities</h2>
          <p className="section-subheading">
            Browse {roleData.title} internship cohorts across other major Indian tech corridors.
          </p>
          <div className="card p-6 bg-card border border-line">
            <div className="flex flex-wrap gap-2 mb-6">
              {Object.entries(GEO_CITIES).map(([cSlug, cMeta]) => (
                <Link
                  key={cSlug}
                  href={`/internships/${role}/${cSlug}`}
                  className={`tag-chip text-xs font-mono ${cSlug === city ? 'border-accent text-accent' : ''}`}
                >
                  {cMeta.name}
                </Link>
              ))}
            </div>

            <div className="text-center pt-4 border-t border-line">
              <Link href="/internships" className="btn btn-outline btn-sm">
                &larr; Return to All Internship Domains
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
