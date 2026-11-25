import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import {
  GEO_CITIES,
  GEO_ROLES,
  GEO_SHORT_DOMAIN_LABELS,
  buildGeoInternshipDescription,
  buildGeoInternshipTitle,
  generateCityHeadline,
} from '@/data/geo_domains.config';
import TrackLeadCaptureForm from '@/components/forms/TrackLeadCaptureForm';
import { MapPin, Briefcase, Award, ShieldCheck, CheckCircle2, ArrowRight, Building, GraduationCap, Banknote } from 'lucide-react';
import s from '../../learners/learners.module.css';

interface PageProps {
  params: Promise<{ role: string }>;
}

export async function generateStaticParams() {
  const cityParams = Object.keys(GEO_CITIES).map((role) => ({ role }));
  const roleParams = Object.keys(GEO_ROLES).map((role) => ({ role }));
  return [...cityParams, ...roleParams];
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { role: slug } = await params;

  // Case 1: City Slug
  if (GEO_CITIES[slug]) {
    const city = GEO_CITIES[slug];
    const title = `Tech & AI Internships in ${city.shortName} (2027)`;
    const description = `Apply for verified 2-month AI and software internships in ${city.shortName}. Ship client PRs with 1:1 mentor reviews, MSME credentials, and placement support.`;
    return {
      title,
      description,
      alternates: { canonical: `https://dbert.in/internships/${slug}` },
      openGraph: {
        title: `${title} | DBERT`,
        description,
        url: `https://dbert.in/internships/${slug}`,
        type: 'website'
      }
    };
  }

  // Case 2: Role Slug
  if (GEO_ROLES[slug]) {
    const roleShort = GEO_SHORT_DOMAIN_LABELS[slug] || GEO_ROLES[slug].title;
    const title = `${roleShort} Internships in India (2027)`;
    const description = `Apply for 2-month ${roleShort} production internships across 18 Indian cities and remote hubs. Ship live PRs with mentor reviews and verified MSME certs.`;
    return {
      title,
      description,
      alternates: { canonical: `https://dbert.in/internships/${slug}` },
      openGraph: {
        title: `${title} | DBERT`,
        description,
        url: `https://dbert.in/internships/${slug}`,
        type: 'website'
      }
    };
  }

  // Case 3: Combined slug format: [role]-internships-in-[city]
  const match = slug.match(/^([a-z-]+)-internships-in-([a-z-]+)$/);
  if (match) {
    const [, rSlug, cSlug] = match;
    const role = GEO_ROLES[rSlug];
    const city = GEO_CITIES[cSlug];
    if (role && city) {
      const title = buildGeoInternshipTitle(rSlug, cSlug);
      const description = buildGeoInternshipDescription(rSlug, cSlug);
      return {
        title,
        description,
        alternates: { canonical: `https://dbert.in/internships/${slug}` },
        openGraph: {
          title: `${title} | DBERT`,
          description,
          url: `https://dbert.in/internships/${slug}`,
          type: 'website'
        }
      };
    }
  }

  return {
    title: 'Internships',
    description: 'Explore verified engineering and AI production internships across India and global remote tech hubs with dedicated placement assistance.',
    alternates: { canonical: 'https://dbert.in/internships' },
    openGraph: {
      title: 'Internships | DBERT',
      description: 'Explore verified engineering and AI production internships across India and global remote tech hubs with dedicated placement assistance.',
      url: 'https://dbert.in/internships',
      type: 'website'
    }
  };
}

