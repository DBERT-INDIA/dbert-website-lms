import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { lmsInternshipSignupUrl } from '@/lib/lmsLinks';
import { notFound } from 'next/navigation';
import HandNote from '@/components/ui/HandNote';
import { GEO_CITIES, GEO_ROLES, generateCityHeadline } from '@/data/geo_domains.config';
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

  const cityName = cityData.name;
  const title = `${roleData.title} Internship in ${cityName} — 100% Guaranteed Production Internship`;
  const description = `Apply for ${roleData.title} production internship in ${cityName}. Build live client codebases under senior review, secure 100% Guaranteed Production Internship with Dedicated Placement Assistance, and graduate with verifiable MSME credentials.`;

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
              text: `Applicants should have basic competence in ${roleData.skills.slice(0, 3).join(', ')}. Students across all engineering colleges in India (B.Tech, BCA, MCA, B.Sc) are eligible. Selection is based purely on code screening with zero application fees.`
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

      {/* Hero Header */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — {cityName.toUpperCase()} REGIONAL SPRINT
        </div>
        <div className="stack-h justify-center align-baseline gap-3 flex-wrap">
          <h1 className="page-title">
            {roleData.title} Internships in {cityName}
          </h1>
          <HandNote tone="amber">
            {cityHeadline} ✎
          </HandNote>
        </div>
        <p className="lede-wide">
          {roleData.desc} Join our embedded venture squads, receive senior pull-request reviews, secure 100% Guaranteed Production Internship with Dedicated Placement Assistance, and graduate with cryptographic MSME credentials.
        </p>

        <div className="flex justify-center gap-3 flex-wrap mt-4">
          <span className="proof-mark proof-mark-signal">
            <span>⚡ {cityHeadline}</span>
          </span>
          <span className="proof-mark">
            <span>✓ Verified Turnitin Rubrics</span>
          </span>
          <span className="proof-mark">
            <span>✓ {isRemote ? '100% Virtual Sprints' : `${cityName} Hub & Remote`}</span>
          </span>
          <span className="proof-mark">
            <span>✓ MSME Registered Credentials</span>
          </span>
        </div>
      </div>

      {/* Primary Conversion & Inbound Lead Capture Section */}
      <div className="section-band" style={{ padding: '60px 0', background: 'rgba(255, 255, 255, 0.015)', borderTop: '1px solid rgba(255, 255, 255, 0.08)', borderBottom: '1px solid rgba(255, 255, 255, 0.08)' }}>
        <div className="container">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 280px), 1fr))', gap: 36, alignItems: 'start' }}>
            
            {/* Left Column: LMS Direct Links & Fast-Track Route */}
            <div>
              <div className="doclabel mb-2">§ 02 — FAST-TRACK APPLICATION</div>
              <h2 className="section-title mb-3" style={{ textAlign: 'left', fontSize: '2rem' }}>
                Join {roleData.title} in {cityName}
              </h2>
              <p className="band-lede mb-6" style={{ textAlign: 'left', maxWidth: '100%', fontSize: '0.95rem', color: '#94a3b8' }}>
                Apply directly to our venture squad. Your profile will be automatically tagged with the <strong>{roleData.title}</strong> domain track and linked to the <strong>{cityName}</strong> regional engineering corridor.
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 24 }}>
                <a
                  href={lmsInternshipSignupUrl(role, city)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-primary btn-lg"
                  style={{ textAlign: 'center' }}
                >
                  Apply on LMS (Track Auto-Selected) ↗
                </a>
                <Link 
                  href={`/enroll/1999?domain=${encodeURIComponent(roleData.title)}`} 
                  className="btn btn-outline btn-lg"
                  style={{ textAlign: 'center', borderColor: '#f59e0b', color: '#fbbf24' }}
                >
                  Confirm Fellowship Seat (₹1,999 Program) →
                </Link>
                <a
                  href={`https://lms.dbert.in/internships/${role}/${city}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline btn-sm"
                  style={{ textAlign: 'center', opacity: 0.8 }}
                >
                  Browse openings in {cityName} on the LMS ↗
                </a>
              </div>

              {/* Verified Trust Badges */}
              <div style={{ padding: 16, background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: 8, fontSize: '0.8rem', color: '#cbd5e1' }}>
                <div style={{ fontWeight: 700, color: '#10b981', marginBottom: 4 }}>✓ Automated Selection Gating</div>
                <div>Applications are scored on algorithmic code reviews and Turnitin originality verification (&lt;5% threshold). Selected candidates receive verified 3-document credential packets.</div>
              </div>
            </div>

            {/* Right Column: Embedded Dynamic Lead Capture Form */}
            <div>
              <TrackLeadCaptureForm
                initialCity={cityName}
                initialDomain={role}
                title={`Register for ${roleData.title} (${cityName})`}
                subtitle="Submit your details for priority screening, direct curriculum syllabus download, and admissions squad consultation."
              />
            </div>

          </div>
        </div>
      </div>

      {/* Tech Stack & Core Competencies */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 03 — TECHNICAL SPECIFICATIONS</div>
        <h2 className="section-title">
          Core Technologies &amp; Deliverables
        </h2>

        <div className="grid gap-6 md:grid-cols-2 my-6">
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
            <h3 className="font-mono text-lg font-bold text-white mb-3">What You Ship</h3>
            <ul className="text-xs text-[var(--text-secondary)] space-y-2 list-disc list-inside">
              <li>Pull requests reviewed and graded by senior staff architects.</li>
              <li>Turnitin originality report proving zero plagiarism on capstones.</li>
              <li>Official 3-document credential packet (Certificate, Evaluation Rubric, LOR).</li>
              <li>Referral visibility to partner startups across India.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Breadcrumb Navigation & City Interlinking */}
      <div className="band-top">
        <div className="container">
          <div className="doclabel mb-2">§ 04 — REGIONAL INTERNSHIP HUBS</div>
          <p className="text-xs text-muted mb-4">
            Explore {roleData.title} opportunities across other major Indian tech corridors:
          </p>
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
    </div>
  );
}
