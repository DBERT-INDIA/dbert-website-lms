import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { GEO_CITIES, GEO_ROLES, generateCityHeadline } from '@/data/geo_domains.config';
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
    const title = `Engineering Internships in ${city.name} — 100% Guaranteed Production Internship`;
    const description = `Explore verified engineering and AI production internships in ${city.name}. Commit upstream PRs on production repos, secure 100% Guaranteed Production Internship with Dedicated Placement Assistance, and get verified credentials.`;
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
    const role = GEO_ROLES[slug];
    const title = `${role.title} Internships — 100% Guaranteed Production Internship`;
    const description = `Apply for ${role.title} production internships. Build production codebases under senior architect review, secure 100% Guaranteed Production Internship with Dedicated Placement Assistance, and receive verifiable MSME credentials.`;
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
      const title = `${role.title} Internship in ${city.name} — 100% Guaranteed Production Internship`;
      const description = `Apply for ${role.title} production internship in ${city.name}. Work on live production codebases, secure 100% Guaranteed Production Internship with Dedicated Placement Assistance, and earn verifiable credentials.`;
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

            {/* Role Technical Highlights if Role is selected */}
            {roleData && (
              <div style={{ padding: 20, background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 10, marginBottom: 28 }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
                  <Briefcase size={16} style={{ color: '#10b981' }} /> Role Competencies & Skills Required
                </h3>
                <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.5, marginBottom: 12 }}>
                  {roleData.desc}
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                  {roleData.skills.map((s) => (
                    <span key={s} style={{ fontSize: '0.75rem', fontFamily: 'monospace', background: 'rgba(56,189,248,0.1)', border: '1px solid rgba(56,189,248,0.25)', padding: '3px 8px', borderRadius: 4, color: '#7dd3fc' }}>
                      {s}
                    </span>
                  ))}
                </div>
              </div>
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