export default async function InternshipSlugDispatcher({ params }: PageProps) {
  const { role: slug } = await params;

  let cityData = GEO_CITIES[slug];
  let roleData = GEO_ROLES[slug];
  let isCombined = false;

  if (!cityData && !roleData) {
    const match = slug.match(/^([a-z-]+)-internships-in-([a-z-]+)$/);
    if (match) {
      const [, rSlug, cSlug] = match;
      roleData = GEO_ROLES[rSlug];
      cityData = GEO_CITIES[cSlug];
      isCombined = true;
    }
  }

  if (!cityData && !roleData) {
    notFound();
  }

  const pageTitle = isCombined && roleData && cityData
    ? `${roleData.title} Internships in ${cityData.name}`
    : cityData
    ? `Software & AI Internships in ${cityData.name}`
    : `${roleData?.title} Internships`;

  const pageSubtitle = cityData
    ? `Verified venture squad internships across ${cityData.locality}, ${cityData.region}. Build production features, pass Turnitin evaluations, and secure 100% Guaranteed Production Internship with Dedicated Placement Assistance.`
    : `Verified engineering sprint internships across 18 tech hubs. Build production codebases with senior code reviews and 100% Guaranteed Production Internship with Dedicated Placement Assistance.`;

  const headline = isCombined && roleData && cityData
    ? generateCityHeadline(roleData.title, cityData.name)
    : cityData
    ? generateCityHeadline('Engineering & AI Internships', cityData.name)
    : roleData
    ? generateCityHeadline(roleData.title, 'Pan-India')
    : 'Engineering & AI Internships — 100% Guaranteed Production Internship with Dedicated Placement Assistance';

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'JobPosting',
        '@id': `https://dbert.in/internships/${slug}#job`,
        title: pageTitle,
        description: `<p>${pageSubtitle}</p><p><strong>Outcome:</strong> ${headline}.</p>`,
        datePosted: '2026-11-01T00:00:00+05:30',
        validThrough: '2027-06-30T23:59:59+05:30',
        employmentType: 'INTERN',
        hiringOrganization: {
          '@type': 'Organization',
          '@id': 'https://dbert.in/#organization',
          name: 'DBERT Technical Council & Venture Studio',
          url: 'https://dbert.in'
        },
        jobLocation: cityData && cityData.slug !== 'remote'
          ? {
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
          : undefined,
        jobLocationType: (!cityData || cityData.slug === 'remote') ? 'TELECOMMUTE' : undefined,

      }
    ]
  };

  return (
    <div className={s.pageWrapper} style={{ background: '#0a0a0f', minHeight: '100vh', color: '#f8fafc' }}>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '60px 20px 80px' }}>
        {/* Breadcrumb Navigation */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.85rem', color: '#94a3b8', marginBottom: 24 }}>
          <Link href="/" style={{ color: '#94a3b8', textDecoration: 'none' }}>Home</Link>
          <span>/</span>
          <Link href="/internships" style={{ color: '#94a3b8', textDecoration: 'none' }}>Internships</Link>
          <span>/</span>
          <span style={{ color: '#38bdf8', fontWeight: 600 }}>{pageTitle}</span>
        </div>

        {/* Hero Section */}
        <div style={{ marginBottom: 40, borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: 32 }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '4px 12px', background: 'rgba(56,189,248,0.1)', border: '1px solid rgba(56,189,248,0.2)', borderRadius: 20, color: '#38bdf8', fontSize: '0.8rem', fontWeight: 600, marginBottom: 16 }}>
            <ShieldCheck size={14} /> Official DBERT Venture Studio Internship Track
          </div>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: 12, color: '#ffffff' }}>
            {pageTitle}
          </h1>
          <p style={{ fontSize: '1.05rem', color: '#94a3b8', maxWidth: 800, lineHeight: 1.6 }}>
            {pageSubtitle}
          </p>

          {cityData && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16, marginTop: 20, fontSize: '0.85rem', color: '#cbd5e1' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <MapPin size={16} style={{ color: '#38bdf8' }} /> {cityData.locality}, {cityData.region}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Building size={16} style={{ color: '#10b981' }} /> {cityData.street}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Briefcase size={16} style={{ color: '#10b981' }} /> {headline}
              </span>
            </div>
          )}
        </div>

        {/* Responsive 2-Column Split: Detailed Info + Lead Capture Form */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 340px), 1fr))', gap: 36, alignItems: 'start' }}>
          
          {/* Left Column: Curricular & Sprint Details */}
          <div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 28 }}>
              <div style={{ padding: 16, background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: 8 }}>
                <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: 700, textTransform: 'uppercase' }}>Program Duration</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', marginTop: 2 }}>2 Months (8 Weeks)</div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: 4 }}>10.0 hrs/week logged with senior architect code reviews</div>
              </div>
              <div style={{ padding: 16, background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: 8 }}>
                <div style={{ fontSize: '0.75rem', color: '#a855f7', fontWeight: 700, textTransform: 'uppercase' }}>Verifiable Credentials</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', marginTop: 2 }}>3-Doc Packet</div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: 4 }}>Cryptographic UUID verifiable on dbert.in/verify</div>
              </div>
            </div>

            {/* Role Technical Highlights & Multi-City Hubs if Role is selected */}
            {roleData && (
              <>
                <div style={{ padding: 20, background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 10, marginBottom: 24 }}>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
                    <Briefcase size={16} style={{ color: '#10b981' }} /> Role Competencies &amp; Skills Required
                  </h3>
                  <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.5, marginBottom: 12 }}>
                    {roleData.desc}
                  </p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                    {roleData.skills.map((skill) => (
                      <span key={skill} style={{ fontSize: '0.75rem', fontFamily: 'monospace', background: 'rgba(56,189,248,0.1)', border: '1px solid rgba(56,189,248,0.25)', padding: '3px 8px', borderRadius: 4, color: '#7dd3fc' }}>
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* ₹1,999 Tiered Value Ladder Fast-Track Card */}
                <div style={{ padding: 20, background: 'linear-gradient(135deg, rgba(245,158,11,0.12), rgba(15,23,42,0.9))', border: '1.5px solid rgba(245,158,11,0.35)', borderRadius: 10, marginBottom: 24 }}>
                  <div style={{ fontSize: '0.75rem', fontWeight: 800, color: '#fbbf24', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 6 }}>
                    ₹1,999 Incubation Fast-Track · 2027 Cohort
                  </div>
                  <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#ffffff', marginBottom: 8 }}>
                    Verified Certificate &rarr; ₹5,000+ Stipend &rarr; 100% Placement Assistance
                  </h3>
                  <ul style={{ fontSize: '0.82rem', color: '#e2e8f0', lineHeight: 1.6, margin: '0 0 14px 18px', padding: 0 }}>
                    <li>Cryptographic 3-document packet &amp; Turnitin originality seal on <code>/verify</code></li>
                    <li>Gate 1 ₹5,000+ stipend unlock upon shipping 3 approved PRs (&ge;75% attendance)</li>
                    <li>Direct Round-1 screening waiver + Tab 1 placement in Pre-Vetted Directory</li>
                  </ul>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, alignItems: 'center' }}>
                    <Link
                      href={`/enroll/1999?domain=${encodeURIComponent(roleData.title)}`}
                      className="btn btn-primary btn-sm"
                    >
                      Enroll Now — ₹1,999 (₹1,500 if ₹499 paid) &rarr;
                    </Link>
                    <Link
                      href={`/learners/courses/${roleData.slug}`}
                      className="btn btn-outline btn-sm"
                    >
                      Inspect Full {roleData.title} Syllabus
                    </Link>
                  </div>
                </div>

                {/* All 18 Regional Hub City Pills */}
                <div style={{ padding: 20, background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 10, marginBottom: 24 }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#ffffff', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 8 }}>
                    <MapPin size={16} style={{ color: '#38bdf8' }} /> {roleData.title} Across All 18 Indian Tech Hubs
                  </h3>
                  <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: 12 }}>
                    Select your preferred regional sprint corridor or remote hub for localized 2027 openings:
                  </p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                    {Object.values(GEO_CITIES).map((c) => (
                      <Link
                        key={c.slug}
                        href={`/internships/${roleData.slug}/${c.slug}`}
                        style={{
                          fontSize: '0.76rem',
                          fontFamily: 'monospace',
                          padding: '5px 10px',
                          borderRadius: 999,
                          background: c.slug === cityData?.slug ? 'rgba(56,189,248,0.22)' : 'rgba(255,255,255,0.04)',
                          border: c.slug === cityData?.slug ? '1px solid #38bdf8' : '1px solid rgba(255,255,255,0.12)',
                          color: c.slug === cityData?.slug ? '#7dd3fc' : '#e2e8f0',
                          textDecoration: 'none',
                        }}
                      >
                        {c.name}
                      </Link>
                    ))}
                  </div>
                </div>
              </>
            )}

            {/* Available Technical Tracks Grid if City is selected */}
            {cityData && !roleData && (
              <div style={{ marginBottom: 28 }}>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#ffffff', marginBottom: 12 }}>
                  Active Engineering Tracks in {cityData.name}
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                  {Object.entries(GEO_ROLES).slice(0, 6).map(([rKey, rVal]) => (
                    <Link
                      key={rKey}
                      href={`/internships/${rKey}/${cityData.slug}`}
                      style={{
                        padding: 12,
                        background: 'rgba(255,255,255,0.02)',
                        border: '1px solid rgba(255,255,255,0.06)',
                        borderRadius: 8,
                        textDecoration: 'none',
                        color: '#ffffff',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                      }}
                    >
                      <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{rVal.title}</span>
                      <ArrowRight size={14} style={{ color: '#10b981' }} />
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* Upstream Repository Gating Notice */}
            <div style={{ padding: 16, background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: 8 }}>
              <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#ffffff', marginBottom: 4 }}>
                Upstream PR Gating Architecture
              </div>
              <p style={{ fontSize: '0.78rem', color: '#94a3b8', lineHeight: 1.5, margin: 0 }}>
                Fellows contribute code directly to official DBERT partner repositories (Alkame, Gayatri AI, Aivara Insight Lite, and DBERT Systems). Capstones require Turnitin originality scores &lt; 5% and senior architect approval.
              </p>
            </div>
          </div>

          {/* Right Column: Sticky Lead Capture Form */}
          <div style={{ position: 'sticky', top: 24 }}>
            <TrackLeadCaptureForm
              initialCity={cityData ? cityData.name : ''}
              initialDomain={roleData ? roleData.slug : 'ai-agent-development'}
              title={`Apply for ${pageTitle}`}
              subtitle="Submit details to connect with our admissions squad and access the complete syllabus & interview preparation guide."
            />
          </div>

        </div>
      </div>
    </div>
  );
}
